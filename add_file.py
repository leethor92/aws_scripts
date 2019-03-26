#!/usr/bin/env python3
import boto3
import subprocess
import config

s3 = boto3.resource('s3')
ec2 = boto3.resource('ec2')

def add_file():
    for bucket in s3.buckets.all():
      try:
        print (bucket.name)
     
        for item in bucket.objects.all():
          print ("\t%s" % item.key)

      except Exception as error:
        print('This file is not accessable', str(error))

    bucket = input('\nPlease type in the name of the bucket you wish to choose a file from: ')
    file = input('\nPlease type in the name of the file you wish to copy to the Index page: ')
    file_url = "https://s3-eu-west-1.amazonaws.com/" + bucket + "/" + file

    running_instances = ec2.instances.filter(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running']}])
    try:
        for instance in running_instances:
          print (instance.id, instance.state, instance.public_ip_address)

        cmd = " 'echo \"<img src=" + file_url + " />\" | sudo tee -a  /var/www/html/index.html' "
        index= "ssh -i " + config.aws_key + ".pem ec2-user@" + instance.public_ip_address + ' ' + cmd

        subprocess.run(index, shell=True)

    except Exception as error:
        print (error)

def main():
    add_file()


if __name__ == '__main__':
    main()

