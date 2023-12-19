import os
import sys
import shutil
import paramiko
import subprocess
from scp import SCPClient

# Define constants
HOME_PATH = "/home/nhat/Desktop"
SERVER_PATH = "/home/ubuntu"
SERVER_NAME = "ubuntu"
PRIVKEY_FILE = "rmit.pem"
CTA_PATH = os.path.join(HOME_PATH, "CTA")
LOG_PATH = os.path.join(HOME_PATH, "Logs")
SEALPIR_PATH = os.path.join(HOME_PATH, "ParallelSealPIR")
ORCHESTRATOR_PATH = os.path.join(HOME_PATH, "Orchestrator")
AWSKEY_PATH = os.path.join(HOME_PATH, "AWSkey")
PARALLEL_SEAL_PIR_PATH = os.path.join(HOME_PATH, "ParallelSealPIR")

def run_CTA(h, q):
    java_file_path = os.path.join(CTA_PATH, "CTA.java")
    gson_jar_path = os.path.join(CTA_PATH, "gson-2.10.1.jar")
    classpath = f'{gson_jar_path}:{CTA_PATH}'
    main_class_name = 'CTA'

    subprocess.run(['javac', '-cp', gson_jar_path, java_file_path], check=True) # Compile Java source code
    subprocess.run(['java', '-cp', classpath, main_class_name, str(h), str(q)], check=True)  # Run compiled Java class

def read_servers_ip():
    file_path = os.path.join(ORCHESTRATOR_PATH, 'list_servers_IPs.txt')
    try:
        with open(file_path, 'r') as file:
            ip_addresses = file.read().split()
        return ip_addresses
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []

# Sent file from local machine to server
def scp_file_from_local(server_ip, username, privkey_path, local_path, server_path):
    # Create an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the remote server
        ssh.connect(server_ip, username=username, key_filename=privkey_path)

        with SCPClient(ssh.get_transport()) as scp:
            scp.put(local_path, server_path)

        ssh.close()

        print(f"File successfully sent from {local_path} to {server_ip}:{server_path}")

    except Exception as e:
        print(f"Error transferring file from {local_path} to {server_ip}:{server_path}: {e}")

# Sent file from server to local machine
def scp_file_from_server(server_ip, username, privkey_path, local_path, server_path):
    # Create an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the remote server
        ssh.connect(server_ip, username=username, key_filename=privkey_path)

        # Use SCP to download the file from the server to the local machine
        with SCPClient(ssh.get_transport()) as scp:
            scp.get(server_path, local_path)

        # Remove the remote file after successful download
        ssh.exec_command(f"rm {server_path}")

        # Close the SSH connection
        ssh.close()

        print(f"File successfully received from {server_ip}:{server_path} to {local_path}")
        print(f"Remote file {server_path} deleted.")

    except Exception as e:
        print(f"Error transferring file from {server_ip}:{server_path} to {local_path}: {e}")

def copy_and_remove(src_path, dest_path):
    try:
        # Copy the file from source to destination
        shutil.copy(src_path, dest_path)
        print(f"File '{src_path}' copied to '{dest_path}'.")
        # Remove the original file
        os.remove(src_path)
        print(f"Original file '{src_path}' removed.")
    except FileNotFoundError:
        print(f"Error: File '{src_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Read indices from the file created by CTA
def read_indices(file_path):
    entries = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

        entry = None
        for line in lines:
            if line.startswith('TX_index:'):
                if entry is not None:
                    entries.append(entry)

                # Create a new entry
                entry = {'TX_index': int(line.split(':')[1].strip()), 'file_entries': []}
            else:
                # Extract information from lines
                parts = line.split(';')
                if len(parts) == 3:
                    file_info = {
                        'FileName': parts[0].strip(),
                        'NodeID': int(parts[1].split(':')[1].strip()),
                        'Index': int(parts[2].split(':')[1].strip())
                    }
                    entry['file_entries'].append(file_info)

        # Add the last entry if it exists
        if entry is not None:
            entries.append(entry)

    return entries

def generate_servers_list(server_ips, entries, output_file_path):
    with open(output_file_path, 'w') as file:
        for entry in entries:
            i = 0
            for file_entry in entry['file_entries']:
                server_ip = server_ips[i] if server_ips else "127.0.0.1"
                i += 1
                port_number = 3000  # You can replace this with your port number
                file_name = file_entry['FileName']
                index = file_entry['Index']

                # Write to the file
                file.write(f"{server_ip}:{port_number};{file_name};{index}\n")

    print(f"Servers_list successfully saved to {output_file_path}")

def build_parallel_SealPIR(sealpir_path):
    # Change to the project directory
    os.chdir(sealpir_path)
    # Run cmake
    subprocess.run(["cmake", "."])
    # Run make
    subprocess.run(["make"])

def run_SealPIR_client(client_path):
    # Change the current working directory to the client path
    os.chdir(client_path)
    # Run pirmessage_client
    subprocess.run(["./pirmessage_client"], check=True)
    print("pirmessage_client successfully executed")


def run_SealPIR_server(server_ip, username, privkey_path, server_path, port):
    # Create an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Connect to the remote server
    ssh.connect(server_ip, username=username, key_filename=privkey_path)

    # Run pirmessage_server on the remote server with the specified port
    command = f"cd {server_path} && ./pirmessage_server -port {port}"
    ssh.exec_command(command)

    print("pirmessage_server successfully sent and executed on the remote server")

    ssh.close()

def main_parallel_SealPIR():
    color = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
         'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    if len(sys.argv) >= 3:
        h = int(sys.argv[1])
        q = int(sys.argv[2])

        privkey_path = os.path.join(AWSKEY_PATH, PRIVKEY_FILE)

        # Run the CTA
        print("Running CTA_db: Setup Color databases...")
        run_CTA(h, q)

        # Read Servers' IP
        server_ips = read_servers_ip()
        for i in range(h):
            print("Server address: " + server_ips[i])
            local_file_path = os.path.join(CTA_PATH, f"color{color[i]}_{h}_{q}.json")
            scp_file_from_local(server_ips[i], SERVER_NAME, privkey_path, local_file_path, SERVER_PATH)

        # Read indices
        color_indices_path = os.path.join(ORCHESTRATOR_PATH, f"color_indices_{h}_{q}.txt")
        output_file_path = os.path.join(PARALLEL_SEAL_PIR_PATH, "servers_list.txt")
        entries = read_indices(color_indices_path)
        # Generate servers_list.txt
        generate_servers_list(server_ips, entries, output_file_path)

        # Build SealPIR for client and servers
        build_parallel_SealPIR(PARALLEL_SEAL_PIR_PATH)

        # Send pirmessage_server to each server
        local_file_path = os.path.join(PARALLEL_SEAL_PIR_PATH, 'pirmessage_server')
        for i in range(h):
            print("Server address: " + server_ips[i])
            scp_file_from_local(server_ips[i], SERVER_NAME, privkey_path, local_file_path, SERVER_PATH)
            # Run SealPIR Servers
            run_SealPIR_server(server_ips[i], SERVER_NAME, privkey_path, SERVER_PATH, 3000)

        #Run SealPIR Client
        run_SealPIR_client(PARALLEL_SEAL_PIR_PATH)

        # Construct remote and local file paths
        server_file_path = os.path.join(SERVER_PATH, "server_log.txt")

        # Sent logs from servers to local machine
        for i in range(h):
            local_file_path = os.path.join(LOG_PATH, f"{server_ips[i]}_color{color[i]}_{h}_{q}_log.txt")
            scp_file_from_server(server_ips[i], SERVER_NAME, privkey_path, local_file_path, server_file_path)

        # Sent log files from the source to Logs path
        src_path = os.path.join(CTA_PATH,  f"CTA_{h}_{q}_log.txt")
        dest_path = os.path.join(LOG_PATH, f"CTA_{h}_{q}_log.txt")
        copy_and_remove(src_path, dest_path)
        src_path = os.path.join(SEALPIR_PATH, "client_log.txt")
        dest_path = os.path.join(LOG_PATH, f"client_{h}_{q}_log.txt")
        copy_and_remove(src_path, dest_path)
        src_path = os.path.join(ORCHESTRATOR_PATH, f"color_indices_{h}_{q}.txt")
        dest_path = os.path.join(LOG_PATH, f"color_indices_{h}_{q}.txt")
        copy_and_remove(src_path, dest_path)

        print("Orchestration completed successfully.")
    else:
        print("Insufficient command-line arguments. Usage: python3 orchestrator.py <parameter1: (h)> <parameter2: (q)>")

if __name__ == "__main__":
    main_parallel_SealPIR()
