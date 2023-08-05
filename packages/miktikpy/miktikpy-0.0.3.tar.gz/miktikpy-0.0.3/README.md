# miktikpy

`miktikpy` is a Python library for interacting with MikroTik routers using their REST API. It provides a convenient way to automate common tasks, such as retrieving IP addresses, managing interfaces, and working with ARP entries.


## Introduction
miktikpy is a Python library that simplifies interaction with MikroTik routers through their REST API. It provides a convenient and intuitive way to automate common tasks, such as retrieving IP addresses, managing interfaces, and working with ARP entries. Whether you're a network administrator, a developer, or an enthusiast, miktikpy enables you to streamline your MikroTik router management processes and save time.

By leveraging the REST API provided by MikroTik routers, miktikpy allows you to retrieve essential information about IP addresses, interfaces, and ARP entries, as well as perform actions such as enabling/disabling interfaces, configuring interface properties, and managing bridge interfaces. The library handles the underlying HTTP requests and authentication, abstracting away the complexities and providing a straightforward interface for interacting with your MikroTik router.

With miktikpy, you can easily integrate MikroTik router management into your existing Python projects or develop custom automation scripts tailored to your specific needs. The library supports authentication using username and password credentials, ensuring secure access to your router's REST API.

To get started with miktikpy, simply install the library using pip, establish a connection to your MikroTik router by providing the router's IP address, username, and password, and start utilizing the available methods to retrieve information or perform actions on your router.

Whether you're looking to automate routine tasks, gather network information programmatically, or build custom network management solutions, miktikpy empowers you with the tools to efficiently interact with MikroTik routers and enhance your network administration experience.

Now that you have an overview of what miktikpy offers, let's dive into the installation process and explore its features in more detail.

### As of now the functionality is still very limited , so expect interim updates. Over the next few months, I will be adding more features in miktikpy.
## Features

- Retrieve IP addresses from a MikroTik router
- Manage interfaces: get information, enable/disable, configure properties
- Work with ARP entries: retrieve, add, remove
- Supports authentication with username and password
- Compatible with MikroTik RouterOS versions os7 and above

You would first need to secure your router with a ssl certificate without it the Rest API will not work

Generating a Self-Signed SSL Certificate on your Mikrotik
Access your MikroTik router via web or Winbox.

Go to the "System/Certificates" section.

Click on the "Add New" button to create a new certificate.

In the "Subject" field, enter the details for the certificate. This typically includes information such as the common name (e.g., your domain or hostname), organization, location, etc.

"Key Size" 2048 is the minimum recommended bits to use . You could also use 4096 but please note this could take a few minutes depending on the type of cpu in the router. Generating 8192
on a router is not advisable as it could take hours to generate

In the "Validity" section, specify the duration for which the certificate should be valid. Typically, certificates are valid for a certain number of years.

In the "Key Usage" section, select the appropriate key usage options based on your requirements. This determines how the certificate can be used, such as for encryption, signing, or both.
### Required
- Digital Signature: This key usage allows the certificate to be used for verifying digital signatures, which is essential for establishing secure connections.

- Key Encipherment: This key usage allows the certificate to be used for encrypting data during SSL/TLS sessions.

- Key Agreement (optional): This key usage allows the certificate to be used for key agreement protocols, such as Diffie-Hellman key exchange. This is typically required for some advanced SSL/TLS configurations.

In the "SAN (Subject Alternative Name)" section, you can specify additional domain names or IP addresses that the certificate should be valid for. This is useful if you have multiple domains or subdomains associated with your router.

Optionally, you can configure advanced settings such as CRL (Certificate Revocation List), OCSP (Online Certificate Status Protocol), or specify custom extensions.

Once you have provided all the necessary details, click on the "Sign" button to generate the self-signed certificate.

The self-signed certificate is now created and available in the list of certificates.

- Go to "ip/services"
- Select api-ssl
- In the Certificate dropdown menu select the newly generated certificate
- Click on "Save"

You should now be able to access the certificate via web or Winbox.

[UPDATE]

After adding additional domain name, you need to save the certificate and then use the same command to sign it.

You can also use the same command to create a signed certificate for multiple IPs.

The "verify ssl" attribute is by default set to "False", so it will not be checked. To enable it, simply set it to "True" by passing it as an argument.
```
verify=True
```

## Installation

You can install `miktikpy` using pip:
```
pip install miktikpy
```
Usage
Here's a basic example of how to use miktikpy:

```
from miktikpy import MikroTikAPI

# Initialize MikroTikAPI with router IP, username, and password
api = MikroTikAPI('192.168.0.1', 'admin', 'password')

# Retrieve IP addresses
ip_addresses = api.get_ip_addresses()
for address in ip_addresses:
    print(address)

# Get interface information
interfaces = api.get_interfaces()
for interface in interfaces:
    print(interface)

# Add a bridge interface
api.add_bridge(name='br0')

# Get interface information filterted by properties

interfaces = api.get_interfaces(proplist={'interface_type':'wlan','mac_address':'AA:BB:CC:DD:EE:FF'})


```
For more detailed usage examples and available methods, please refer to the API Documentation.

Contributing
Contributions are welcome! If you have any ideas, bug reports, or feature requests, please open an issue or submit a pull request. Make sure to follow the Contributing Guidelines.

License
This project is licensed under the MIT License. See the LICENSE file for more information.
