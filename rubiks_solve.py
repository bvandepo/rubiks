#!/usr/bin/python3
#B. Vandeportaele 2020
#T. Flayols 2020

#https://realpython.com/python-sockets/

import socket
import time
from IPython import embed
import rubiks_utils
#######################################
def send(s,chaine):
  s.sendall(chaine)
  print('envoi: '+chaine.decode('utf-8'))
#######################################

#mouvements utilisés pour l'apprentissage 
#le rubiks est posé avec la face jaune au centre de la face supérieure
initListMoves=['Y','FCW','UCW','B','FCW','O','FCW','G','FCW','R','FCW','UCW','FCCW','W','FCW','FCW','UCW','UCW']

#init
listMoves=initListMoves
indiceMoves=0

#Corespondance code entier vers couleur (d'apres tcv4.py)
colorsCode = ["b","r","w","g","o","y"]

yellowFace = "yyyyyyyyy"
blueFace = "bbbbbbbbb"
redFace = "rrrrrrrrr"
greenFace = "ggggggggg"
orangeFace = "ooooooooo"
whiteFace = "wwwwwwwww"

#######################################

HOSTSERVER = '127.0.0.1'  # The server's hostname or IP address
PORT = 30000        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
        serversocket.connect((HOSTSERVER, PORT))
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
                if indiceMoves>=len(listMoves) or listMoves[indiceMoves]=='END':
                        print('envoi de '+str(listMoves[indiceMoves]))
                        send(c,listMoves[indiceMoves].encode('utf-8'))
                        print('FINI')
                        c.close()
                        #finished=True
                        break        
                if len(listMoves[indiceMoves])==1: #il faut apprendre une face
                  #apprentissage
                  print('APPRENTISSAGE FACE '+listMoves[indiceMoves])
                  serversocket.sendall(b'r 100 101 102 103 104 105 106 107 108')               
                  data = serversocket.recv(1024)
                  print('Received', repr(data))
                  faceColorStr = str(data).replace(' ','').replace("b",'').replace("r","").replace("\\","").replace("'","").replace("]","").replace("[","").replace(".0","")
                  for i in range(6):
                    faceColorStr = faceColorStr.replace(str(i),colorsCode[i]);
                  if len(faceColorStr) == 9:
                    if listMoves[indiceMoves]=='Y':
                      yellowFace = faceColorStr
                    elif listMoves[indiceMoves]=='B':
                      blueFace = faceColorStr
                    elif listMoves[indiceMoves]=='R':
                      redFace = faceColorStr
                    elif listMoves[indiceMoves]=='G':
                      greenFace = faceColorStr
                    elif listMoves[indiceMoves]=='O':
                      orangeFace = faceColorStr
                    elif listMoves[indiceMoves]=='W':
                      whiteFace = faceColorStr
                      
                  if listMoves[indiceMoves]=='W': #Toute les faces ont été vues
                    #Resolution du rubiks cube
                    cubeInitialState = yellowFace + blueFace + redFace + greenFace + orangeFace + whiteFace
                    print("solving cube: {}...".format(cubeInitialState))
                    #time.sleep(10)
                    solutionMoves=rubiks_utils.solve(cubeInitialState)
                    listMoves.extend(solutionMoves) #Add all moves to save the rubiks cube
                    listMoves.append('END')
                    print(str(listMoves))
                  indiceMoves+=1
                #listMoves[indiceMoves] est forcement un mouvement
                print('envoi de '+str(listMoves[indiceMoves]))
                send(c,listMoves[indiceMoves].encode('utf-8'))
                indiceMoves+=1
              elif listfields[0]==b'reinit':
                print('REINITIALISATION')
                indiceMoves=0
                listMoves=initListMoves
              #elif listfields[0]==b'app':
              #  print('APPRENTISSAGE FACE '+str(listfields[1]))

          #jamais exécuté en fait: 
          print('fermeture socket s')
          s.close()               
           
           

