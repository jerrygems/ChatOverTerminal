import socket
import threading
import random



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


PORT = random.randint(1000, 9999)
print(f"PORT:{PORT}")
#clients list
client_list = []
lock = threading.Lock()

#create socket and bind
HOST = '127.0.0.1'
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind((HOST,PORT))

#listening
sock.listen()
print("server started listening for connections\n[LISTENING...]")

def MSG_Spreader(msg,senders_socket,senders_addr,senders_uname):
	with lock:
		try:
			for client in client_list:
				if client["socket"] != senders_socket:
					client_sock = client["socket"]
					client_username = client["username"]
					prompt = f"{senders_uname if senders_uname else senders_addr}@CYBER_SOCIETY => {msg}"
					client_prompt = f"\r{prompt}\n{GREEN}{client_username}@CYBER_SOCIETY => {RESET}"
					client_sock.sendall(client_prompt.encode())
		except Exception as e:
			print(f"{RED}[EXCEPTION HAS OCCURRED: while broadcasting]{e}{RESET}")

def client_handler(client_sock,client_addr):
	with lock:
		client_list.append({"socket":client_sock,"username":None})
	auth = False
	received_uname=None
	while not auth:
		client_sock.sendall(f"{GREEN}[ENTER YOUR USERNAME] => {RESET}".encode())
		received_uname = client_sock.recv(1024).decode().strip()
		try:
			if any(user["username"] == received_uname for user in client_list):
				client_sock.sendall(f"{GREEN}[USERNAME ALREADY TAKEN] {RESET}".encode())
				received_uname=None
			else:
				try:
					for client in client_list:
						if client["socket"]==client_sock:
							client["username"] = received_uname

					var1 = f"{GREEN}[YOUR USERNAME IS {received_uname}]{RESET}\n"
					client_sock.sendall(var1.encode())

					client_sock.sendall(f"{GREEN}[ENTER THE PASSPHRASE FOR GROUP] => {RESET}".encode())
					received_pass = client_sock.recv(1024).decode().strip()
					if received_pass == "COT":
						auth = True
						client_sock.sendall(f"{GREEN}Password Accepted{RESET}\n".encode())
					else:
						client_sock.sendall(f"{GREEN}Password Incorrect, Please Enter The Correct PASSWORD{RESET}\n".encode())
				except Exception as e:
					print(f"{RED}[EXCEPTION HAS OCCURRED: while handling else part condition]{e}{RESET}")

		except Exception as e:
			print(f"{RED}[EXCEPTION HAS OCCURRED: while handling]{e}{RESET}")
		

	while True:
		
		try:
			client_sock.sendall(f"{GREEN}{received_uname}@CYBER_SOCIETY => {RESET}".encode())
			data = client_sock.recv(1024)
			if not data:
				break
			msg = data.decode()
			print(f"{received_uname}@CYBER_SOCIETY =>{msg}")
			
			MSG_Spreader(msg,client_sock,client_addr,received_uname)
		except Exception as e:
			print(f"{RED}[EXCEPTION HAS OCCURRED: in While loop after authentication stuff]{e}{RESET}")
		
#here is the main stuff

while True:
	try:
		client_sock, client_addr = sock.accept()
		print(f"Connected to {client_sock}")

		client_thread = threading.Thread(target=client_handler, args=(client_sock, client_addr))
		client_thread.start()
	except Exception as e:
			print(f"{RED}[EXCEPTION HAS OCCURRED: in while loop that was for accepting connections]{e}{RESET}")
