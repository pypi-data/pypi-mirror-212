"""DNS Authenticator for SOLIDserver."""
import logging

from eiprest import EipRest
import zope.interface
from certbot import errors, interfaces
from certbot.plugins import dns_common

logger = logging.getLogger(__name__)


@zope.interface.implementer(interfaces.IAuthenticator)
@zope.interface.provider(interfaces.IPluginFactory)
class Authenticator(dns_common.DNSAuthenticator):
    """DNS Authenticator for SOLIDserver
    
    This Authenticator uses the SOLIDserver REST API to fulfill a dns-01 challenge.
    """

    description = "Obtain certificates using a DNS TXT record (if you are using SOLIDserver for DNS)."
    ttl = 120

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add):  # pylint: disable=arguments-differ
        super(Authenticator, cls).add_parser_arguments(
            add, default_propagation_seconds=10
        )
        add("credentials", help="SOLIDserver credentials INI file.",
        	default='/etc/letsencrypt/solidserver.ini')

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return ("This plugin configures a DNS TXT record to respond to a dns-01 challenge using the SOLIDserver Remote REST API.")

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            "credentials",
            "SOLIDserver credentials INI file",
            {
                "hostname": "Hostname for SOLIDserver REST API.",
                "username": "Username for SOLIDserver REST API.",
                "password": "Password for SOLIDserver REST API.",
                "dnsname": "DNS server name.",
                "viewname": "View to use for TXT entries (leave blank if not used)"
            },
        )

    def _perform(self, domain, validation_name, validation):
        self._get_eiprest_client().add_txt_record(domain, validation_name, validation, self.ttl)

    def _cleanup(self, domain, validation_name, validation):
        self._get_eiprest_client().del_txt_record(domain, validation_name, validation, self.ttl)

    def _get_eiprest_client(self):
    	return _EipRestClient(
    		self.credentials.conf("hostname"),
            self.credentials.conf("username"),
            self.credentials.conf("password"),
            self.credentials.conf("dnsname"),
            self.credentials.conf("viewname"),
    	)

class _EipRestClient(object):
    """
    Encapsulates all communication with the SOLIDserver REST API.
    """

    def __init__(self, hostname, username, password, dnsname, viewname):
        logger.debug("creating eiprest client")
        self.dnsname = dnsname
        self.viewname = viewname
        self.eiprest = EipRest(host=hostname, user=username, password=password)

    def add_txt_record(self, domain, record_name, record_content, ttl):
        record = self.get_rr_txt(record_name)
        if record is not None:
            if record[0]["value1"] == record_content:
                logger.info(f"already there, id {record[0]['rr_id']}")
                return
            else:
                logger.info(f"update record {record[0]['rr_id']}")
                self.update_rr_txt(record[0]['rr_id'], record_content, ttl)    
        else:
            logger.info("insert new txt record")
            self.add_rr_txt(record_name, record_content, ttl)

    def del_txt_record(self, domain, record_name, record_content, ttl):
        params = {
            'WHERE': f"rr_full_name='{record_name}' AND rr_type='TXT' AND value1='{record_content}' AND vdns_parent_id=0 AND dnszone_type='master'",
        }
        self.eiprest.query('GET', 'dns_rr_list', params)
        resp = self.eiprest.getData()
        if resp:
            for rr in resp:
                logger.info(f"delete record TXT {rr['rr_full_name']}")
                self.eiprest.query('DELETE', 'dns_rr_delete', {'rr_id': rr['rr_id']})

    def get_rr_txt(self, rr_name):
        params = {
            'WHERE': f"dns_name='{self.dnsname}' AND rr_full_name='{rr_name}' AND rr_type='TXT'",
            'limit': 1,
        }
        if self.viewname:
            params['WHERE'] += f" AND dnsview_name='{self.viewname}'"
        self.eiprest.query('GET', 'dns_rr_list', params)
        return self.eiprest.getData()

    def update_rr_txt(self, rr_id, value1, ttl):
        params = {
            'rr_id': rr_id,
            'value1': value1,
            'rr_ttl': ttl,
            'add_flag': 'edit_only',
        }
        self.eiprest.query('POST', 'dns_rr_add', params)
        if self.eiprest.resp.status_code != 201:
            raise errors.PluginError(f"Failed to update record TXT {rr_name}")

    def add_rr_txt(self, rr_name, value1, ttl):
        params = {
            'dns_name': self.dnsname,
            'rr_name': rr_name,
            'rr_type': 'TXT',
            'value1': value1,
            'rr_ttl': ttl,
            'add_flag': 'new_only',
        }
        if self.viewname:
            params['dnsview_name'] = self.viewname
        self.eiprest.query('PUT', 'dns_rr_add', params)
        if self.eiprest.resp.status_code != 201:
            raise errors.PluginError(f"Failed to add record TXT {rr_name}")
    	