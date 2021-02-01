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
map_moveToCodeCmd = {'FCW':"0\r\n",'FCCW':"1\r\n",'UCW':"2\r\n",'UCCW':"3\r\n",'MCW':"4\r\n",'MCCW':"5\r\n", 'END':"100\r\n"}
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

#HOSTSERVER = '127.0.0.1'  # The server's hostname or IP address
HOSTSERVER = '192.168.3.11'  # The server's hostname or IP address
PORT = 30000        # The port used by the server

global activateDisplay
#option -d pour affichage dans graphique dans fenetre, désactivé par défaut
#activateDisplay=False
#pour debug
activateDisplay=True        

#######################################

def communicationThread():
  global activateDisplay
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
                  #faceColorStr = str(data).replace(' ','').replace("b",'').replace("r","").replace("\\","").replace("'","").replace("]","").replace("[","").replace(".0","")
                  faceColorStrNum = str(data).replace(' ','').replace("b",'').replace("r","").replace("\\","").replace("'","").replace("]","").replace("[","").replace(".0","")
                  faceColorStr = faceColorStrNum

                  for i in range(6):
                    faceColorStr = faceColorStr.replace(str(i),colorsCode[i]);
                  faceColorStrNum=list(faceColorStrNum) #transforme la chaine en liste de caractères
                  faceColorStrNum=[int(i) for i in faceColorStrNum] #transforme chaque caractère en une valeur int
                  #print(faceColorStrNum)

                  if len(faceColorStr) == 9:
                    if listMoves[indiceMoves]=='Y':
                      yellowFace = faceColorStr
                      if activateDisplay: drawFace(3,0,sc,img,faceColorStrNum,listeRGB)
                    elif listMoves[indiceMoves]=='B':
                      blueFace = faceColorStr
                      if activateDisplay: drawFace(0,3,sc,img,faceColorStrNum,listeRGB)
                    elif listMoves[indiceMoves]=='R':
                      redFace = faceColorStr
                      if activateDisplay: drawFace(3,3,sc,img,faceColorStrNum,listeRGB) 
                    elif listMoves[indiceMoves]=='G':
                      greenFace = faceColorStr
                      if activateDisplay: drawFace(6,3,sc,img,faceColorStrNum,listeRGB)    
                    elif listMoves[indiceMoves]=='O':
                      orangeFace = faceColorStr
                      if activateDisplay: drawFace(9,3,sc,img,faceColorStrNum,listeRGB)     
                    elif listMoves[indiceMoves]=='W':
                      whiteFace = faceColorStr
                      if activateDisplay: drawFace(3,6,sc,img,faceColorStrNum,listeRGB)        
                      
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
        
                #send(c,listMoves[indiceMoves].encode('utf-8'))
                send(c,map_moveToCodeCmd[listMoves[indiceMoves]].encode('utf-8'))
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
                      
#######################################           
def animationThread():
  #pour debug
  time.sleep(1)
  drawSquare(6,4,sc,img,(255,0,0))
  time.sleep(1)
  drawSquare(8,2,sc,img,(0,0,255))
  time.sleep(1)
  drawFace(3,0,sc,img,[0,1,2,3,4,5,0,1,2],listeRGB)
  time.sleep(1)
  drawFace(0,3,sc,img,[0,0,0,0,0,0,0,0,0],listeRGB)
  time.sleep(1)
  drawFace(3,3,sc,img,[5,5,5,0,0,0,0,0,0],listeRGB)
  time.sleep(1)
  drawFace(6,3,sc,img,[5,5,5,0,0,0,0,0,0],listeRGB)
  time.sleep(1)
  drawFace(9,3,sc,img,[0,0,0,0,0,0,0,0,0],listeRGB)
  time.sleep(1)
  drawFace(3,6,sc,img,[5,5,5,0,0,0,0,0,0],listeRGB)

#######################################
sc=30 #taille en pixel d'un coté de carré

def drawFace(indx,indy,sc,img,listcol,listeRGB):
    for y in range(0,3):
      for x in range(0,3):
            col=listeRGB[listcol[x+y*3]]
            print('x: '+str(x)+' , y: '+str(y)+' , ind: '+str(listcol[x+y*3])+' , col: '+ str(col))
            drawSquare(indx+x,indy+y,sc,img,col)
                
def drawSquare(indx,indy,sc,img,col):
    for x in range(indx*sc,(indx+1)*sc):
        for y in range(indy*sc,(indy+1)*sc):
            img[y][x]=col
            
import sys
if len(sys.argv)==2:
    if sys.argv[1]=='-d':
        activateDisplay=True

if activateDisplay:
    from threading import Thread
    import cv2 as cv
    import numpy as np        
    listeRGB=[] #chargement des couleurs des faces depuis fichier
    filedata = np.genfromtxt('listecolors.out', delimiter=',').astype('uint8')
    for i in range(0,6): listeRGB.append(filedata[i]) 
    print(listeRGB)     
    img = np.zeros((3*sc*3,3*sc*4,3), np.uint8)
    #lance une thread pour raffraichir périodiquement l'affichage avec les données entrantes
    print('démarre thread')
    t=Thread(target=communicationThread,args=())
    #pour debug
    #t=Thread(target=animationThread,args=())
    t.start()
    while(True):
      cv.imshow('image',img)
      if cv.waitKey(20) & 0xFF==ord("q"):
        cv.destroyAllWindows()
        sys.exit()  #violent, mais au moins tue la thread de communication, libérant la socket
else:
#lancement sans affichage
  communicationThread()
#######################################
          
          

