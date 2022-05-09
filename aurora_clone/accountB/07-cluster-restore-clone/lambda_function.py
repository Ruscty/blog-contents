import json
import boto3
client = boto3.client('rds')

def lambda_handler(event, context):
    
    # スナップショット復元　クラスター
    response = client.restore_db_cluster_from_snapshot(
        AvailabilityZones=[
            'ap-northeast-1a',
        ],
        DBClusterIdentifier='restore-cluster', #任意の名前
        SnapshotIdentifier='arn:aws:rds:ap-northeast-1:[ACCOUNTB]:cluster-snapshot:cloned-snapshot', #対象スナップショットのARN
        Engine='aurora-postgresql',
        EngineVersion='13.4',
        DBSubnetGroupName='restore-subnet-group',
        DatabaseName='test_table',
        KmsKeyId='[KMSKEYID]', #アカウントBの任意KMSキー
    ),
    # スナップショット復元　インスタンス
    response = client.create_db_instance(
        DBClusterIdentifier='restore-cluster', #クラスタ名を指定
        Engine='aurora-postgresql', #ソースと同じエンジンを指定
        DBInstanceIdentifier='restore-instance', #任意のインスタンス名を指定
        DBInstanceClass='db.r6g.large' #任意のインスタンスサイズを指定
    )
    
    # 待機処理は最後の処理のため不要としている

    return {
        'statusCode': 200,
        'body': json.dumps('success!')
    }