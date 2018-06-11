#!/usr/bin/python


DOCUMENTATION = '''
---
module: bmf_rest_bigchain_remove_service_instance
short_description: BMF BigChain remove service instance
description:
  - Makes HTTPS request to remove a service instance from a chain.
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

# Here's how you would run it.
% ansible-playbook <playbook.yml> -v
'''

RETURN = '''
'''


import sys
import json

sys.path.append('/home/admin/modules')

from bsn_rest import BmfRest
from ansible.module_utils.basic import *

def main():
    fields = dict(node             = dict(required=True),
                  user    = dict(required=True),
                  password    = dict(required=True),
                  chain            = dict(required=True, type="str"),
                  service          = dict(required=True, type="str"),
                  service_instance = dict(required=True, type="str"))
    
    module = AnsibleModule(
        argument_spec = fields,
        supports_check_mode = True)

    node = module.params['node']
    chain = module.params['chain']
    service = module.params['service']
    service_instance = module.params['service_instance']
    result = {}
    with BmfRest(host=node, user=user, password=password, debug=True) as dev:
        path = dev.bigchain_path()+'chain[name="%s"]/service[service-name="%s"]' % (chain, service)
        data = {"instance": service_instance}
        remove_service_instance = dev.delete(path, data=data)['content']

        result = dict(remove_service_instance=remove_service_instance)
    module.exit_json(**result)


if __name__ == '__main__':
    main()
