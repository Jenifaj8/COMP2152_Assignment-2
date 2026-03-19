"""
Unit Tests for Assignment 2 — Port Scanner
"""

import unittest

# TODO: Import your classes and common_ports from assignment2_studentID
# from assignment2_studentID import PortScanner, common_ports
from assignment2_101571040 import PortScanner, common_ports


class TestPortScanner(unittest.TestCase):

    def test_scanner_initialization(self):
        """Test that PortScanner initializes with correct target and empty results list."""
        # TODO: Create a PortScanner with target "127.0.0.1"
        scanner = PortScanner("127.0.0.1")
        # TODO: Assert scanner.target equals "127.0.0.1"
        self.assertEqual(scanner.target, "127.0.0.1")
        # TODO: Assert scanner.scan_results is an empty list
        self.assertEqual(scanner.scan_results, [])

    def test_get_open_ports_filters_correctly(self):
        """Test that get_open_ports returns only Open ports."""
        # TODO: Create a PortScanner object
        scanner = PortScanner("127.0.0.1")
        # TODO: Manually add these tuples to scanner.scan_results:
        #   (22, "Open", "SSH"), (23, "Closed", "Telnet"), (80, "Open", "HTTP")
        scanner.scan_results = [
            (22, "Open", "SSH"), 
            (23, "Closed", "Telnet"), 
            (80, "Open", "HTTP")
        ]
        # TODO: Call get_open_ports() and assert the returned list has exactly 2 items
        open_ports = scanner.get_open_ports()
        self.assertEqual(len(open_ports), 2)

    def test_common_ports_dict(self):
        """Test that common_ports dictionary has correct entries."""
        # TODO: Assert common_ports[80] equals "HTTP"
        self.assertEqual(common_ports[80], "HTTP")
        # TODO: Assert common_ports[22] equals "SSH"
        self.assertEqual(common_ports[22], "SSH")

    def test_invalid_target(self):
        """Test that setter rejects empty string target."""
        # TODO: Create a PortScanner with target "127.0.0.1"
        scanner = PortScanner("127.0.0.1")
        # TODO: Try setting scanner.target = "" (empty string)
        scanner.target = ""
        # TODO: Assert scanner.target is still "127.0.0.1"
        self.assertEqual(scanner.target, "127.0.0.1")


if __name__ == "__main__":
    unittest.main()
