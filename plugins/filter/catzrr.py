from ansible.errors import AnsibleError
import dns.name
import hashlib

DOCUMENTATION = r'''
  name: catzrr
  version_added: "1.0.0"
  short_description: print a DNS resource record for a catalog zone
  description:
    - Return a full DNS resource record for a specified domain name, with a
      hashed ownername and a PTR to the domain,  suitable for use in a catalog
      zone (
      https://jpmens.net/2016/05/24/catalog-zones-are-coming-to-bind-9-11/ )
  positional: _input, query
  options:
    _input:
      description: domain name
      type: str
      required: true
'''

EXAMPLES = r'''

    label: '{{ "example.com" | catzrr }}'
    # => "c5e4b4da1e5a620ddaa3635e55c3732a5b49c7f4.zones\t\tPTR example.com."

'''

def catzrr(domain):
    fqdn = dns.name.from_text(domain)
    label = None
    try:
        label = hashlib.sha1(dns.name.from_text(domain).to_wire()).hexdigest()
    except Exception as e:
        raise AnsibleError('cannot convert {0}: {1}'.format(domain, str(e)))
    
    return "{0}.zones\t\tPTR {1}".format(label, fqdn)

class FilterModule(object):
    def filters(self):
        return {
            'catzrr'   : catzrr,
        }
