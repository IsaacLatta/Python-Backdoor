# Python-Backdoor

## Disclaimer

This project is for educational purposes only. It is designed to understand and learn about network security, penetration testing, and the functioning of reverse shells. Unauthorized use of this software against any devices or networks without explicit permission is illegal. The developer assumes no liability and is not responsible for any misuse or damage caused by this program.

## Description

Python-Backdoor is a reverse shell backdoor tool designed to demonstrate and practice concepts of network security and penetration testing. It allows for remote command execution, taking screenshots, uploading/downloading files, and executing some basic system commands. The backdoor ensures persistence through a `while True` loop, attempting to reconnect to the server every 20 seconds, ensuring that the connection can be re-established automatically without manual intervention unless the `abort` command is sent.

## Features

- **Reverse Shell**: Gain command line access to the target system.
- **File Upload/Download**: Transfer files to/from the target system.
- **Screenshots**: Capture screenshots of the target system.
- **Persistence**: Automatic reconnection attempt every 20 seconds, backdoor may be killed via the 'abort' command.
- **Basic Command Execution**: Perform system commands remotely.

## Requirements

- Python 3.x

## Installation

1. Clone this repository to your local machine;  https://github.com/IsaacLatta/Python-Backdoor.git
2. Run the scripts via "python3 server.py" and "python3 backdoor.py".

## Usage

### Server Setup

1. Configure the `SERVER_IP` variable at the beginning of the server.py script to the IP address of the machine that will be listening for connections.

### Client Setup

1. Configure the `SERVER_IP` variable at the beginning of the backdoor.py script to the IP address of the machine that will be listening for connections.
2. Deploy the client script to the target system.
3. The backdoor will attempt to connect to the server every 20 seconds, unless killed via trhe 'abort' command

### Commands

- `screenshot`: Capture a screenshot of the target system.
- `upload filename`: Upload a file to the target system.
- `download filename`: Download a file from the target system.
- `quit` : Exit the shell and close connection
- `abort`: Terminate the connection and stop the backdoor.

## Legal Notice

This project is a demonstration developed to teach ethical hacking and network security. It should only be deployed in environments where explicit permission has been granted. Misuse of this software can lead to criminal charges brought against the individuals in question. Consult your local laws and regulations before using this software.


