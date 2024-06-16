import os
import sys
import socket
from platform import system
from scapy.all import IP, ICMP, sr1

TIMEOUT = 2


def is_ip_valid(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


def check_availability(ip):
    platform = system().lower()
    # Нижеописанная проверка излишня, если запускать из скрипт из докер контейнера
    # Она будет полезна, если запускать скрипт из bare железа
    if platform == "windows":
        cmd = f"ping -n 1 {ip}"
    else:
        cmd = f"ping -c 1 {ip}"

    resp = os.system(cmd + " > /dev/null 2>&1")
    return resp == 0


def is_icmp_blocked(ip):
    packet = IP(dst=ip, flags="DF") / ICMP() / "X"
    resp = sr1(packet, timeout=TIMEOUT, verbose=0)
    return resp is None


def is_ping_ok(target, size):
    packet = IP(dst=target, flags="DF") / ICMP() / ("X" * size)
    resp = sr1(packet, timeout=TIMEOUT, verbose=0)
    return resp is not None and (
        not resp.haslayer(ICMP)
        or resp.getlayer(ICMP).type != 3
        or resp.getlayer(ICMP).code != 4
    )


def get_ip(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)


def bin_search(target):
    mx = 10000  # обычно = 1500 - 28 = 1472
    mn = 1

    while mn < mx:
        mid = (mn + mx) // 2

        if is_ping_ok(target, mid):
            mn = mid + 1
        else:
            mx = mid - 1
    return mn - 1


def main():
    if len(sys.argv) != 2:
        print("Usage: python find_mtu.py <target_ip_or_domain>")
        sys.exit(1)

    target = sys.argv[1]

    if is_ip_valid(target):
        target_ip = target
    else:
        target_ip = get_ip(target)
        if target_ip is None:
            print("Error: Can not resolve domain to IP address.")
            sys.exit(1)
    print(f"Target IP: {target_ip}")

    if not check_availability(target_ip):
        print("Error: Target is not reachable.")
        sys.exit(1)
    print("Target availability: reachable")

    if is_icmp_blocked(target_ip):
        print("Error: ICMP requests to the target are blocked.")
        sys.exit(1)
    print("ICMP: not blocked")

    try:
        mss = bin_search(target_ip)
        print(f"Result MTU: {mss + 28} bytes (MSS {mss} + 28 bytes in headers)")
    except PermissionError:
        print("Error: Permission denied (Try running as root)")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)


if __name__ == "__main__":
    main()
