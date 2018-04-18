'''
blame: chrijust
language: python
purpose: get some net info from an ami

Changelog:
17 March 2016: 
    Edit getNetInfo() to change how the dictionaries are defined
    Write getInstanceInfo() to grab instance metadata
    JSONified output, and made it super pretty.
'''

import psutil
import json
import datetime 
import urllib2
import subprocess
import json
import parser

def getNetInfo():
    netInfo = []
    for proc in psutil.process_iter():
        try:
            #get the current running processes as a dictionary, and then get the connections
            pinfo = proc.as_dict()
            pnet = psutil.Process(pinfo['pid']).connections()
        except psutil.NoSuchProcess:
            pass
        else:
            if (pinfo['exe'] and pnet and pnet[0][5] in ('ESTABLISHED', 'LISTEN')):

                datestart = datetime.datetime.fromtimestamp(proc.create_time()).strftime("%Y-%m-%d %H:%M:%S")

                currDict = {}
                currDict['name'] = pinfo['name']
                currDict['cmd_path'] = pinfo['exe']
                currDict['cmd_line'] = pinfo['cmdline']
                currDict['started'] = datestart
                currDict['status'] = pnet[0][5] 
                currDict['laddr'] = pnet[0][3]

                if (pnet[0][4]):
                    currDict['raddr']=pnet[0][4] 

                netInfo.append(currDict)
    return netInfo 

def getInstanceInfo():
    instanceInfo = {}
    try:    
        amiID = urllib2.urlopen("http://169.254.169.254/latest/meta-data/ami-id").read()
    except urllib2.HTTPError:
        amiID="Not Found, this shouldn't be possible"
    try:
        pubIP = urllib2.urlopen("http://169.254.169.254/latest/meta-data/public-ipv4").read()
    except urllib2.HTTPError:
        pubIP = "Not Found, are you in a VPC?" 
    try:
        instanceID = urllib2.urlopen("http://169.254.169.254/latest/meta-data/instance-id").read()
    except urllib2.HTTPError:
        instanceID = "No Instance ID Found"

    instanceInfo = {
        'ami_id':amiID,
        'ami_instance_id':instanceID,
        'ami_ip':pubIP
       }
    return instanceInfo 

def sshInfo():
    #I don't know if I'll be using this function. It might be easier to parse the info 
    #   when I connect. It might also be possible to just ssh localhost to get stuff.
    #   Again, this one's up in the air.
    pass

def launchInstances(instanceList):
    #I don't know if I'll be using this function either. This is a placeholder
    #   for where my instance launching logic will go.
    pass

def main():
    #make a new file for our stuff
    filename = "/var/log/ami_info_"+getInstanceInfo()['ami_id']+".json"
    f = open (filename,'w')
    
    #statically define configFile as /etc/ssh/sshd_config for now. POC.
    configFile = "/etc/ssh/sshd_config"
    
    amiData = {
        'ami_id':getInstanceInfo()['ami_id'], 
        'networking_pids':getNetInfo(), 
        'service_config':parser.parseFile(configFile)
    }

    j = json.dumps(amiData, indent=4, sort_keys=True)
    f.write(j)
    f.close()
    #proc = subprocess.Popen(["cat", "/var/log/ami_info.json"])
main()
