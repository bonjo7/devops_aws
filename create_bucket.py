#!/usr/bin/env python3
import time
import sys
import boto3
import subprocess

s3 = boto3.resource("s3")

file_instanceIP = open("instanceID.txt", "r")

global instanceIP

instanceIP = file_instanceIP.read()

#Function which will list existing buckets to the users
def list_buckets():

  for bucket in s3.buckets.all():

    try:
      print (bucket.name)
      print ("---")

      for item in bucket.objects.all():
          print ("\t%s" % item.key)

    except Exception as error:
      print('This file is not accessable', str(error))

#Function to allow the user to create a bucket
def create_bucket():

  try:
    global bucket_name
    bucket_name = input('Enter bucket name: ')

    response = s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'}, ACL='public-read')
    
    print ('Bucket successfully created, bucket name = ', bucket_name)

  except:
      
    print('Bucket name', bucket_name, 'not entered and bucket not created') 
    print('Please try a different name')       

#Upload an image to the newly created or already created buckets
def upload_image():

  global image_name
  image_name = input('Enter the image name, please include the file extension eg. .jpg .png .txt etc....: ')
  try:
    response = s3.Object(bucket_name, image_name).put(Body=open(image_name, 'rb'), ACL='public-read')
    
    print('Image successfully uploaded: ', response)

    #Creating variables to stings which will be used to push image to the index page
    
    #ssh to set path, permissions to change the permissions of the index file located at var/www/html
    ssh = "ssh -t -o StrictHostKeyChecking=no -i Assignment_key.pem ec2-user@"
    permissions = " 'sudo chmod 777 /var/www/html/index.html'"
    #Command to ssh into instance, ip pulled from text file and change permissions of index
    ssh_string = ssh + instanceIP + permissions
    print(ssh_string)
    subprocess.call(ssh_string, shell=True)
    
    #Allowing some time to ensure commands are exectuded
    time.sleep(2)

    #command to be used to append the index file with the image from the newlt formed bucket
    command_string = ssh + instanceIP + ' \'sudo echo "<img src=https://s3-eu-west-1.amazonaws.com/' + bucket_name + '/' + image_name + '>" >> /var/www/html/index.html\''
    #Command to push image in bucket to index.html of the running instance
    print(command_string) 
    subprocess.call(command_string, shell=True)

  except Exception as error:
    print('Error uploading image', '\n', str(error))


#Function which will run the output and above functions to the user
def run_bucket_functions():

  print('\n You are about to create a new bucket')

  time.sleep(2)

  print('\n Before creating a new bucket here are the buckets that currently exist')

  time.sleep(2)

  list_buckets()

  time.sleep(2)

  print('\n Your bucket name must be unique')

  create_bucket()

  time.sleep(2)

  print('\n Upload an image to your newly created bucket')
  upload_image()

#RUn the run_bucket_functions function
run_bucket_functions()  



