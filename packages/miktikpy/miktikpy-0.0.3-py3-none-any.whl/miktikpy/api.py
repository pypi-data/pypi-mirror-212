import requests


def get_ip_addresses(router_ip, username, password, interface_id=None, comment=None, interface=None, network=None,
                     dynamic=False, proplist=None, address=None, disabled=False):
    base_url = f"https://{router_ip}/rest/ip/address"
    params = {}

    if interface_id is not None:
        base_url += f"/{interface_id}"

    if comment is not None:
        params["comment"] = comment

    if interface is not None:
        params["interface"] = interface

    if network is not None:
        params["network"] = network

    if dynamic is not False:
        params["dynamic"] = dynamic

    if proplist is not None:
        if address is not None:
            proplist += ",address"
        if disabled is not False:
            proplist += ",disabled"
        params[".proplist"] = proplist

    try:
        response = requests.get(base_url, auth=(username, password), verify=False, params=params)
        response.raise_for_status()

        ip_addresses = response.json()
        return ip_addresses

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def get_interfaces(router_ip, username, password, interface_id=None, comment=None, interface=None, proplist=None,
                   disabled=False, actual_mtu=None, fp_rx_byte=None, fp_rx_packet=None, fp_tx_byte=None,
                   fp_tx_packet=None, l2mtu=None, last_link_up_time=None, link_downs=None, mac_address=None, mtu=None,
                   interface_name=None, running=None, rx_byte=None, interface_type=None, tx_queue_drop=None,
                   tx_packet=None, tx_error=None, tx_drop=None, tx_byte=None, rx_packet=None, rx_error=None,
                   rx_drop=None):
    base_url = f"https://{router_ip}/rest/interface"
    params = {}

    if interface_id is not None:
        base_url += f"/{interface_id}"

    if comment is not None:
        params["comment"] = comment

    if interface is not None:
        params["interface"] = interface

    if proplist is not None:
        attributes = {
            "actual-mtu": actual_mtu,
            "disabled": disabled,
            "fp-rx-byte": fp_rx_byte,
            "fp-rx-packet": fp_rx_packet,
            "fp-tx-byte": fp_tx_byte,
            "fp-tx-packet": fp_tx_packet,
            "l2mtu": l2mtu,
            "last-link-up-time": last_link_up_time,
            "link-downs": link_downs,
            "mac-address": mac_address,
            "mtu": mtu,
            "name": interface_name,
            "running": running,
            "rx-byte": rx_byte,
            "rx-drop": rx_drop,
            "rx-error": rx_error,
            "rx-packet": rx_packet,
            "tx-byte": tx_byte,
            "tx-drop": tx_drop,
            "tx-error": tx_error,
            "tx-packet": tx_packet,
            "tx-queue-drop": tx_queue_drop,
            "type": interface_type
        }
        proplist = ",".join(attr for attr, value in attributes.items() if value is not None)
        params[".proplist"] = proplist

    try:
        response = requests.get(base_url, auth=(username, password), verify=False, params=params)
        response.raise_for_status()

        interfaces = response.json()
        return interfaces

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def get_interface_lists(router_ip, username, password, list_name=None, comment=None, proplist=None,
                        dynamic=False, static=False, interface=None):
    base_url = f"https://{router_ip}/rest/interface/list"
    params = {}

    if list_name is not None:
        base_url += f"/{list_name}"

    if interface is not None:
        base_url += "/member"
        params["interface"] = interface

    if comment is not None:
        params["comment"] = comment

    if proplist is not None:
        if dynamic is not False:
            proplist += ",dynamic"
        if static is not False:
            proplist += ",static"
        params[".proplist"] = proplist

    try:
        response = requests.get(base_url, auth=(username, password), verify=False, params=params)
        response.raise_for_status()

        interface_list = response.json()
        return interface_list

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def get_arps(router_ip, username, password, address, comment=None, mac_address=None, published=False, interface=None,
             interface_id=None,
             proplist=None, actual_mtu=None, disabled=None, fp_rx_byte=None, fp_rx_packet=None, fp_tx_byte=None,
             fp_tx_packet=None, l2mtu=None, last_link_up_time=None, link_downs=None, mtu=None, interface_name=None,
             running=False, rx_byte=None, rx_drop=None, rx_error=None, rx_packet=None, tx_byte=None, tx_drop=None,
             tx_error=None, tx_packet=None, tx_queue_drop=None, interface_type=None):
    base_url = f"https://{router_ip}/rest/arp"
    params = {}

    if interface_id is not None:
        base_url += f"/{interface_id}"

    if published is not None:
        params["published"] = published

    if interface is not None:
        params["interface"] = interface

    if mac_address is not None:
        params["mac-address"] = mac_address

    if address is not None:
        params["address"] = address

    if comment is not None:
        params["comment"] = comment

    if proplist is not None:
        attributes = {
            "actual-mtu": actual_mtu,
            "disabled": disabled,
            "fp-rx-byte": fp_rx_byte,
            "fp-rx-packet": fp_rx_packet,
            "fp-tx-byte": fp_tx_byte,
            "fp-tx-packet": fp_tx_packet,
            "l2mtu": l2mtu,
            "last-link-up-time": last_link_up_time,
            "link-downs": link_downs,
            "mac-address": mac_address,
            "mtu": mtu,
            "name": interface_name,
            "running": running,
            "rx-byte": rx_byte,
            "rx-drop": rx_drop,
            "rx-error": rx_error,
            "rx-packet": rx_packet,
            "tx-byte": tx_byte,
            "tx-drop": tx_drop,
            "tx-error": tx_error,
            "tx-packet": tx_packet,
            "tx-queue-drop": tx_queue_drop,
            "type": interface_type
        }
        proplist = ",".join(attr for attr, value in attributes.items() if value is not None)
        params[".proplist"] = proplist

    try:
        response = requests.get(base_url, auth=(username, password), verify=False, params=params)
        response.raise_for_status()

        interface_list = response.json()
        return interface_list

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def update_ip(router_ip, username, password, address_id, data):
    url = f"https://{router_ip}/rest/ip/address/{address_id}"
    headers = {"Content-Type": "application/json"}
    auth = (username, password)

    try:
        response = requests.patch(url, json=data, headers=headers, auth=auth, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def update_interface(router_ip, username, password, data=None, interface_name=None):
    url = f"https://{router_ip}/rest/interface/{interface_name}"
    headers = {"Content-Type": "application/json"}
    auth = (username, password)

    try:
        response = requests.patch(url, json=data, headers=headers, auth=auth, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def update_interface_list(router_ip, username, password, list_name, data):
    url = f"https://{router_ip}/rest/ip/address/{list_name}"
    headers = {"Content-Type": "application/json"}
    auth = (username, password)

    try:
        response = requests.patch(url, json=data, headers=headers, auth=auth, verify=False)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def add_ip(router_ip, username, password, data):
    url = f"https://{router_ip}/rest/ip/address"
    headers = {"Content-Type": "application/json"}
    auth = (username, password)

    try:
        response = requests.put(url, json=data, headers=headers, auth=auth, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def add_interface(router_ip, username, password, data):
    url = f"https://{router_ip}/rest/interface"
    headers = {"Content-Type": "application/json"}
    auth = (username, password)

    try:
        response = requests.put(url, json=data, headers=headers, auth=auth, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
