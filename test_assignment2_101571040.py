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
        # Create a PortScanner with target "127.0.0.1"
        scanner = PortScanner("127.0.0.1")
        # Assert scanner.target equals "127.0.0.1"
        self.assertEqual(scanner.target, "127.0.0.1")
        # Assert scanner.scan_results is an empty list
        self.assertEqual(scanner.scan_results, [])

    def test_get_open_ports_filters_correctly(self):
        """Test that get_open_ports returns only Open ports."""
        # Create a PortScanner object
        scanner = PortScanner("127.0.0.1")
        # Manually add these tuples to scanner.scan_results:
        #   (22, "Open", "SSH"), (23, "Closed", "Telnet"), (80, "Open", "HTTP")
        scanner.scan_results = [
            (22, "Open", "SSH"), 
            (23, "Closed", "Telnet"), 
            (80, "Open", "HTTP")
        ]
        # Call get_open_ports() and assert the returned list has exactly 2 items
        open_ports = scanner.get_open_ports()
        self.assertEqual(len(open_ports), 2)

    def test_common_ports_dict(self):
        """Test that common_ports dictionary has correct entries."""
        # Assert common_ports[80] equals "HTTP"
        self.assertEqual(common_ports[80], "HTTP")
        # Assert common_ports[22] equals "SSH"
        self.assertEqual(common_ports[22], "SSH")

    def test_invalid_target(self):
        """Test that setter rejects empty string target."""
        # Create a PortScanner with target "127.0.0.1"
        scanner = PortScanner("127.0.0.1")
        # Try setting scanner.target = "" (empty string)
        scanner.target = ""
        # Assert scanner.target is still "127.0.0.1"
        self.assertEqual(scanner.target, "127.0.0.1")


if __name__ == "__main__":
    unittest.main()
