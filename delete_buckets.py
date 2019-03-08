#!/usr/bin/env python3
import sys
import boto3
import time
s3 = boto3.resource('s3')

print('Listing all buckets...')

#List all buckets to the user
for bucket in s3.buckets.all():
  try:
    print (bucket.name)
    print ("---")
    for item in bucket.objects.all():
        print ("\t%s" % item.key)
  except Exception as error:
    print('This file is not accessable')

#Allow a slight pause in the program
time.sleep(2) 

#Request the user to input the name of the cucket that they wish to delete
user_input_deleteBucket = input('Enter bucket name that you wish to delete: ')  
print('Attempting to delete, please wait...')  

#Allow a slight pause in the program
time.sleep(1)

#For all the buckets delete the bucket with the matching name from the user input
for bucket_name in s3.buckets.all():
    bucket = s3.Bucket(user_input_deleteBucket)
time.sleep(2)  

#If delete was successful inform the user if not ask them to try again
try:
    bucket.objects.all().delete()
    response = bucket.delete()
    print ('Bucket with name: ', user_input_deleteBucket, ' has been deleted', '\n Full details of bucket deleted are : ', response)
except Exception as error:
    print('Error deleting bucket, try again', '\n', str(error))
    
