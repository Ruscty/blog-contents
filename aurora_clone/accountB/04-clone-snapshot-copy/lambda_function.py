import json
import boto3
client = boto3.client('rds')

def lambda_handler(event, context):
    
    # 共有スナップショットコピー(KMSキーをアカウントBのものに切り替え)
    response = client.copy_db_cluster_snapshot(
        SourceDBClusterSnapshotIdentifier='arn:aws:rds:ap-northeast-1:[ACCOUNTA]:cluster-snapshot:copied-cloned-snapshot',
        TargetDBClusterSnapshotIdentifier='cloned-snapshot',
        KmsKeyId='[KMSKEYID]', #アカウントBの任意KMSキー
        SourceRegion='ap-northeast-1'
    )
    
    # 待機処理
    waiter = client.get_waiter('db_cluster_snapshot_available')
    waiter.wait(
        DBClusterSnapshotIdentifier='cloned-snapshot',
        SnapshotType='manual'
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('success!')
    }