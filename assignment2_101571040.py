"""
Author: Jenifa Joseph
Assignment: #2
Description: Port Scanner — A tool that scans a target machine for open network ports
"""

# (Step ii) - Import the required modules - socket, threading, sqlite3, os, platform, datetime

import socket
import threading
import sqlite3
import os
import platform
import datetime


# (Step iii) - Print Python version and OS name

print(f"Python Version: {platform.python_version()}")
print(f"Operating System: {os.name}")


# (Step iv) - Create the common_ports dictionary & Add a 1-line comment above it explaining what it stores

# This dictionary stores the port numbers that are mapped to their service names.
common_ports = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Alt"
}


# (Step v) - Create the NetworkTool parent class

class NetworkTool:
    def __init__(self, target):
        self.__target = target

# Q3: What is the benefit of using @property and @target.setter? (2-4 sentence answer)
    # Using @property and @target.setter helps control how the target value is used.
    # The getter lets us access the value, and the setter makes sure it is not empty.
    # This prevents mistakes that could cause problems when scanning.
    # It also makes the code easier to understand and manage.
    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, value):
        if value != "":
             self.__target = value
        else:
            print("Error: Target cannot be empty")     

    def __del__(self):
        print("NetworkTool instance destroyed")
        

# (Step vi) - Create the PortScanner child class that inherits from NetworkTool

# Q1: How does PortScanner reuse code from NetworkTool? (2-4 sentence answer)
# PortScanner reuses code from NetworkTool by inheriting from it.
# This means it can use the target value from the parent class instead of creating it again.
# For example, PortScanner uses super().__init__(target) to set up the target.
# This saves time and keeps the code more organized.
class PortScanner(NetworkTool):
    def __init__(self, target):
        super().__init__(target)
        self.scan_results = []
        self.lock = threading.Lock()

    def __del__(self):
        print("PortScanner instance destroyed")
        super().__del__()

    def scan_port(self, port):
        sock = None

        # Q4: What would happen without try-except here? (2-4 sentence answer)
        # Without try-except, the program could stop if an error happens while scanning a port.
        # For example, if the target machine cannot be reached, the scanner may crash instead of continuing.
        # Using try-except helps the program handle the error and keep running.
        # It also shows an error message instead of ending the whole program.        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
            sock.settimeout(1)
            result = sock.connect_ex((self.target, port))

            if result == 0:
                status = "Open"
            else:
                status = "Closed"

            service_name = common_ports.get(port, "Unknown")
            self.lock.acquire()
            self.scan_results.append((port, status, service_name))
            self.lock.release()

        except socket.error as e:
            print(f"Error scanning port {port}: {e}")
        finally:
            if sock:
                sock.close() 

    def get_open_ports(self):
        return [result for result in self.scan_results if result[1] == "Open"]  


    # Q2: Why do we use threading instead of scanning one port at a time? (2-4 sentence answer)
    # We use threading so the program can scan many ports at the same time.
    # This makes the scan faster than checking one port and then the next one.
    # If we scanned 1024 ports without threads, it could take a long time to finish.
    # Threading helps save time and makes the scanner work better.                          

    def scan_range(self, start_port, end_port):
        threads = []
        for port in range(start_port, end_port + 1):
            thread = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()


# (Step vii) - Create save_results(target, results) function

def save_results(target, results):
    try:
        conn = sqlite3.connect("scan_history.db")
        cursor = conn.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS scans (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            target TEXT,
                            port INTEGER,
                            status TEXT,
                            service TEXT,
                            scan_date TEXT
                       )
                       """)
        for port, status, service in results:
            cursor.execute("""
                           INSERT INTO scans (target, port, status, service, scan_date)
                           VALUES (?, ?, ?, ?, ?)
                           """,
                           (target, port, status, service, str(datetime.datetime.now())))
        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    

# (Step viii) - Create load_past_scans() function 

def load_past_scans():
    conn = None
    try:
        conn = sqlite3.connect("scan_history.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM scans")
        rows = cursor.fetchall()
        for row in rows:
                print(f"[{row[5]}] {row[1]} : Port {row[2]} ({row[4]}) - {row[3]}")
                
        conn.close()

    except sqlite3.Error:
        print("No past scans found.")
        if conn:
            conn.close()


# ============================================================
# MAIN PROGRAM
# ============================================================

# (Step ix) - Get user input with try-except

if __name__ == "__main__":
    target = input("Enter target IP address (press Enter for 127.0.0.1): ").strip()
    if target == "":
        target = "127.0.0.1"

    try:
        start_port = int(input("Enter starting port number (1-1024): "))
        end_port = int(input("Enter ending port number (1-1024): "))

        if start_port < 1 or start_port > 1024 or end_port < 1 or end_port > 1024:
            print("Port must be between 1 and 1024.")
        elif end_port < start_port:
            print("End port must be greater than or equal to start port.")
        else:
            # (Step x) - After valid input    
            scanner = PortScanner(target)
            print(f"Scanning {target} from port {start_port} to {end_port}...")

            scanner.scan_range(start_port, end_port)
            open_ports = scanner.get_open_ports()

            print(f"--- Scan Results for {target} ---")
            for port, status, service in open_ports:
                print(f"Port {port}: {status} ({service})")

            print("------")
            print(f"Total open ports found: {len(open_ports)}")

            save_results(target, scanner.scan_results)

            history_choice = input("Would you like to see past scan history? (yes/no): ").strip().lower()
            if history_choice == "yes":
                load_past_scans()

    except ValueError:
        print("Invalid input. Please enter a valid integer.")



# Q5: New Feature Proposal - (2-3 sentence) 
# One extra feature I would add is a Port Risk Classifier that labels open ports as high,
# medium, or low risk. This could use nested if-statements to check the port number and
# decide which risk level it belongs to. This would help the user understand which open
# ports may need more attention.

# Diagram: See diagram_101571040.png in the repository root

