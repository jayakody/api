#!/usr/bin/python
# Sample module as described in http://docs.ansible.com/ansible/developing_modules.html.

# See https://github.com/ansible/ansible/blob/devel/examples/DOCUMENTATION.yml
DOCUMENTATION = '''
---
module: timetest
short_description: This is a simple module to demonstrate Ansible Module capabilities.
description:
    - This module simply returns the current time.
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
ansible all -m timetest
'''

RETURN = '''
  time:
    description: the current time
    return: success
    type: string
    sample: "2016-08-25 14:04:51.423223"
'''

import datetime
import json

date = str(datetime.datetime.now())
print json.dumps({
    "time": date
})

