#!/usr/bin/python3
#T. Flayols - B. Vandeportaele 
# Simulateur de robot kuka, demande d'ordre de mouvement
import socket
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 15000        # The port used by the server
#######################################""
def send(s,chaine):
	s.sendall(chaine)
	print('envoi: '+chaine.decode('utf-8'))
#######################################""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    send(s,b'reinit') #reinitialisation
    time.sleep(1)
    send(s,b'app 0') #apprentissage face 0 ...
    time.sleep(1)
    send(s,b'app 5') #jusqu'à apprentissage face 5 ...
    time.sleep(1)
    while True:
      send(s,b'getmove')
      time.sleep(1)
      data = s.recv(1024)
      print('Received', repr(data))
      if data==b'END':
        print("fini!")
        break
