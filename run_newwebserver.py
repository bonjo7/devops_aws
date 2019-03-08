#!/usr/bin/env python3

#Import configuration file for security settings
import aws_config

#Import boto3
import boto3

#Import subprocess
import subprocess

#Creating colour class in order to change text colour
class bcolors:
    
    OKBLUE = '\033[94m' #Blue
    OKGREEN = '\033[92m' #Green
    WARNING = '\033[93m' #Yellow
    FAIL = '\033[91m' #Red
    ENDC = '\033[0m' #white to revert back to white colour

#Using try exception to ensure the user is notifed if the instance created or not
try:
    #Create varibale ec2, setting the resource as ec2 and the region as Ireland
    ec2 = boto3.resource('ec2', region_name='eu-west-1')

    tagValue = input(bcolors.OKBLUE + 'Enter instance name: ' + bcolors.ENDC)    

    #Create a vaiable instance which will use the boto create_instance method
    #Too create the new instance
    instance = ec2.create_instances(

        #Image id is the id for an Amazon Linux 2 AMI
        ImageId='ami-0fad7378adf284ce0',

        #Setting min and max volume to 1 as I will only be using one instance
        MinCount=1,
        MaxCount=1,

        #Using my assignment key which I previously created on aws console and downloaded
        #If I wished to create a new key I could have used the code which is commented out
        #At the top of this script
        KeyName='Assignment_key',

        #Using t2.micro type as it is free tier eligible    
        InstanceType='t2.micro',

        #Using the following security group which I created during one of the first lads
        SecurityGroupIds=[
            aws_config.AWS_CONFIG['security'],
        ],
        

        #Creating user data script to use the apporaite web server, ngnix
        UserData='#!/bin/bash\n' \
                 'yum update -y\n' \
                 'yum install python37 -y\n' \
                 'yum install httpd -y\n' \
                 'systemctl enable httpd\n' \
                 'systemctl start httpd\n'\
                 'echo "<h2>Bernards Assignment Page</h2>Instance ID: " > /var/www/html/index.html\n' \
                 'curl --silent http://169.254.169.254/latest/meta-data/instance-id/ >> /var/www/html/index.html\n' \
                 'echo "<br>Availability zone: " >> /var/www/html/index.html\n' \
                 'curl --silent http://169.254.169.254/latest/meta-data/placement/availability-zone/ >> /var/www/html/index.html\n' \
                 'echo "<br>IP address: " >> /var/www/html/index.html\n' \
                 'curl --silent http://169.254.169.254/latest/meta-data/public-ipv4 >> /var/www/html/index.html\n' \
                 'echo "<hr>Here is an image that I have stored on my S3: <br>" >> /var/www/html/index.html\n',

        #Setting the tags for my instance   
         
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': tagValue
                    },
                ]
            },
        ]
    ) 
except Exception as error:
    print(bcolors.FAIL + "Instance did not create: ID of the instance is:  ", instance[0].id, ". " + str(error) + bcolors.ENDC)


print(bcolors.WARNING + "Your instance is now initializing, please wait...." + bcolors.ENDC)

instance[0].wait_until_running('Instance running')
instance[0].reload()

#Setting the ip as avarible so the varibale name can be used to ssh into instance
global instanceIP
instanceIP = instance[0].public_ip_address
#If all goes well the following should be printed at the command line
print (bcolors.OKGREEN + "The following instanace with ID: ", instance[0].id, ", has been created and is running.\nName of the instance: ", tagValue, "\nThe public ip address is: ", instanceIP + "\n\n" + bcolors.ENDC)

#Write the instance ip to a file which I will call in the create bucket script to SSH into to push the bucket image to the index page
file_instanceIP = open("instanceID.txt", "w")
file_instanceIP.write(instanceIP)

print(bcolors.WARNING + 'Checking to see if instance is running... please wait' + bcolors.ENDC)

permission = "chmod 700 check_webserver.py"
print(permission) 

subprocess.call(permission, check = True, shell = True)

cmd_check = "scp -i Assignment_key.pem check_webserver.py ec2-user@" + instanceIP + ":."

print(cmd_check)

subprocess.call(cmd_check, check=True, shell=True)

