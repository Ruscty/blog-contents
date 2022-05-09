import json
import boto3
client = boto3.client('rds')

def lambda_handler(event, context):
    # クラスター(インスタンス)削除処理
    response = client.delete_db_instance(
        DBInstanceIdentifier='evacuation-instance',
        SkipFinalSnapshot=True,
        DeleteAutomatedBackups=True
    ),
    response = client.delete_db_cluster(
        DBClusterIdentifier='evacuation-cluster',
        SkipFinalSnapshot=True,
    )

    # クラスター(インスタンス)削除完了待機処理
    waiter = client.get_waiter('db_instance_deleted')
    waiter.wait(
        DBInstanceIdentifier = 'evacuation-instance',
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('aurora db cluster delete success!')
    }