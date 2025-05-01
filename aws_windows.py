import boto3
import os
import sys
import logging
from botocore.exceptions import ClientError

log = logging.getLogger(__name__)


def _setup_win_ad_dns(ami, domain):
    """Strictly for AWS testing, this will start vm based on ami. Use _terminate_instances to
    terminate started systems, simple check is included to prevent starting multiple windows
    system
    @param ami: ami of vm template
    @param domain: windows domain
    @return: boto3 Instance
    """
    if os.path.exists(f'aws-win-ad-dns-vm{domain[3:7]}.txt'):
        log.info(f"file aws-win-ad-dns-vm{domain[3:7]}.txt exists it's possible that vm is already running!")
        log.info("please check if that's correct and use terminate-instances before setting up new systems!")
        sys.exit()
    
    log.info('creating windows vm for gss-tsig testing')
    ec2 = boto3.resource('ec2', region_name='us-east-1')
    init_script = """
<powershell>
shutdown /s /t 25200
</powershell>
<persist>true</persist>
    """
    params = dict(MaxCount=1,  # pylint: disable=use-dict-literal
                  MinCount=1,
                  InstanceType='t3a.small',
                  ImageId=ami,
                  SubnetId='subnet-0efca44a30c0a40c0',
                  KeyName='jenkins-ec2',
                  SecurityGroupIds=['sg-04a74236a5389e87f'],  # DomainController
                  TagSpecifications=[{'ResourceType': 'instance', 'Tags': [
                      {'Key': 'isc:purpose', 'Value': 'forge-testing'},
                      {'Key': 'isc:owner', 'Value': 'jenkins-ec2'},
                      {'Key': 'isc:group', 'Value': 'kea'},
                      {'Key': 'isc:provisioning', 'Value': 'python-api'},
                      {'Key': 'isc:access', 'Value': 'private'},
                      {'Key': 'isc:contact', 'Value': 'qa@isc.org'},
                      {'Key': 'Name', 'Value': f'j-windows-{domain[3:7]}-forge-testing'}
                  ]}],
                  InstanceInitiatedShutdownBehavior='terminate',
                  UserData=init_script)

    i = list(ec2.create_instances(**params))[0]
    with open(f'aws-win-ad-dns-vm{domain[3:7]}.txt', 'w') as f:
        f.write(f'instance-id={i.id}\n')
        f.write(f'domain={domain}\n')
    log.info(f'windows vm using domain {domain} and instance-id: {i.id}')
    return i

def _get_win_addresses(vars, version):
    """
    Update forge configuration with ip addresses of windows systems
    :param vars: string, include entire forge configuration
    :param version: string, contain release year of windows systems, in our setup it's 2016 or 2019
    :return: string, updated forge configuration
    """
    vars[f'WIN_DNS_ADDR_{version}'] = ''
    if os.path.exists(f'aws-win-ad-dns-vm{version}.txt'):
        with open(f'aws-win-ad-dns-vm{version}.txt', 'r') as f:
            for line in f.readlines():
                if line.startswith('ip-address='):
                    vars[f'WIN_DNS_ADDR_{version}'] = line[11:].strip()
                    log.info(f'extended forge configuration with WIN_DNS_ADDR_{version}=%s',
                             vars[f'WIN_DNS_ADDR_{version}'])
    else:
        log.info(f"aws-win-ad-dns-vm{version}.txt not found! Tests for GSS TSIG and ACTIVE DIRECTORY won't work")
    return vars

def _terminate_single_vm(instance):
    """
    terminate single vm in AWS
    @param instance: instance class to be terminated
    @return: True if termination was successful
    """
    log.info(f'>>>>> Terminating vm with id {instance.id} in progress..')
    try:
        instance.terminate()
        instance.wait_until_terminated()
    except ClientError as er:
        log.error(f'>>>>> There was a problem with termination of {instance.id}: {er}.')
        return False
    log.info(f'>>>>> AWS vm {instance.id} terminated.')
    return True


def _terminate_instances(args):
    """Strictly for AWS testing, this will terminate previously started vms by ./forge setup --win-gss-tsig
    """
    ec2 = boto3.resource('ec2', region_name='us-east-1')
    if args.id is not None:
        vms = args.id.split(",")
        for vm_id in vms:
            instance = ec2.Instance(vm_id)
            _terminate_single_vm(instance)
    else:
        for i in ("2016", "2019"):
            if os.path.exists(f'aws-win-ad-dns-vm{i}.txt'):
                termination = []
                with open(f'aws-win-ad-dns-vm{i}.txt', 'r') as f:
                    for line in f.readlines():
                        if line.startswith('instance-id='):
                            vm_id = line[12:].strip()
                            instance = ec2.Instance(vm_id)
                            termination.append(_terminate_single_vm(instance))
                if all(termination):
                    os.rename(f'aws-win-ad-dns-vm{i}.txt', f'aws-win-ad-dns-vm{i}_terminated.txt')
            else:
                log.info(f'aws-win-ad-dns-vm{i}.txt not found, looks like systems were not started!')

