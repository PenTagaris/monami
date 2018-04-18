#!/apollo/env/SDETools/bin/python
#import boto
import boto3
import time

#amiId = 'ami-8fcee4e5'
vpcId = 'vpc-6fcce10b'
snId = 'subnet-c5d87def'
instType = 't2.micro'
sgId = 'sg-988624e0'
fileLoc = 'ami-list.txt'
kn = 'AMI_ISO'
ud="""#!/bin/bash
sleep 60
touch /tmp/stage1
curl 10.0.1.194/monami > /tmp/monami
chmod +x /tmp/monami
/tmp/monami > /tmp/monamilog 2>&1 
for i in /var/log/ami_info_*; do curl -X POST -F file=@$i http://10.0.1.194:8000; done
shutdown -h now"""

#ec2 = boto3.resource('ec2')
f = open(fileLoc)
for amiId  in f:
    #ec2 = boto3.resource('ec2')
    amiId = str(amiId).strip()
    print "Launching AMI ID ",amiId,"with the following user data: \n",ud 
    #start up some instances
    instance =  boto3.resource('ec2').create_instances(ImageId = amiId, 
                MinCount = 1, 
                MaxCount = 1, 
                KeyName = kn,
                SubnetId = snId,
                SecurityGroupIds = [sgId],
                InstanceInitiatedShutdownBehavior='terminate',
                InstanceType = instType, 
                UserData = ud)
