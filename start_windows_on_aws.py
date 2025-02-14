# Copyright (C) 2025 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Start windows VMs on AWS that are required for GSS TSIG tests."""

import argparse
import os
import sys
import boto3
import logging
from botocore.exceptions import ClientError

log = logging.getLogger(__name__)
logging.basicConfig(format='[WINDOWS ON AWS] %(asctime)-15s %(message)s', level=logging.INFO)

# def _get_win_addresses(vars, version):
#     vars[f'WIN_DNS_ADDR_{version}'] = ''
#     if os.path.exists(f'aws-win-ad-dns-vm{version}.txt'):
#         with open(f'aws-win-ad-dns-vm{version}.txt', 'r') as f:
#             for line in f.readlines():
#                 if line.startswith('ip-address='):
#                     vars[f'WIN_DNS_ADDR_{version}'] = line[11:].strip()
#                     log.info(f'extended forge configuration with WIN_DNS_ADDR_{version}=%s',
#                              vars[f'WIN_DNS_ADDR_{version}'])
#     else:
#         log.info(f"aws-win-ad-dns-vm{version}.txt not found! Tests for GSS TSIG and ACTIVE DIRECTORY won't work")
#     return vars



def _setup_win_ad_dns(ami, domain):
    if os.path.exists(f'aws-win-ad-dns-vm{domain[3:7]}.txt'):
        log.info(f"file aws-win-ad-dns-vm{domain[3:7]}.txt exists it's possible that vm is already running!")
        log.info("please check if that's correct and use terminate-instances before setting up new systems!")
        sys.exit()

    log.info('Start windows %s vm for gss-tsig testing', domain)
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
    log.info(f'Windows vm using domain {domain} and instance-id: {i.id}')
    return i


def _terminate_single_vm(instance):
    log.info(f'Terminating vm with id {instance.id} in progress..')
    try:
        instance.terminate()
        instance.wait_until_terminated()
    except ClientError as er:
        log.error(f'There was a problem with termination of {instance.id}: {er}.')
        return False
    log.info(f'AWS vm {instance.id} terminated.')
    return True


def terminate_instances():
    ec2 = boto3.resource('ec2', region_name='us-east-1')
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



def parse_args():
    description = """
    Start windows VMs on AWS that are required for GSS TSIG tests.
    """
    main_parser = argparse.ArgumentParser(description=description,
                                          formatter_class=argparse.RawDescriptionHelpFormatter)

    main_parser.add_argument('--start', action='store_true', help='Start windows VMs on AWS.')
    main_parser.add_argument('--id', default=None, help='Terminate AWS system with id, multiple ids can be passed separated by comma.')
    main_parser.add_argument('--terminate', action='store_true', help='Terminate all windows VMs on AWS saved in aws-win-ad-dns-vm*.txt files.')

    args, _ = main_parser.parse_known_args()
    return args


def main():
    args = parse_args()
    if args.start:
        win_vm_2016 = _setup_win_ad_dns('ami-06774e1cb71fbe789', 'win2016ad.aws.isc.org')
        win_vm_2019 = _setup_win_ad_dns('ami-06602a989923b1eba', 'win2019ad.aws.isc.org')

        for vm, version in zip([win_vm_2016, win_vm_2019], ['2016', '2019']):
            vm.wait_until_running()
            vm.reload()
            win_dns_addr = vm.private_ip_address
            with open(f'aws-win-ad-dns-vm{version}.txt', 'a') as f:
                f.write('ip-address=%s\n' % win_dns_addr)
            with open("init_all.py", 'a') as f:
                f.write(f'\nWIN_DNS_ADDR_{version}="{win_dns_addr}"\n')
            log.info('windows %s vm ip-address: %s' % (version, win_dns_addr))

    elif args.id:
        vms = args.id.split(",")
        for vm_id in vms:
            ec2 = boto3.resource('ec2', region_name='us-east-1')
            instance = ec2.Instance(vm_id)
            _terminate_single_vm(instance)

    elif args.terminate:
        terminate_instances()


if __name__ == "__main__":
    main()
