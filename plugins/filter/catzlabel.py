from ansible.errors import AnsibleError
import dns.name
import hashlib

DOCUMENTATION = r'''
  name: catzlabel
  version_added: "1.0.0"
  short_description: convert a DNS domain name to a unique hash for a catalog zone
  description:
    - Hash a DNS domain name to a unique label destined to be used as owner name
      in a catalog zone (
      https://jpmens.net/2016/05/24/catalog-zones-are-coming-to-bind-9-11/ )
  positional: _input, query
  options:
    _input:
      description: domain name
      type: str
      required: true
'''

EXAMPLES = r'''

    label: '{{ "example.com" | catzlabel }}'
    # => "c5e4b4da1e5a620ddaa3635e55c3732a5b49c7f4"

'''

def catzlabel(domain):
    hash = None
    try:
        hash = hashlib.sha1(dns.name.from_text(domain).to_wire()).hexdigest()
    except Exception as e:
        raise AnsibleError('cannot convert {0}: {1}'.format(domain, str(e)))
    
    return hash

class FilterModule(object):
    def filters(self):
        return {
            'catzlabel'   : catzlabel,
        }
