

import socket
import ipaddress
from datetime import datetime

# Terminal colors
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Common port names
port_names = {
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL",
    8000: "Development Server",
    8080: "HTTP Alternative"
}


# Function to check a port
def check_port(ip, port):

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            result = s.connect_ex((ip, port))
            return result == 0

    except OSError:
        return False


# Function to save report
def save_report(ip, scan_results, open_ports, closed_ports):

    with open("scan_report.txt", "w") as file:

        file.write("PORT STATUS CHECKER REPORT\n")
        file.write("===========================\n")
        file.write(f"Date and Time: {datetime.now()}\n")
        file.write(f"Target IP: {ip}\n\n")

        file.write("SCAN RESULTS\n")
        file.write("------------\n")

        for result in scan_results:
            file.write(result + "\n")

        file.write("\nSUMMARY\n")
        file.write("-------\n")
        file.write(f"Open Ports: {open_ports}\n")
        file.write(f"Closed/Unreachable Ports: {closed_ports}\n")

    print(GREEN + "\nReport saved successfully!" + RESET)


# Welcome screen
def welcome():

    print(CYAN + "=" * 45)
    print("          PORT STATUS CHECKER")
    print("             CYBER SECURITY")
    print("=" * 45 + RESET)


# Main program
def main():

    welcome()

    try:

        # Get IP address
        ip = input("\nEnter IP Address: ").strip()

        # Validate IPv4 address
        ipaddress.IPv4Address(ip)

        print(YELLOW + "\n1. Check Single Port")
        print("2. Scan Common Ports" + RESET)

        choice = input("\nEnter your choice: ").strip()

        scan_results = []
        open_ports = 0
        closed_ports = 0

        # Single port scanning
        if choice == "1":

            port = int(input("Enter port number: "))

            if not 1 <= port <= 65535:
                print(RED + "Invalid port number!" + RESET)
                return

            print(YELLOW + "\nChecking port..." + RESET)

            if check_port(ip, port):

                print(GREEN + f"Port {port} is OPEN" + RESET)
                scan_results.append(f"Port {port}: OPEN")
                open_ports += 1

            else:

                print(RED + f"Port {port} is CLOSED or UNREACHABLE" + RESET)
                scan_results.append(
                    f"Port {port}: CLOSED or UNREACHABLE"
                )
                closed_ports += 1

        # Multiple port scanning
        elif choice == "2":

            print(CYAN + "\nSCANNING STARTED")
            print("-" * 45 + RESET)

            for port, service in port_names.items():

                status = check_port(ip, port)

                if status:

                    print(GREEN + f"{port} - {service}: OPEN" + RESET)
                    scan_results.append(
                        f"{port} - {service}: OPEN"
                    )
                    open_ports += 1

                else:

                    print(RED + f"{port} - {service}: CLOSED/UNREACHABLE" + RESET)
                    scan_results.append(
                        f"{port} - {service}: CLOSED/UNREACHABLE"
                    )
                    closed_ports += 1

        else:

            print(RED + "Invalid choice!" + RESET)
            return

        # Display summary
        print(YELLOW + "\n" + "=" * 45)
        print("                 SCAN SUMMARY")
        print("=" * 45 + RESET)

        print(GREEN + f"Open Ports: {open_ports}" + RESET)
        print(RED + f"Closed/Unreachable Ports: {closed_ports}" + RESET)

        print(CYAN + "\nScanning Completed!" + RESET)

        # Save report automatically
        save_report(ip, scan_results, open_ports, closed_ports)

    except ValueError:

        print(RED + "Invalid IP address or port number!" + RESET)

    except OSError:

        print(RED + "Network error occurred!" + RESET)


# Run the program
if __name__ == "__main__":
    main()

    print("\nThank you for using Port Status Checker!")
