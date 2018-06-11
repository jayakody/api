#!/usr/bin/python


DOCUMENTATION = '''
---
module: bmf_rest_bigchain_create_chain
short_description: BMF BigChain create chain
description:
  - Makes HTTPS request to create chain.
version_added: "1.0.0"
author:
  - Ted Elhourani (ted@bigswitch.com)
notes:
  - This module can only be called in a playbook with the connection set to
    'local'. The module will run locally on the Ansible host.
    
options: {}
'''

EXAMPLES = '''
# Playbook task
- hosts: tme-bmf-controllers
  connection: local
  gather_facts: no
  any_errors_fatal: true
  tasks:
    - name: Create chain
      bmf_rest_bigchain_create_chain: 'node={{ inventory_hostname }} name=Chain1 switch=00:00:cc:37:ab:2c:97:ea endpoint1=ethernet11 endpoint2=ethernet17'

# Here's how you would run it.
% ansible-playbook <playbook.yml> -v
'''

RETURN = '''
PLAY [tme-bmf-controllers] *****************************************************

TASK [Create chain] ************************************************************
task path: /home/admin/playbooks/bmf_bigchain_config_tasks.yml:7
<10.2.19.102> ESTABLISH LOCAL CONNECTION FOR USER: admin
<10.2.19.102> EXEC /bin/sh -c '( umask 77 && mkdir -p "` echo $HOME/.ansible/tmp/ansible-tmp-1477065852.28-135238786849019 `" && echo ansible-tmp-1477065852.28-135238786849019="` echo $HOME/.ansible/tmp/ansible-tmp-1477065852.28-135238786849019 `" ) && sleep 0'
<10.2.19.102> PUT /tmp/tmpYVl24r TO /home/admin/.ansible/tmp/ansible-tmp-1477065852.28-135238786849019/bmf_rest_bigchain_create_chain
<10.2.19.102> EXEC /bin/sh -c 'chmod u+x /home/admin/.ansible/tmp/ansible-tmp-1477065852.28-135238786849019/ /home/admin/.ansible/tmp/ansible-tmp-1477065852.28-135238786849019/bmf_rest_bigchain_create_chain && sleep 0'
<10.2.19.102> EXEC /bin/sh -c 'LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 LC_MESSAGES=en_US.UTF-8 /usr/bin/python /home/admin/.ansible/tmp/ansible-tmp-1477065852.28-135238786849019/bmf_rest_bigchain_create_chain; rm -rf "/home/admin/.ansible/tmp/ansible-tmp-1477065852.28-135238786849019/" > /dev/null 2>&1 && sleep 0'
ok: [10.2.19.102] => {"chain": {}, "changed": false, "endpoints": {}, "invocation": {"module_args": {"endpoint1": "ethernet11", "endpoint2": "ethernet17", "name": "Chain1", "node": "10.2.19.102", "switch": "00:00:cc:37:ab:2c:97:ea"}, "module_name": "bmf_rest_bigchain_create_chain"}}

PLAY RECAP *********************************************************************
10.2.19.102                : ok=1    changed=0    unreachable=0    failed=0
'''


import sys
import json

sys.path.append('/home/admin/modules')

from bsn_rest import BmfRest
from ansible.module_utils.basic import *

def main():
    fields = dict(node         = dict(required=True),
                  user         = dict(required=True),
                  password     = dict(required=True),
                  name         = dict(required=True, type="str"),
                  switch       = dict(required=True, type="str"),
                  endpoint1    = dict(required=True, type="str"),
                  endpoint2    = dict(required=True, type="str"))
    
    module = AnsibleModule(
        argument_spec = fields,
        supports_check_mode = True)

    node = module.params['node']
    user = module.params['user']
    password = module.params['password']
    
    name = module.params['name']
    switch = module.params['switch']
    endpoint1 = module.params['endpoint1']
    endpoint2 = module.params['endpoint2']
    result = {}
    with BmfRest(host=node, user=user, password=password, debug=True) as dev:
        path = dev.bigchain_path()+'chain[name="%s"]' % name
        data = {"name": name}
        chain = dev.put(path, data=data)['content']

        path = dev.bigchain_path()+'chain[name="%s"]/endpoint-pair' % name
        data = {"switch": switch, "endpoint1": endpoint1, "endpoint2": endpoint2}
        endpoints = dev.patch(path, data=data)['content']

        result = dict(chain=chain, endpoints=endpoints)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
