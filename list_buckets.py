#!/usr/bin/env python3
import boto3

#Creating colour class in order to change text colour
class bcolors:
    
    OKBLUE = '\033[94m' #Blue
    OKGREEN = '\033[92m' #Green
    WARNING = '\033[93m' #Yellow
    FAIL = '\033[91m' #Red
    ENDC = '\033[0m' #white to revert back to white colour

s3 = boto3.resource('s3')

#List all the buckets to the user
for bucket in s3.buckets.all():
  try:
    print (bcolors.OKGREEN + bucket.name + bcolors.ENDC)
    print ("----------")
    for item in bucket.objects.all():
        print ("\t%s" % item.key)
          
  #Handle the files that are not accessable        
  except Exception as error:
    print(bcolors.WARNING + 'This file is not accessable\n' + bcolors.ENDC)

 