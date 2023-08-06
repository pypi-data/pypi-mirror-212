import uuid
import os
import subprocess
from urllib.parse import urlparse
import json
import tempfile

from spark_etl.template import GenTemplate

import oci
from oci_core import get_os_client, get_df_client, os_upload, os_upload_json

from spark_etl.deployers import AbstractDeployer
from spark_etl import Build, SparkETLDeploymentFailure
from .tools import check_response, remote_execute
from spark_etl.misc_tools import read_textfile, get_filename

def _save_json_temp(payload):
    # save a dict to temporary json file, and return filename
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(json.dumps(payload).encode('utf8'))
        return f.name

def get_job_loader(oci_config):
    # render job_loader.py, rendered result in a temporary file
    # return the rendered filename
    job_loader_filename = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'job_loader.py'
    )

    if oci_config is not None:
        oci_cfg = dict(oci_config)
        key_file = oci_cfg.pop("key_file")
        oci_key = read_textfile(key_file)

    template = GenTemplate()
    if oci_config is None:
        c = template.render(job_loader_filename,
            use_instance_principle = True,
        )
    else:
        c = template.render(job_loader_filename,
            use_instance_principle = False,
            oci_config_str = json.dumps(oci_cfg, indent=4),
            oci_key = oci_key
        )

    with tempfile.NamedTemporaryFile(mode='w+t', delete=False) as f:
        f.write(c)
        return f.name


class DataflowDeployer(AbstractDeployer):
    def __init__(self, config):
        super(DataflowDeployer, self).__init__(config)
        # config must have
        #   region, e.g., value is IAD
        #   compartment_id: the compartment we want to have the dataflow app
        #   driver_shape
        #   executor_shape
        #   (optional) driver_shape_config
        #   (optional) executor_shape_config
        #   num_executors
        #   spark_version

    @property
    def region(self):
        return self.config["region"]

    def create_application(self, manifest, destination_location):
        df_client = get_df_client(self.region, config=self.config.get("oci_config"))
        dataflow = self.config['dataflow']

        display_name = f"{manifest['display_name']}-{manifest['version']}"

        # if the application already exist, we will fail the deployment
        # since user should bump the version for new deployment
        r = df_client.list_applications(
            dataflow['compartment_id'],
            limit=1,
            display_name=display_name,
        )
        check_response(r, lambda : SparkETLDeploymentFailure("Unable to list application"))
        if len(r.data) > 0:
            raise SparkETLDeploymentFailure(f"Application {display_name} already created")

        create_application_details = oci.data_flow.models.CreateApplicationDetails(
            compartment_id=dataflow['compartment_id'],
            display_name=display_name,
            driver_shape=dataflow['driver_shape'],
            driver_shape_config=dataflow.get('driver_shape_config'),
            executor_shape_config=dataflow.get('executor_shape_config'),
            executor_shape=dataflow['executor_shape'],
            num_executors=dataflow['num_executors'],
            spark_version=dataflow.get("spark_version", "2.4.4"),
            file_uri=f"{destination_location}/{manifest['version']}/job_loader.py",
            language="PYTHON",
            archive_uri=dataflow.get("archive_uri")
        )

        r = df_client.create_application(
            create_application_details=create_application_details
        )
        check_response(r, lambda : SparkETLDeploymentFailure("Unable to create dataflow application"))
        return r.data

    def deploy(self, build_dir, destination_location):
        o = urlparse(destination_location)
        if o.scheme != 'oci':
            raise SparkETLDeploymentFailure("destination_location must be in OCI")

        namespace = o.netloc.split('@')[1]
        bucket = o.netloc.split('@')[0]
        root_path = o.path[1:]    # remove the leading "/"

        build = Build(build_dir)

        print("Uploading files:")
        # Data flow want to call python lib python.zip
        os_client = get_os_client(self.region, config=self.config.get("oci_config"))
        for artifact in build.artifacts:
            local_filename = f"{build_dir}/{artifact}"
            if artifact == "lib.zip" and not os.path.isfile(local_filename):
                # user might choose not build lib.zip in some cases
                # so do not blow up in case lib.zip does not exist
                continue
            os_upload(
                os_client,
                f"{build_dir}/{artifact}",
                namespace,
                bucket,
                f"{root_path}/{build.version}/{artifact}"
            )

        # let's upload the job loader
        job_loader_filename = get_job_loader(self.config.get("oci_config"))

        os_upload(
            os_client,
            job_loader_filename,
            namespace,
            bucket,
            f"{root_path}/{build.version}/job_loader.py"
        )

        application = self.create_application(build.manifest, destination_location)
        app_info = {
            "application_id": application.id,
            "compartment_id": application.compartment_id
        }

        os_upload_json(
            os_client, app_info,
            namespace, bucket, f"{root_path}/{build.version}/deployment.json"
        )

        oci_config = self.config.get("oci_config")
        if oci_config is not None:
            os_upload(
                os_client,
                _save_json_temp(oci_config),
                namespace,
                bucket,
                "oci_config.json"
            )
            os_upload(
                os_client,
                get_filename(oci_config['key_file']),
                namespace,
                bucket,
                "oci_api_key.pem",
            )


