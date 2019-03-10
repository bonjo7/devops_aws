#!/usr/bin/env python3
import sys
import boto3
import time
ec2 = boto3.resource('ec2')

print('About to list all instances, please wait...')
time.sleep(1)
#List all instances for the user so they can decided which instance they  wish to terminate
for instance in ec2.instances.all():

    print ('Id: ', instance.id,  '\n   State: ', instance.state, '\n   Type: ', instance.instance_type, '\n **********')
    time.sleep(1) 

#Ask the user to enter instance id that they wish to delete
user_input_instance = input('Enter instance id that you wish to terminate: ')
time.sleep(1) 
print('Preparing to terminate instance, please wait....')
time.sleep(1) 

#Loop through all instances and deletes the instance that matches the user input
for instance_id in ec2.instances.all():
    try:
        instance = ec2.Instance(user_input_instance)
        response = instance.terminate()
        print ('Istance with ID: ', user_input_instance, ' has been terminated', '\n Review of termination \n\n\n' ,response)

    except Exception as error:
        print('Error terminating instance, please try again', '\n', str(error))      
