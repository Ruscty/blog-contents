import json
import boto3

client = boto3.client('rds')
sts_client = boto3.client("sts")

def lambda_handler(event, context):
    # DBクラスター作成処理
    response = client.restore_db_cluster_to_point_in_time(
        DBClusterIdentifier = 'cloned-cluster', #任意のクラスタ名を指定
        RestoreType='copy-on-write', 
        SourceDBClusterIdentifier="arn:aws:rds:ap-northeast-1:[ACCOUNTA]:cluster:[AURORA_DBCLUSTER_NAME]", #ソースのクラスタのARN指定
        DBSubnetGroupName = 'clone-subnet-group', #指定しているDBサブネットグループ
        UseLatestRestorableTime= True,
        KmsKeyId='arn:aws:kms:ap-northeast-1:[ACCOUNTA]:key/xxxxxxxxxxxxx'
    ),
    
    # DBインスタンス作成処理
    response = client.create_db_instance(
        DBClusterIdentifier = 'cloned-cluster', #クローン作成したクラスタ名を指定
        Engine = 'aurora-postgresql', #ソースと同じエンジンを指定
        DBInstanceIdentifier = 'cloned-instance', #任意のインスタンス名を指定
        DBInstanceClass = 'db.r6g.large', #任意のインスタンスサイズを指定
        StorageEncrypted=True,
    ),
    
    # DBインスタンス作成処理完了待機処理
    waiter = client.get_waiter('db_instance_available')
    waiter.wait(
        DBInstanceIdentifier = 'cloned-instance',
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('aurora clone Success!')
    }