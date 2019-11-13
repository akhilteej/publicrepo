####################################################################################
#   AWS Lambda function which deletes Images which has creation date older than
#   retention date.
#
#
####################################################################################
import boto3
import datetime
import os

retention = int(os.getenv("retention"))
region = os.getenv("region")
start_date = str(datetime.datetime.now() - datetime.timedelta(days = retention))[:10]


EC2 =  boto3.client('ec2',region)

def delete_image(imageID):
    SnapDesc= "*"+imageID+"*"
    myAccount = boto3.client('sts').get_caller_identity()['Account']
    snapshots = EC2.describe_snapshots(Filters=[{'Name': 'description','Values': [SnapDesc,]},],MaxResults=10000, OwnerIds=[myAccount])['Snapshots']
    print("Deregistering image " + imageID)
    amiResponse = EC2.deregister_image(DryRun=False,ImageId=imageID,)
    for snapshot in snapshots:
        if snapshot['Description'].find(imageID) > 0:
            snapResonse = EC2.delete_snapshot(SnapshotId=snapshot['SnapshotId'])
            print("Deleting snapshot " + snapshot['SnapshotId'])
    print("------------------------------------------")

def lambda_handler(event, context):
    
    AMIsName= "Lambda for *"
    count=0
    images = EC2.describe_images(Filters=[{'Name': 'name','Values': [AMIsName,]},],DryRun=False)['Images']
    print("             "+start_date+"                 ")
    print("------------------------------------------")
    for image in images:
        if start_date >= image['CreationDate'][:10]:
            count = count + 1
            print(image['ImageId']+" "+image['State']+ " "+image['CreationDate'][:10])
            delete_image(image['ImageId'])
    
