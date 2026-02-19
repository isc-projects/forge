# Copyright (C) 2025-2026 Internet Systems Consortium, Inc. ("ISC")
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Start windows VMs on AWS that are required for GSS TSIG tests."""

import argparse
import os
import sys
import logging
import boto3
from botocore.exceptions import ClientError

log = logging.getLogger(__name__)
logging.basicConfig(format='[WINDOWS ON AWS] %(asctime)-15s %(message)s', level=logging.INFO)


def _setup_win_ad_dns(ami, domain):
    """Start windows node with preconfigured AD and DNS on AWS.

    :param ami: string with AMI id
    :type ami: str
    :param domain: string with domain name
    :type domain: str
    :return: instance object
    :rtype: boto3.resources.factory.ec2.Instance
    """
    if os.path.exists(f'aws-win-ad-dns-vm{domain[3:7]}.txt'):
        log.info("file aws-win-ad-dns-vm%s.txt exists it's possible that vm is already running!", domain[3:7])
        log.info("please check if that's correct and use --terminate before setting up new systems!")
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
    with open(f'aws-win-ad-dns-vm{domain[3:7]}.txt', 'w', encoding='utf-8') as f:
        f.write(f'instance-id={i.id}\n')
        f.write(f'domain={domain}\n')
    log.info('Windows vm using domain %s and instance-id: %s', domain, i.id)
    return i


def _terminate_single_vm(instance):
    """Terminate single vm on AWS.

    :param instance: instance object
    :type instance: boto3.resources.factory.ec2.Instance
    :return: True if vm was terminated, False otherwise
    :rtype: bool
    """
    log.info('Terminating vm with id %s in progress..', instance.id)
    try:
        instance.terminate()
        instance.wait_until_terminated()
    except ClientError as er:
        log.error('There was a problem with termination of %s: %s.', instance.id, er)
        return False
    log.info('AWS vm %s terminated.', instance.id)
    return True


def terminate_instances():
    """Terminate all windows VMs on AWS saved in aws-win-ad-dns-vm*.txt files."""
    ec2 = boto3.resource('ec2', region_name='us-east-1')
    for i in ("2016", "2019"):
        if os.path.exists(f'aws-win-ad-dns-vm{i}.txt'):
            termination = []
            with open(f'aws-win-ad-dns-vm{i}.txt', 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    if line.startswith('instance-id='):
                        vm_id = line[12:].strip()
                        instance = ec2.Instance(vm_id)
                        termination.append(_terminate_single_vm(instance))
            if all(termination):
                os.rename(f'aws-win-ad-dns-vm{i}.txt', f'aws-win-ad-dns-vm{i}_terminated.txt')
        else:
            log.info('aws-win-ad-dns-vm%s.txt not found, looks like systems were not started!', i)


def parse_args():
    """Parse command line arguments.

    :return: parsed arguments
    :rtype: argparse.Namespace
    """
    description = """
    Start windows VMs on AWS that are required for GSS TSIG tests.
    """
    main_parser = argparse.ArgumentParser(description=description,
                                          formatter_class=argparse.RawDescriptionHelpFormatter)

    main_parser.add_argument('--start', action='store_true',
                             help='Start windows VMs on AWS.')
    main_parser.add_argument('--id', default=None,
                             help='Terminate AWS system with id, multiple ids can be passed separated by comma.')
    main_parser.add_argument('--terminate', action='store_true',
                             help='Terminate all windows VMs on AWS saved in aws-win-ad-dns-vm*.txt files.')

    args, _ = main_parser.parse_known_args()
    return args


def main():
    """Parse command line arguments and start or terminate windows VMs on AWS."""
    args = parse_args()
    if args.start:
        win_vm_2016 = _setup_win_ad_dns('ami-06774e1cb71fbe789', 'win2016ad.aws.isc.org')
        win_vm_2019 = _setup_win_ad_dns('ami-06602a989923b1eba', 'win2019ad.aws.isc.org')

        for vm, version in zip([win_vm_2016, win_vm_2019], ['2016', '2019']):
            vm.wait_until_running()
            vm.reload()
            win_dns_addr = vm.private_ip_address
            with open(f'aws-win-ad-dns-vm{version}.txt', 'a', encoding='utf-8') as f:
                f.write(f'ip-address={win_dns_addr}\n')
            with open("init_all.py", 'a', encoding='utf-8') as f:
                f.write(f'\nWIN_DNS_ADDR_{version}="{win_dns_addr}"\n')
            log.info('Windows %s vm ip-address: %s', version, win_dns_addr)
            log.info('To access windows %s vm use: ssh Administrator@%s from bikeshed', version, vm.public_ip_address)

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
