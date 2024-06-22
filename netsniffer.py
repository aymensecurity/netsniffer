import socket
import subprocess
import sys
from termcolor import colored
import colorama
from colorama import Fore, Back, Style

def scan_ports(ip, ports):
    try:
        print("\nScanning ports for {}...".format(ip))
        for port in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            result = s.connect_ex((ip, port))
            s.close()

            if result == 0:
                print(colored("[+] Port {} is open".format(port), "green"))
            else:
                print(colored("[-] Port {} is closed".format(port), "red"))

    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit()

def check_live_hosts(network):
    try:
        print("\nChecking for live hosts on {}...".format(network))
        for host in range(1, 255):
            ip = network + ".{}".format(host)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.01)

            if not s.connect_ex((ip, 135)):
                print(colored("[+] {} is live".format(ip), "green"))
            s.close()
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit()

def get_ip_from_url(url):
    try:
        ip = socket.gethostbyname(url)
        print("\nIP address of {} is: {}\n".format(url, ip))
    except socket.gaierror:
        print(colored("[-] Could not resolve hostname", "red"))

if __name__ == "__main__":
    print(colored("""
    _   __     __     _____       _ ________
   / | / /__  / /_   / ___/____  (_) __/ __/__  _____
  /  |/ / _ \/ __/   \__ \/ __ \/ / /_/ /_/ _ \/ ___/
 / /|  /  __/ /_    ___/ / / / / / __/ __/  __/ /
/_/ |_/\___/\__/   /____/_/ /_/_/_/ /_/  \___/_/
       #Coded by Aymen Ahmedin   @aymensecurity
""", "red"))

    options = """
    Options:
        1. Single port scan (separate by comma)
        2. common ports scan <-- faster
        3. All port scan
        4. Live host identification
        5. Get IP of a website
    """
    print(colored(options, "yellow"))

    choice = input("Enter your choice: ")

    if choice == '1':
        ip = input("Enter the IP address: ")
        ports = input("Enter the ports to scan (separated by commas): ").split(',')
        ports = [int(port.strip()) for port in ports]
        scan_ports(ip, ports)

    elif choice == '2':
        ip = input("Enter the IP address: ")
        ports = (80,20,21,22,23,25,53,69,7,88,135,443,587,8080,4444,8000,5900,5901,691,3306,2428,5432,6665,9929,31337)  # Scan ports 1-1000
        scan_ports(ip, ports)

    elif choice == '3':
        ip = input("Enter the IP address: ")
        ports = range(1, 10000)  # Scan ports 1-1000
        scan_ports(ip, ports)

    elif choice == '4':

        def check_host(ip):
            # Use the ping command to check if the host is reachable
            result = subprocess.call(['ping', '-c', '1', ip])

            if result == 0:
                subprocess.call(['clear'])
                print(f"{Fore.GREEN}[=] {ip} is live ")
            else:
                print(f"{Fore.RED}[x] {ip} is unreachable")

        # Get IP address range from user input
        start_ip = input("Enter the starting IP address: ")
        end_ip = input("Enter the ending IP address: ")

        # Extract the common part of the IP addresses
        common_part = '.'.join(start_ip.split('.')[:-1])

        # Iterate over the IP address range and check each host
        for i in range(int(start_ip.split('.')[-1]), int(end_ip.split('.')[-1]) + 1):
            ip = f"{common_part}.{i}"
            check_host(ip)

    elif choice == '5':
        url = input("Enter the website URL with out http : ")
        get_ip_from_url(url)

    else:
        print(colored("[-] Invalid choice. Exiting...", "red"))
