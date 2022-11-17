"""An AWS Python Pulumi program"""

import json
import pulumi
from pulumi_aws import s3

from pulumi_aws import rds
from pulumi_aws import batch
from pulumi_aws import ecs
from pulumi_aws import iam
from pulumi_aws import secretsmanager

### SETUP ###
config = pulumi.Config()
resource_base_name = config.require('base_name')
boostrap_action_path = config.require('boostrap_action_path')
boostrap_action_script = config.require('boostrap_action_script')
glue_job_path = config.require('glue_job_path')
db_name = config.require('db_name')
db_username = config.require_secret('db_user')
db_pwd = config.require('db_pwd')


### IAM ###



### SECRETS ###

secrets = secretsmanager.Secret(
    f'{resource_base_name}-demo-glue-dask-secrets-manager'
)

secretsmanager.SecretVersion(
    'DB_USERNAME',
    secret_id=secrets.id,
    secret_string=db_username,
)
secretsmanager.SecretVersion(
    'DB_PWD',
    secret_id=secrets.id,
    secret_string=db_pwd,
)
secretsmanager.SecretVersion(
    'DB_NAME',
    secret_id=secrets.id,
    secret_string=db_name,
)

### BUCKETS ###
data_storage = s3.BucketV2(
    f'{resource_base_name}-data-storage',
    bucket=f"{resource_base_name}-data-storage",
)
lib_storage = s3.BucketV2(
    f'{resource_base_name}-managed-scripts-and-lib',
    bucket=f"{resource_base_name}-managed-scripts-and-lib",
)

boostrap_action_file = s3.BucketObjectv2(
    f'{resource_base_name}-boostrap-action-scrip',
    bucket=lib_storage.id,
    source=pulumi.FileAsset(f"resources/{boostrap_action_script}"),
    key=f"{boostrap_action_path}/{boostrap_action_script}",
)
workflow = s3.BucketObjectv2(
    f'{resource_base_name}-glue-job-scrip',
    bucket=lib_storage.id,
    source=pulumi.FileAsset(glue_job_path),
    key="workflow/demo_dask_glue_job.py",
)

### RDS ###
rds.Cluster(
    f'{resource_base_name}_postgres-db',
    cluster_identifier=f'{resource_base_name}-postgres-db',
    engine=rds.EngineType.AURORA_POSTGRESQL,
    database_name="postgres",
    master_username=db_username,
    master_password=db_pwd,
    skip_final_snapshot=True,
)
