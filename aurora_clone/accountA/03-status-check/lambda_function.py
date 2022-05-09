import json
import boto3

rds = boto3.client('rds')

# 引数指定したDBインスタンスのステータス情報取得
# 引数: snapshot フィルタリングに使用
def get_describe_db_cluster_snapshot(snapshot,snapshot_type):
    rds_info = rds.describe_db_cluster_snapshots(
        DBClusterSnapshotIdentifier=snapshot,
        SnapshotType=snapshot_type)
    status=rds_info['DBClusterSnapshots'][0]['Status']
    return status

def lambda_handler(event, context):
    status=get_describe_db_cluster_snapshot('copied-cloned-snapshot','manual')
    # StepFuncitonへの戻り値はjson 形式にする
    return {
        'status': status
    }