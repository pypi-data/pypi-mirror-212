from .miktikpy import MikroTikAPI


# Example test case
def test_get_ip_addresses():
    # Create an instance of MikroTikAPI with the appropriate credentials
    api = MikroTikAPI('192.168.0.1', 'admin', 'password')

    # Call the method you want to test
    ip_addresses = api.get_ip_addresses()

    # Add assertions to verify the expected behavior
    assert len(ip_addresses) > 0
