#!/usr/bin/python3
#B. Vandeportaele 2020

#https://realpython.com/python-sockets/

import socket
import time

#######################################
def send(s,chaine):
	s.sendall(chaine)
	print('envoi: '+chaine.decode('utf-8'))
#######################################

listMoves=['FCW','FCCW','UCW','UCCW','MCW','MCCW','END']

indiceMoves=0


with  socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  host = ""
  port = 15000
  #pour éviter l'empechement de réutiliser la socket après fermeture brutale de l'appli par CTRL C
  #https://stackoverflow.com/questions/27360218/how-to-close-socket-connection-on-ctrl-c-in-a-python-programme
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind((host, port)) # premier champ vide pour recevoir depuis n'importe quelle adresse,sinon IP en chaine de caractères
  print("socket binded to port", port)
  # put the socket into listening mode
  s.listen(5)
  print("socket is listening")
  # a forever loop until client wants to exit
  #finished=False
  while True:
    # establish connection with client
    c, addr = s.accept()
    # lock acquired by client
    # print_lock.acquire()
    print('Connected to :', addr[0], ':', addr[1])
    # Start a new thread and return its identifier
    #_thread.start_new_thread(self.threaded, (c,))
    #a priori un seul client, pas besoin de thread
    while True:
      # data received from client
      data = c.recv(1024)
      print("receving " + str(data))
      if not data:
        print('Bye')
        # lock released on exit
        # print_lock.release()
        break  # sort du while -> déconnexion
      
      # décodage de la requete: format r n1 n2...
      listfields = data.split()
      print(str(listfields))
      if listfields[0]==b'getmove':
        print('GETMOVE')
        send(c,listMoves[indiceMoves].encode('utf-8'))
        if listMoves[indiceMoves]=='END':
                print('FINI')
                c.close()
                #finished=True
                break
        indiceMoves+=1
      elif listfields[0]==b'reinit':
        print('REINITIALISATION')
        indiceMoves=0
      elif listfields[0]==b'app':
        print('APPRENTISSAGE FACE '+str(listfields[1]))
  #jamais exécuté en fait: 
  print('fermeture socket s')
  s.close()               
   
   

