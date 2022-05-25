from oslo_log import log as oslo_logging

from cloudbaseinit import conf as cloudbaseinit_conf
from cloudbaseinit.metadata.services import nocloudservice
from cloudbaseinit.utils import debiface

CONF = cloudbaseinit_conf.CONF
LOG = oslo_logging.getLogger(__name__)


class SakuraCloudService(nocloudservice.NoCloudConfigDriveService):
    def get_network_details(self):
        import ipaddress

        interfaces = self._get_meta_data().get('Server', {}).get('Interfaces', {})
        if interfaces == {}:
            return None

        debian_net_config = 'network-interfaces: |'
        for index, interface in enumerate(interfaces):
            subnet = interface['Switch']['Subnet']
            ip = ipaddress.ip_network(f"{subnet['NetworkAddress']}/{subnet['NetworkMaskLen']}")
            debian_net_config += f'''
        iface Ethernet{index} inet static
        address {interface['IPAddress']}
        network {ip.network_address}
        netmask {ip.netmask}
        gateway {subnet['DefaultRoute']}
        hwaddress ether {interface['MACAddress']}'''

        return debiface.parse(debian_net_config)
