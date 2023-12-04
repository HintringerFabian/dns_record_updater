import ipaddress
import unittest

from src.IpChecker import are_same_ipv4


class TestAreSameIpv4(unittest.TestCase):

    # Test with two identical IPv4 addresses
    def test_identical_ipv4_addresses(self):
        ip_a = ipaddress.IPv4Address('192.168.0.1')
        ip_b = ipaddress.IPv4Address('192.168.0.1')
        self.assertTrue(are_same_ipv4(ip_a, ip_b))

    # Test with two different IPv4 addresses
    def test_different_ipv4_addresses(self):
        ip_a = ipaddress.IPv4Address('192.168.0.1')
        ip_b = ipaddress.IPv4Address('192.168.0.2')
        self.assertFalse(are_same_ipv4(ip_a, ip_b))

    # Test with IPv4 address and its string representation
    def test_ipv4_address_and_string_representation(self):
        ip_a = ipaddress.IPv4Address('192.168.0.1')
        ip_b = '192.168.0.1'
        self.assertRaises(TypeError, are_same_ipv4, ip_a, ip_b)

    # Test with None as one of the inputs
    def test_none_input(self):
        ip_a = ipaddress.IPv4Address('192.168.0.1')
        ip_b = None
        self.assertRaises(TypeError, are_same_ipv4, ip_a, ip_b)

    # Test with empty string as one of the inputs
    def test_empty_string_input(self):
        ip_a = ipaddress.IPv4Address('192.168.0.1')
        ip_b = ''
        self.assertRaises(TypeError, are_same_ipv4, ip_a, ip_b)

    # Test with IPv6 address as one of the inputs
    def test_ipv6_address_input(self):
        ip_a = ipaddress.IPv4Address('192.168.0.1')
        ip_b = ipaddress.IPv6Address('2001:0db8:85a3:0000:0000:8a2e:0370:7334')
        self.assertRaises(TypeError, are_same_ipv4, ip_a, ip_b)
