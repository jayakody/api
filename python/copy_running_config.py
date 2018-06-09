#!/usr/bin/env python
# Descriptions:
# - Dependencies:
#     % pip install pexpect

import pexpect
import argparse
import os
import datetime

descr = """
This tool copies the config snapshot to a specified destination.

Usage:
   % ./copy_running_config.py \\
                 -c 10.8.28.14 \\
                 -u admin \\
                 -p adminadmin \\
                 --dest-path root@10.8.0.99:/tmp \\
                 --dest-password bsn
   Executing 'ssh -o "UserKnownHostsFile /dev/null" -o "StrictHostKeyChecking no" admin@10.8.28.14'
   Enter CLI enable mode
   Copying running-config to snapshot://config-snapshot-20180523_140849
   Copying running-config to scp://root@10.8.0.99:/tmp/config-snapshot-20180523_140849
   Sending password to dest path.
   Done!
"""

parser = argparse.ArgumentParser(prog=os.path.basename(__file__),
                                 formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description=descr)

parser.add_argument('-c', '--controller', help='Controller IP address',
                    required=True)
parser.add_argument('-u', '--user', help='User name',
                    required=True)
parser.add_argument('-p', '--password', help='User password',
                    required=True)
parser.add_argument('--dest-path', help='Destination user, host and path, e.g., root@10.8.28.14:/tmp',
                    required=True)
parser.add_argument('--dest-password', help='Destination password',
                    required=True)
parser.add_argument('--dest-file', help='Destination file name')

args = parser.parse_args()

if not args.dest_file:
    local_datetime = datetime.datetime.now()
    dts = local_datetime.strftime("%Y%m%d_%H%M%S")
    args.dest_file = 'config-snapshot-%s' % dts


cmd = ('ssh -o "UserKnownHostsFile /dev/null" -o "StrictHostKeyChecking no" %s@%s'
       % (args.user, args.controller))
print("Executing '%s'" % cmd)
#child = pexpect.spawn(cmd)
child = pexpect.spawn(cmd)
child = pexpect.popen_spawn.PopenSpawn(cmd)

opt = child.expect(['password:', 'yes/no'])
if opt == 1:
    child.sendline('yes')
    child.expect('password')
child.sendline(args.password)
child.expect('>')

print('Enter CLI enable mode')
child.sendline('enable')
child.expect('#')

print('Copying running-config to snapshot://%s' % args.dest_file)
child.sendline('copy running-config snapshot://%s' % args.dest_file)
opt = child.expect(['#', 'overwrite snapshot'])
if opt == 1:
    print('Overwriting existing file - snapshot://%s' % args.dest_file)
    child.sendline('yes')
    child.expect('#')

print('Copying running-config to scp://%s/%s' % (args.dest_path, args.dest_file))
child.sendline('copy running-config scp://%s/%s' % (args.dest_path, args.dest_file))

opt = child.expect(['password:'])
if opt != 0:
    print('ERROR: Expected password prompt but did not see it.')
    sys.exit(1)
else:
    print("Sending password to dest path.")
    child.sendline(args.dest_password)
child.expect('#')

print('Done!')



