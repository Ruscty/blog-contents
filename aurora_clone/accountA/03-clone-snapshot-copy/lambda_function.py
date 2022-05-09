import json
import boto3

client = boto3.client('rds')

def lambda_handler(event, context):
    
    # スナップショットコピー
    response = client.copy_db_cluster_snapshot(
        SourceDBClusterSnapshotIdentifier='arn:aws:rds:ap-northeast-1:[ACCOUNTA]:cluster-snapshot:cloned-snapshot',
        TargetDBClusterSnapshotIdentifier='copied-cloned-snapshot',
        KmsKeyId='[KMSKEYID]', #アカウントAのDB暗号化に使用しているものと別のKMSキー(クロスアカウント用)
        SourceRegion='ap-northeast-1'
    )
    
    # 待機処理
    waiter = client.get_waiter('db_cluster_snapshot_available')
    waiter.wait(
        DBClusterSnapshotIdentifier='copied-clone-snapshot',
        SnapshotType='manual'
    )

    # スナップショット共有
    client.modify_db_cluster_snapshot_attribute(
        DBClusterSnapshotIdentifier='arn:aws:rds:ap-northeast-1:[ACCOUNTA]:cluster-snapshot:copied-cloned-snapshot',
        AttributeName='restore',
        ValuesToAdd=[
            '[ACCOUNTB]',
        ]
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('success!')
    }