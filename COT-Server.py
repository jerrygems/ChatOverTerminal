import socket
import threading
import random
from collections import deque

BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
#reset colors
RESET = "\033[0m"


#clients list
client_list = []
lock = threading.Lock()

#message_history
message_history = deque(maxlen=100)

#create socket and bind
PORT = random.randint(4444,9999)
print(f"PORT:{PORT}")
HOST = '127.0.0.1'
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind((HOST,PORT))

#listening
sock.listen()
print("server started listening for connections\n[LISTENING...]")

def MSG_Spreader(msg,senders_socket,senders_addr,senders_uname):
	with lock:
		try:
			print("worked")
			prompt = f"{senders_uname if senders_uname else senders_addr}@CYBER_SOCIETY => {msg}"
			message_history.append(prompt)
			for client in client_list:
				print("workedd")
				if client["socket"] != senders_socket and client["client-name"] and client["authorized"]:
					client_sock = client["socket"]
					client_username = client["client-name"]
					if client_sock != senders_socket:
						client_prompt = f"\r{prompt}\n{GREEN}{client_username}@CYBER_SOCIETY => {RESET}"
						client_sock.sendall(client_prompt.encode())
					elif not client["authorized"]:
						# Send message history to the newly connected client
						for message in message_history:
							client_sock.sendall(message.encode())
						client["authorized"] = True

		except Exception as e:
			print(f"{RED}[EXCEPTION HAS OCCURRED: while broadcasting]{e}{RESET}")

def authenticator(client_sock):
	client_sock.sendall(f"{GREEN}[ENTER YOUR PASSPHRASE] => {RESET}".encode())
	client_pass = client_sock.recv(1024).decode().strip()
	if client_pass == "ls":
		client_sock.sendall(f"{GREEN}Password Accepted{RESET}\n".encode())
		return True
	else:
		client_sock.sendall(f"{GREEN}Password Denied{RESET}\n".encode())
		return False


def isNameAvailable(arg1):
	for client in client_list:
		if client["client-name"] == arg1:
			return False
	return True

def client_handler(client_sock,client_addr):

	client_name=None
	client_sock.sendall(f"{GREEN}[ENTER YOUR USERNAME] => {RESET}".encode())
	client_name = client_sock.recv(1024).decode().strip()
	if len(client_name) <= 30:
		if isNameAvailable(client_name):
			with lock:
				client_list.append({"socket":client_sock,"client-name":client_name,"authorized":True})

			for message in message_history:
				client_sock.sendall(message.encode())

			while True:
				try:
					#implementations
					client_sock.sendall(f"{GREEN}{client_name}@CYBER_SOCIETY => {RESET}".encode())
					data = client_sock.recv(1024)
					if not data:
						break

					msg = data.decode()
					print(f"{client_name}@CYBER_SOCIETY =>{msg}")

					if msg.strip()=="$exit":
						break
					
					MSG_Spreader(msg,client_sock,client_addr,client_name)
				except Exception as e:
					print(f"{RED}[EXCEPTION HAS OCCURRED: in While loop after username stuff]{e}{RESET}")
		else:
			client_sock.sendall(f"{RED}[SORRY BUT USERNAME NOT AVAILABLE]{RESET}".encode())
	else:
		client_sock.sendall(f"{RED}[USERNAME WITH MORE THAN 30 LETTERS ARE NOT ALLOWED]{RESET}".encode())
	client_sock.close()
		
#here is the main stuff

while True:
	try:
		client_sock, client_addr = sock.accept()
		print(f"Connected to {client_sock}")
		client_sock.sendall(f"""{RED}
   ___ _           _       ___                   _____                    _             _ 
  / __\ |__   __ _| |_    /___\__   _____ _ __  /__   \___ _ __ _ __ ___ (_)_ __   __ _| |
 / /  | '_ \ / _` | __|  //  //\ \ / / _ \ '__|   / /\/ _ \ '__| '_ ` _ \| | '_ \ / _` | |
/ /___| | | | (_| | |_  / \_//  \ V /  __/ |     / / |  __/ |  | | | | | | | | | | (_| | |
\____/|_| |_|\__,_|\__| \___/    \_/ \___|_|     \/   \___|_|  |_| |_| |_|_|_| |_|\__,_|_|
                                                                                          
			\n{RESET}""".encode())
		isAuth = authenticator(client_sock)
		if isAuth:
			client_thread = threading.Thread(target=client_handler, args=(client_sock, client_addr))
			client_thread.start()
		else:
			print(f"authentication failed {client_sock}")
			client_sock.close()
	except Exception as e:
			print(f"{RED}[EXCEPTION HAS OCCURRED: in while loop that was for accepting connections]{e}{RESET}")
