#!/usr/bin/env python3
import boto3
ec2 = boto3.resource('ec2')

#List instances by their id, state and instance type
for instance in ec2.instances.all():
    try:
        print ('Id: ', instance.id,  '\n   State: ', instance.state, '\n   Type: ', instance.instance_type, '\n **********', instance.public_ip_address)
    except Exception as error:
        print ('Error listing instances \n', str(error))


