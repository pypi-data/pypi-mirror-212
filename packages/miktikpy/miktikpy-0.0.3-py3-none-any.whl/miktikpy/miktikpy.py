import requests

from .api import get_ip_addresses, get_interfaces, get_interface_lists


class MikroTikAPI:
    def __init__(self, ip, username, password, comment=None, interface=None, proplist=None,
                 dynamic=False, network=None, interface_id=None, list_name=None, member=None, mac_address=None):
        self.comment = comment
        self.interface = interface
        self.proplist = proplist
        self.ip = ip
        self.username = username
        self.password = password
        self.dynamic = dynamic
        self.network = network
        self.interface_id = interface_id
        self.list_name = list_name
        self.member = member
        self.mac_address = mac_address

    def get_ip_addresses(self):
        return get_ip_addresses(
            self.ip,
            self.username,
            self.password,
            self.interface_id,
            self.comment,
            self.interface,
            self.proplist,
            self.dynamic,
            self.network,
        )

    def get_interfaces(self):
        return get_interfaces(
            self.ip,
            self.username,
            self.password,
            self.interface_id,
            self.comment,
            self.interface,
            self.proplist,
        )

    def get_interface_lists(self):
        return get_interface_lists(
            self.ip,
            self.username,
            self.password,
            self.list_name,
            self.member,
            self.comment,
            self.proplist,
        )

    def get_arps(self):
        return get_interfaces(
            self.ip,
            self.username,
            self.password,
            self.interface_id,
            self.comment,
            self.interface,
            self.mac_address,
        )

    def update_ip(self, address_id=None, data=None):
        url = f"https://{self.ip}/rest/ip/address/{address_id}"
        headers = {"Content-Type": "application/json"}
        auth = (self.username, self.password)

        try:
            response = requests.patch(url, json=data, headers=headers, auth=auth, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def update_interface(self, username, password, data=None, interface_name=None):
        url = f"https://{self}/rest/interface/{interface_name}"
        headers = {"Content-Type": "application/json"}
        auth = (username, password)

        try:
            response = requests.patch(url, json=data, headers=headers, auth=auth, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def update_interface_list(self, list_name=None, data=None):
        url = f"https://{self}/rest/ip/address/{list_name}"
        headers = {"Content-Type": "application/json"}
        auth = (self.username, self.password)

        try:
            response = requests.patch(url, json=data, headers=headers, auth=auth, verify=False)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def update_bridge(self, bridge_name=None, data=None):
        url = f"https://{self}/rest/interface/bridge/{bridge_name}"
        headers = {"Content-Type": "application/json"}
        auth = (self.username, self.password)

        try:
            response = requests.patch(url, json=data, headers=headers, auth=auth, verify=False)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def add_ip(self, data=None):
        url = f"https://{self}/rest/ip/address"
        headers = {"Content-Type": "application/json"}
        auth = (self.username, self.password)

        try:
            response = requests.put(url, json=data, headers=headers, auth=auth, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def add_bridge(self, username, password, data):
        url = f"https://{self}/rest/interface/bridge"
        headers = {"Content-Type": "application/json"}
        auth = (username, password)

        try:
            response = requests.put(url, json=data, headers=headers, auth=auth, verify=False)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def main(self):
        """Example usage."""
        ip_addresses = self.get_ip_addresses()
        for ip_address in ip_addresses:
            print(ip_address)
        interfaces = self.get_interfaces()
        for interface in interfaces:
            print(interface)
        interface_lists = get_interface_lists(router_ip='192.168.0.1', username='admin', password='password',
                                              interface='wlan1')
        for interface_list in interface_lists:
            print(interface_list)

        interface_lists = get_interface_lists(router_ip='192.168.0.1', username='admin', password='password',
                                              list_name='les')
        print(interface_lists)

        interface_lists = get_interface_lists(router_ip='192.168.0.1', username='admin', password='password',
                                              list_name='les')
        print(interface_lists)
        arps = self.get_arps()
        for arp in arps:
            print(arp)


if __name__ == '__main__':
    mik = MikroTikAPI('192.168.0.1', 'admin', 'password')
    mik.main()
