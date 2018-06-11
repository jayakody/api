#!/usr/bin/python


DOCUMENTATION = '''
---
module: bsn_rest_show_version
short_description: BSN show version module
description:
  - Runs REST equivalence of 'show version' on BSN controller.
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
- hosts: tme-bmf-controllers
  connection: local
  gather_facts: no
  tasks:
    - name: Show version
      bmf_rest_show_version:
        node={{ inventory_hostname }}

# Here's how you would run it.
% ansible-playbook <playbook.yml> -v
'''

RETURN = '''
PLAY [tme-bmf-controllers] *****************************************************

TASK [Show version] ************************************************************
ok: [10.2.19.102] => {"changed": false, "content": [{"controller": "Big Tap Controller 5.8.0 (2016.09.27.0717-b.bsc.bmf-5.8.0)"}]}

PLAY RECAP *********************************************************************
10.2.19.102                : ok=1    changed=0    unreachable=0    failed=0
'''


import sys
import json

sys.path.append('/home/admin/modules')

from bsn_rest import BmfRest
from ansible.module_utils.basic import *


def main():
    module = AnsibleModule(
        argument_spec = dict(
            node = dict(required=False)
        ),
        supports_check_mode = True
    )


    node = module.params['node']

    result = None
    with BmfRest(host=node, user='admin', password='bsn', debug=True) as dev:
        content = dev.get('/rest/v1/system/version', data={})['content']
        result = dict(content=content)
        
    module.exit_json(**result)


if __name__ == '__main__':
    main()
