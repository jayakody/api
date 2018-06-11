import httplib2
import base64
import json


class BsnRest(object):
    def __init__(self, host, user, password, debug=False):
        self.host = host
        self.user = user
        self.password = password
        self.debug = debug
        self.http = None
        self.http_port = None
        self.session_cookie = None
        self.headers = None
        self.set_headers()

    def set_headers(self):
        """
        Create HTTP headers for accessing Big Switch controller.
        """
        raise NotImplementedError()

    def base_url(self):
        raise NotImplementedError()

    def delete_session_cookie(self):
        raise NotImplementedError()

    def get_session_cookie(self):
        return self.session_cookie

    def to_json(self, python_dict):
        return json.dumps(python_dict, indent=4, sort_keys=True)

    def from_json(self, json_str):
        return json.loads(json_str)

    def http_request(self, url, verb='GET', data=None):
        verb = verb.upper()
        if not verb in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
            raise ValueError('REST verb must be a GET, POST, PUT, PATCH, or DELETE')
        url = self.base_url() + url
        json_str = ''
        if data:
            json_str = self.to_json(data)
        if self.debug:
            print("DEBUG: %s %s, DATA='%s'" % (verb, url, json_str))
        resp, content = self.http.request(url, verb, body=json_str, headers=self.headers)

        # Sometimes returned content is an empty string, convert it to empty dictionary.
        if content == '':
            content = '{}'

        return {
                "response": resp,
                "content": json.loads(content)
                }

    def get(self, url, *args, **kwargs):
        return self.http_request(url, 'GET', *args, **kwargs)

    def post(self, url, *args, **kwargs):
        return self.http_request(url, 'POST', *args, **kwargs)

    def put(self, url, *args, **kwargs):
        return self.http_request(url, 'PUT', *args, **kwargs)

    def patch(self, url, *args, **kwargs):
        return self.http_request(url, 'PATCH', *args, **kwargs)

    def delete(self, url, *args, **kwargs):
        return self.http_request(url, 'DELETE', *args, **kwargs)


class BcfRest(BsnRest):
    """
    For BCF:
    - port 8443
    - https://host:8443/api/v1/auth/login
    - https://host:8443/api/v1/data/controller/applications/bvs/tenant[name="%s"]
    """
    def __init__(self, *args, **kwargs):
        super(BcfRest, self).__init__(*args, **kwargs)
        self.http_port = 8443

    def set_headers(self):
        self.http = httplib2.Http(".cache", disable_ssl_certificate_validation=True, timeout=30)
        base_url = "https://%s:8443" % self.host
        url = base_url + "/api/v1/auth/login"
        data = {'password': self.password, 'user': self.user}
        self.headers = {"content-type": "application/json"}
        data_json = json.dumps(data, indent=4, sort_keys=True)

        # Get session cookie.
        resp, content = self.http.request(url, 'POST', body=data_json, headers=self.headers)
        self.session_cookie = json.loads(content)['session_cookie']
        self.headers['Cookie'] = 'session_cookie=%s' % self.session_cookie
        return self.headers

    def base_url(self):
        return "https://%s:%s" % (self.host, self.http_port)

    def delete_session_cookie(self):
        if self.get_session_cookie() == None:
            return None
        url = '/api/v1/data/controller/core/aaa/session[auth-token="%s"]' % self.get_session_cookie()

        # ATTENTION: Not working. Need to investigate.
        result = self.delete(url)

        self.session_cookie = None
        return result


class BmfRest(BsnRest):
    """
    For BigChain/BigTap
    - port 8082 for API URL
    - port 8000 for REST URL
    - http://host:8082/auth/login (works with both 8000 and 8082 ports)
    - http://host:8082/api/v1/data/controller/core/switch[dpid="%s"]
    - http://host:8000/rest/v1/model/snmp-server-config/

    Be sure to configure controller firewall to enable access to these ports.
        controller-node 765ecc87-d641-4479-a7fb-39c6b6208978
        interface Ethernet 0
        firewall allow tcp 8000
        firewall allow tcp 8082
        firewall allow tcp 443
    """
    def __init__(self, *args, **kwargs):
        super(BmfRest, self).__init__(*args, **kwargs)
        self.http_port = 443
        self.bigchain = '/api/v1/data/controller/applications/bigchain/'

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        url = '/api/v1/data/controller/core/aaa/session[auth-token="%s"]' % self.get_session_cookie()
        result = self.delete(url)
        self.session_cookie = None
            
    def set_headers(self):
        self.http = httplib2.Http(".cache", disable_ssl_certificate_validation=True, timeout=30)
        url = self.base_url() + "/auth/login"
        data = {'password': self.password, 'user': self.user}
        self.headers = {"content-type": "application/json"}
        data_json = json.dumps(data, indent=4, sort_keys=True)

        # Get session cookie.
        resp, content = self.http.request(url, 'POST', body=data_json, headers=self.headers)
        self.session_cookie = json.loads(content)['session_cookie']
        self.headers['Cookie'] = 'session_cookie=%s' % self.session_cookie
        return self.headers

    def base_url(self):
        return "http://%s:443" % self.host

    def bigchain_path(self):
        return self.bigchain

    def bigchain_service_rules(self, name):
        #path = self.base_url() + self.bigchain_path()
        path = self.bigchain_path()+'service[name="%s"]/policy/rule' % name
        data = {}
        content = self.get(path, data)['content']
        if content:
            return content

    def bigchain_next_service_rule_sequence_number(self, name):
        """ returns the next available sequence number for a service rule """
        rules = self.bigchain_service_rules(name)
        if rules:
            current_sequence = map(lambda x: x['sequence'], rules)
            next_sequence_number = 1
            while next_sequence_number in current_sequence:
                next_sequence_number += 1
            return next_sequence_number
        return 1

    def bigchain_find_rule(self, name, ip_tuple):
        """ returns list of rules equal to rule, that are already programmed on the controller for the service  """
        rules = self.bigchain_service_rules(name)
        if not rules:
            return []
        matching_rules = []
        for rule in rules:
            if all(item in rule.items() for item in ip_tuple.items()):
                matching_rules.append(rule)
        return matching_rules
