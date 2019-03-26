#!/usr/bin/env python3
import boto3
ec2 = boto3.resource('ec2')
tag_instance = {"Key": "Name", "Value": "Tagged"}

instance = ec2.create_instances(
    ImageId='ami-0fad7378adf284ce0',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    SecurityGroupIds=['Web traffic'],
    KeyName="lee_key",
    TagSpecifications=[{'ResourceType': 'instance', 'Tags': [tag_instance]}])[0],
print (instance[0].id)
