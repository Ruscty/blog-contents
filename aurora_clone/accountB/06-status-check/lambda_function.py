import json
import boto3

rds = boto3.client('rds')

# ステータスは「deleting」をチェック
# 引数指定したDBインスタンスのステータス情報取得
def get_describe_db_clusters(cluster_name):
    rds_info = rds.describe_db_clusters(
        DBClusterIdentifier=cluster_name)
    status=rds_info['DBClusters'][0]['Status']
    return status

def lambda_handler(event, context):
    status=get_describe_db_clusters('evacuation-cluster')
    # StepFuncitonへの戻り値はjson 形式にする
    return {
        'status': status
    }