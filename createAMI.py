####################################################################################
#   AWS Lambda function which creates Images for instances which has "backup" as 
#   tag or instances mentioned in environment varibles
#
#
####################################################################################
import json
import os
import boto3
import datetime

start_date = str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
region = os.getenv("region")
client = boto3.client('ec2','us-west-2')

def lambda_handler(event, context):
    instanceids = []
    if os.getenv('instances') == 'backup':
        
        reservations = client.describe_instances( Filters=[{ 'Name': 'tag-key', 'Values': ['backup',]},], DryRun=False).get('Reservations', [])
        instances = sum([[i for i in r['Instances']]for r in reservations], [])
        for instance in instances:
            instanceids.append(instance['InstanceId'])
    else:
        instanceids = json.loads(os.getenv("instances"))
    #print(start_date)
    for instanceid in instanceids:
        name= "Lambda for "+instanceid+" from "+start_date
        description= "AMI for "+instanceid+" created by lambda"
        image = client.create_image(Description=description,DryRun=False, InstanceId=instanceid, Name=name, NoReboot=True)
        print(image['ImageId'])
