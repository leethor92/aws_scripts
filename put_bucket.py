#!/usr/bin/env python3
import sys
import boto3
import os

s3 = boto3.resource("s3")

#Function to upload file to bucket
def put_bucket():
    #prints list of buckets
    for bucket in s3.buckets.all():
      print ('\nList of buckets:')
      print (bucket.name)
    #user prompted to enter bucket name they wish to upload a file to
    bucket = input('\nPlease type in the name of the bucket you wish to upload to: ')
    #User is prompted to define file name they wish to upload
    file = input('Please type in the file you wish to upload to ' + bucket + ': ')
    #upload file to specified bucket
    try:
      response = s3.Object(bucket, file).put(Body=open(file, 'rb'))
      print ("\nFile has been uploaded successfully")

    except Exception as error:
        print (error)
    #added read only access so image can be displayed
    try:
       object_acl = s3.ObjectAcl(bucket, file).put(ACL='public-read')
       print ('\nAdded Public Read Only Access to ' + file)
    except Exception as error:
        print (error)

def main():
    put_bucket()


if __name__ == '__main__':
    main()
