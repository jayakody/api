#!/usr/bin/python


DOCUMENTATION = '''
---
module: bmf_rest_bigchain_add_service_instance
short_description: BMF BigChain add service instance
description:
  - Makes HTTPS request to add a service instance.
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
    - name: Add WAF service instance
      bmf_rest_bigchain_add_service_instance: 'node={{ inventory_hostname }} name=WAF instance_id=1 switch=00:00:cc:37:ab:2c:97:ea input=ethernet20 output=ethernet21'

# Here's how you would run it.
% ansible-playbook <playbook.yml> -v
'''

RETURN = '''
TASK [Add WAF service instance] ************************************************
task path: /home/admin/playbooks/bmf_bigchain_config_tasks.yml:11
<10.2.19.102> ESTABLISH LOCAL CONNECTION FOR USER: admin
<10.2.19.102> EXEC /bin/sh -c '( umask 77 && mkdir -p "` echo $HOME/.ansible/tmp/ansible-tmp-1477074513.94-280014149993979 `" && echo ansible-tmp-1477074513.94-280014149993979="` echo $HOME/.ansible/tmp/ansible-tmp-1477074513.94-280014149993979 `" ) && sleep 0'
<10.2.19.102> PUT /tmp/tmpUSC9Ks TO /home/admin/.ansible/tmp/ansible-tmp-1477074513.94-280014149993979/bmf_rest_bigchain_add_service_instance
<10.2.19.102> EXEC /bin/sh -c 'chmod u+x /home/admin/.ansible/tmp/ansible-tmp-1477074513.94-280014149993979/ /home/admin/.ansible/tmp/ansible-tmp-1477074513.94-280014149993979/bmf_rest_bigchain_add_service_instance && sleep 0'
<10.2.19.102> EXEC /bin/sh -c 'LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 LC_MESSAGES=en_US.UTF-8 /usr/bin/python /home/admin/.ansible/tmp/ansible-tmp-1477074513.94-280014149993979/bmf_rest_bigchain_add_service_instance; rm -rf "/home/admin/.ansible/tmp/ansible-tmp-1477074513.94-280014149993979/" > /dev/null 2>&1 && sleep 0'
ok: [10.2.19.102] => {"changed": false, "invocation": {"module_args": {"input": "ethernet20", "instance_id": "1", "name": "WAF", "node": "10.2.19.102", "output": "ethernet21", "switch": "00:00:cc:37:ab:2c:97:ea"}, "module_name": "bmf_rest_bigchain_add_service_instance"}, "service_instance": {}, "service_instance_endpoints": {}}
'''


import sys
import json

sys.path.append('/home/admin/modules')

from bsn_rest import BmfRest
from ansible.module_utils.basic import *

def main():
    fields = dict(node          = dict(required=True),
                  user         = dict(required=True),
                  password     = dict(required=True),
                  name          = dict(required=True, type="str"),
                  instance_id   = dict(required=True, type="str"),
                  switch        = dict(required=True, type="str"),
                  input  = dict(required=True, type="str"),
                  output = dict(required=True, type="str"))
    
    module = AnsibleModule(
        argument_spec = fields,
        supports_check_mode = True)

    node = module.params['node']
    user = module.params['user']
    password = module.params['password']
    name = module.params['name']
    instance_id = module.params['instance_id']
    switch = module.params['switch']
    in_interface = module.params['input']
    out_interface = module.params['output']
    result = {}

    with BmfRest(host=node, user=user, password=password, debug=True) as dev:
        path = dev.bigchain_path()+'service[name="%s"]/instance[id=%s]' % (name, instance_id)
        data = {"id": instance_id}
        service_instance = dev.put(path, data=data)['content']
        
        path = dev.bigchain_path()+'service[name="%s"]/instance[id=%s]/interface-pair' % (name, instance_id)
        data = {"switch": switch, "in": in_interface, "out": out_interface}
        service_instance_endpoints = dev.put(path, data=data)['content']

        result = dict(service_instance=service_instance, service_instance_endpoints=service_instance_endpoints)

    module.exit_json(**result)

if __name__ == '__main__':
    main()