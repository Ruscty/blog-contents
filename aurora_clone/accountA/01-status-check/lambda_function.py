import json
import boto3

rds = boto3.client('rds')

# ステータスは「available」をチェック
# 引数指定したDBインスタンスのステータス情報取得
def get_describe_db_instances(instance_name):
    rds_info = rds.describe_db_instances(
        DBInstanceIdentifier=instance_name)
    status=rds_info['DBInstances'][0]['DBInstanceStatus']
    return status

def lambda_handler(event, context):
    status=get_describe_db_instances('cloned-instance')
    # StepFuncitonへの戻り値はjson 形式にする
    return {
        'status': status
    }