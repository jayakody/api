#!/usr/bin/python
# Sample module using Ansible Module Boilerplate as described in
# http://docs.ansible.com/ansible/developing_modules.html.

# See https://github.com/ansible/ansible/blob/devel/examples/DOCUMENTATION.yml
DOCUMENTATION = '''
---
module: hellotest
short_description: Hello simple module
description:
  - This module simply returns the hello greeting.
  - Seriously, that's all it does!
version_added: "1.0.0"
author:
  - Vui Le (amelon@gmail.com)
notes:
  - It took me like 10 minutes to put this together.
options: {}
'''

EXAMPLES = '''
# Here's how you would run it.
ansible all -m hellotest -a name=Vui
'''

RETURN = '''
  message:
    description: the hello greeting
    return: success
    type: string
    sample: "Hello, Vui"
'''


def main():
    module = AnsibleModule(
        argument_spec = dict(
            name = dict(required=False)
        ),
        supports_check_mode = True
    )
    result = dict(message='Hello, World')
    if module.params['name']:
        result['message'] = "Hello, " + module.params['name']
    module.exit_json(**result)


#from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import *


if __name__ == '__main__':
    main()
