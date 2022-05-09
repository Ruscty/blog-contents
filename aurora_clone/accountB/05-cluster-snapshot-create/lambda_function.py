import json
import boto3

client = boto3.client('rds')

def lambda_handler(event, context):
    
    # スナップショット作成処理
    client.create_db_cluster_snapshot(
        DBClusterSnapshotIdentifier='evacuation-cluster-snapshot',
        DBClusterIdentifier='evacuation-cluster'
    ),
    
    # スナップショット作成処理完了待機処理
    waiter = client.get_waiter('db_cluster_snapshot_available')
    waiter.wait(
        DBClusterIdentifier = 'evacuation-cluster',
        DBClusterSnapshotIdentifier='evacuation-cluster-snapshot',
        SnapshotType='manual'
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('snapshot create success!')
    }