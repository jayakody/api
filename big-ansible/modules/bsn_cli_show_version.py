#!/usr/bin/python


DOCUMENTATION = '''
---
module: bsn_cli_show_version
short_description: BSN show version module
description:
  - Runs 'show version' on BSN controller.
version_added: "1.0.0"
author:
  - Vui Le (amelon@gmail.com)
notes:
  - This module can only be called in a playbook with the connection set to
    'local'. The module will run locally on the Ansible host. It establishes
    the SSH session with the BSN controller and closes it when done.
    
options: {}
'''

EXAMPLES = '''
# Playbook task
- hosts: qa-controllers
  connection: local
  gather_facts: no
  tasks:
    - name: Show version
      bsn_cli_show_version:
          node={{ inventory_hostname }}

# Here's how you would run it.
% ansible-playbook <playbook.yml> -v
'''

RETURN = '''
PLAY [qa-controllers] **********************************************************

TASK [Show version] ************************************************************
ok: [10.8.7.214] => {"changed": false, "content": "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Appliance ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\r\nName              : Big Cloud Fabric Appliance\r\nBuild date        : 2016-09-16 19:00:15 UTC\r\nBuild user        : bsn\r\nCi build number   : 7516\r\nCi job name       : bcf_master\r\nCommunity edition : False\r\nRelease string    : Big Cloud Fabric Appliance 4.0.0-master-SNAPSHOT (bcf_master #7516)\r\nVersion           : 4.0.0-master-SNAPSHOT"}

PLAY RECAP *********************************************************************
10.8.7.214                 : ok=1    changed=0    unreachable=0    failed=0
'''


import sys
import json

sys.path.append('/home/admin/modules')

from bsn_cli import BsnCli
from ansible.module_utils.basic import *


def main():
    module = AnsibleModule(
        argument_spec = dict(
            node = dict(required=False)
        ),
        supports_check_mode = True
    )


    node = module.params['node']

    dev = BsnCli(node)

    content = dev.cmd('show version')
    result = dict(content=content)
    dev.close()
    module.exit_json(**result)


if __name__ == '__main__':
    main()
