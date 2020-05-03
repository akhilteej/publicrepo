import json
import os
import boto3
import datetime

client = boto3.client('rds')
start_date = str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
region = os.getenv("region")
def lambda_handler(event, context):
    dbs = json.loads(os.getenv("dbs"))
    for db in dbs:
        print(db)
        createdbsnapshot = client.create_db_snapshot(DBSnapshotIdentifier='lambdasnapshot-'+db+'-'+start_date,DBInstanceIdentifier=db)
        print(createdbsnapshot)
        describingdbsnapshot = client.describe_db_snapshots(DBInstanceIdentifier='inspired')
        print(describingdbsnapshot)
