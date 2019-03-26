#!/usr/bin/env python3


import boto3
import subprocess
import config
import time

#Declare an ec2 variable & S3 variable
ec2 = boto3.resource('ec2')
s3 = boto3.resource('s3')

#function to create an instact
def create_instance():
  #user is prompted to enter an instance name to serve as a tag
  #tag is used in below API call in instace creation
  instanceName=input('Please enter your instance name: ')
  tags=[{'Key': 'Name', 'Value': instanceName}]
  tag_instance=[{'ResourceType': 'instance', 'Tags': tags}]

  #try/except catch block to prevent crashing 
  try:
    instance = ec2.create_instances(
      ImageId='ami-0fad7378adf284ce0',
      MinCount=1,
      MaxCount=1,
      InstanceType='t2.micro',
      TagSpecifications=tag_instance,
      KeyName=config.aws_key,
      SecurityGroupIds=config.aws_security_group,
      UserData='''#!/bin/bash
                  yum -y update
                  yum -y install python37
                  yum -y install httpd
                  systemctl enable httpd
                  systemctl start httpd
                  touch home/ec2-user/testFile''')

    #instance ID & IP address is printed to the console
    print("your instance:", instance[0].id ,"has succesfully been created")
    time.sleep(5)
    instance[0].reload()
    print("instance public IP address is:", instance[0].public_ip_address)
    time.sleep(60)

    #SCP check_webserver.py file to instance to retreive status
    cmd_scp="scp -i " + config.aws_key + ".pem check_webserver.py ec2-user@" + instance[0].public_ip_address + ":."
    subprocess.run(cmd_scp, shell=True)
    #make check_webserver.py file executable
    cmd="ssh -o StrictHostKeyChecking=no -i " + config.aws_key + ".pem ec2-user@" + instance[0].public_ip_address + " 'chmod 700 check_webserver.py'"
    subprocess.run(cmd, shell=True)
    #run the check_webserver.py file to get status
    chk_cmd="ssh -i " + config.aws_key + ".pem ec2-user@" + instance.public_ip_address + " 'python3 check_webserver.py'"
    subprocess.run(chk_cmd, shell=True)
    
  #Exception block to prevent script crashing
  except Exception as error:
        print (error)

#main function defined
def main():
  create_instance()
# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()

