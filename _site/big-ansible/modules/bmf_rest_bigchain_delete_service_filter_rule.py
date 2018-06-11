#!/usr/bin/python


DOCUMENTATION = '''
---
module: bmf_rest_bigchain_create_service
short_description: BMF BigChain create service
description:
  - Makes HTTPS request to create service.
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
    - name: Create service WAF
      bmf_rest_bigchain_create_service: 'node={{ inventory_hostname }} name=WAF1'

# Here's how you would run it.
% ansible-playbook <playbook.yml> -v
'''

RETURN = '''
TASK [Create service WAF] ******************************************************
task path: /home/admin/playbooks/bmf_bigchain_config_tasks.yml:9
<10.2.19.102> ESTABLISH LOCAL CONNECTION FOR USER: admin
<10.2.19.102> EXEC /bin/sh -c '( umask 77 && mkdir -p "` echo $HOME/.ansible/tmp/ansible-tmp-1477066486.48-199660440974737 `" && echo ansible-tmp-1477066486.48-199660440974737="` echo $HOME/.ansible/tmp/ansible-tmp-1477066486.48-199660440974737 `" ) && sleep 0'
<10.2.19.102> PUT /tmp/tmptskwsh TO /home/admin/.ansible/tmp/ansible-tmp-1477066486.48-199660440974737/bmf_rest_bigchain_create_service
<10.2.19.102> EXEC /bin/sh -c 'chmod u+x /home/admin/.ansible/tmp/ansible-tmp-1477066486.48-199660440974737/ /home/admin/.ansible/tmp/ansible-tmp-1477066486.48-199660440974737/bmf_rest_bigchain_create_service && sleep 0'
<10.2.19.102> EXEC /bin/sh -c 'LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 LC_MESSAGES=en_US.UTF-8 /usr/bin/python /home/admin/.ansible/tmp/ansible-tmp-1477066486.48-199660440974737/bmf_rest_bigchain_create_service; rm -rf "/home/admin/.ansible/tmp/ansible-tmp-1477066486.48-199660440974737/" > /dev/null 2>&1 && sleep 0'
ok: [10.2.19.102] => {"changed": false, "invocation": {"module_args": {"name": "WAF1", "node": "10.2.19.102"}, "module_name": "bmf_rest_bigchain_create_service"}, "service": {}}

PLAY RECAP *********************************************************************
10.2.19.102                : ok=2    changed=0    unreachable=0    failed=0
'''


import sys
import json

sys.path.append('/home/admin/modules')

from bsn_rest import BmfRest
from ansible.module_utils.basic import *

def main():
    fields = dict(node        = dict(required=True),
                  name        = dict(required=True, type="str"),
                  ip_proto    = dict(required=True, type="int"),
                  src_ip      = dict(required=True, type="str"),
                  src_ip_mask = dict(required=True, type="str"),
                  dst_ip      = dict(required=True, type="str"),
                  dst_ip_mask = dict(required=True, type="str"),
                  src_port    = dict(required=True, type="int"),
                  dst_port    = dict(required=True, type="int"))
    
    module = AnsibleModule(
        argument_spec = fields,
        supports_check_mode = True)

    node = module.params['node']
    name = module.params['name']
    ip_proto = module.params['ip_proto']
    src_ip = module.params['src_ip']
    src_ip_mask = module.params['src_ip_mask']
    dst_ip = module.params['dst_ip']
    dst_ip_mask = module.params['dst_ip_mask']
    src_tp_port = module.params['src_port']
    dst_tp_port = module.params['dst_port']
    
    result = dict(hello="hello")
    with BmfRest(host=node, user='admin', password='bsn', debug=True) as dev:
        rule = {"ether-type": 2048,
                "ip-proto": ip_proto,
                "src-ip": src_ip,
                "src-ip-mask": src_ip_mask,
                "dst-ip": dst_ip,
                "dst-ip-mask": dst_ip_mask,
                "src-tp-port": src_tp_port,
                "dst-tp-port": dst_tp_port}
        matching_rules = dev.bigchain_find_rule(name, rule)

        if not matching_rules:
            module.exit_json(**result)

        matching_rule = matching_rules[0]
        path = dev.bigchain_path()+'service[name="%s"]/policy/rule[sequence=%s]' % (name, matching_rule['sequence'])
        filter_rule_deletion = dev.delete(path, data=matching_rule)['content']
        result = dict(filter_rule_deletion=filter_rule_deletion)

        
    module.exit_json(**result)

if __name__ == '__main__':
    main()