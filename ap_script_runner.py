#!/usr/bin/python

__version__ = ' 1.0 Added argparse'

import paramiko
from cStringIO import StringIO
from time import sleep
from sys import argv
from os import popen
import argparse


parser = argparse.ArgumentParser(description = 'A tool to run an arbitrary terminal command script against an access point.')
parser.add_argument('script', help='Script name or path e.g. "/home/clay/newAPScript.txt"')
parser.add_argument('ip_address', help='IP Address of the Access Point')
parser.add_argument('--silent', '--s', help='Suppress output except for the result of a READ', action='store_true')
parser.add_argument('--version', '--v', help='Returns the version number of this script.', action='version', version=__version__)

args = parser.parse_args()



if args.silent is None:
    args.silent = False


def is_online( target ):
    if 'icmp_seq' in popen('ping -i 0.5 -c 2 %s' % target).read():
        return True
    else:
        return False


def get_script( script_path ):
    with open( script_path ) as f:
        script_lines=f.read().splitlines()
    return script_lines


if is_online( args.ip_address ):
    if not args.silent:
        print("The AP is online.")
    try:
        ap_connection = paramiko.SSHClient()
        #key = paramiko.DSSKey.from_private_key(StringIO(claylib.helpdesk_key))
        ap_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ap_connection.connect(args.ip_address, username='admin', password=<snipped AP remote password>, timeout=30)
        channel = ap_connection.invoke_shell()
        stdin = channel.makefile('wb')
        stdout = channel.makefile('rb')
        for line in get_script( args.script ):
            if not args.silent:
                print("Sending command \"%s\"..." % (line))
            if "READ" in line:
                print(last_response)
            else:
                sleep(1)
                channel.send("%s\r" % (line))
                sleep(1)
                last_response = channel.recv(2048)
    except paramiko.BadAuthenticationType:
        print("Error: Probably a bad password.")
    except paramiko.SSHException:
        print("Error: Possible timeout. Try again.")
    except Exception as e:
        print("Error: %s" % (e))
else:
    print("The AP is not responding to pings!")
    print("Please check the IP address.")
    exit()
