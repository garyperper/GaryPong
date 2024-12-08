#Imports
import pygame
import random
from pygame.locals import *
from PIL import Image
from Raquette import *
import tkinter as tk
from tkinter import messagebox
from Balle import *

#Set des points, et d'une variable si la partie se finit par des points
pointsgauche = 0
pointsdroite = 0
pterm = False

#initation de Pygame
pygame.init()

#initation du mixer, ainsi que load des musiques (de fond,ainsi que effets sonores) + gestion du volume
pygame.mixer.init()
pygame.mixer.music.load("./musiqueson/fond.mp3")
son_rebond_mur = pygame.mixer.Sound("./musiqueson/rebond_mur.mp3")
son_rebond_raquette = pygame.mixer.Sound("./musiqueson/rebond_tennis.mp3")
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.3)
son_rebond_mur.set_volume(1.0)  
son_rebond_raquette.set_volume(1.0)

#pour que ça tourne à 60 fps
clock = pygame.time.Clock()

#debut du gestion du décor (avec la fenetre qui s'adapte au décor)
decorPIL = Image.open("./img/terrain.jpg")
taillefen = decorPIL.size
fenetre = pygame.display.set_mode(taillefen)
pygame.display.set_caption("GaryPong !")

#création de la font
font = pygame.font.Font("./PixeloidMono.ttf", 36) 


#affichage du terrain
decor = pygame.image.load("./img/terrain.jpg").convert()
fenetre.blit(decor,(0,0))

#création et affichage des raquettes
raquette_gauche = Raquette('raquette_gauche.png',1,taillefen,1)
img_rq_gauche = pygame.image.load(raquette_gauche.getNomImage()).convert_alpha()
fenetre.blit(img_rq_gauche,raquette_gauche.getPos())
raquette_droite = Raquette('raquette_droite.png',2,taillefen,1)
img_rq_droite = pygame.image.load(raquette_droite.getNomImage()).convert_alpha()
fenetre.blit(img_rq_droite,raquette_droite.getPos())

#création de l'image de la balle
blle = Balle('balle_tennis.png',taillefen,1,0.4)
balle = pygame.image.load(blle.getNomImage()).convert_alpha()

#affichage des points
imgpointsgauche = font.render(str(pointsgauche), True, (0,0,0))
imgpointsdroite = font.render(str(pointsdroite), True, (0,0,0))
fenetre.blit(imgpointsgauche,(205,75))
fenetre.blit(imgpointsdroite,(520,75))

#gestion de la balle + affichage
fenetre.blit(balle,blle.getPos())
pygame.display.flip()


#si la boucle tourne, le programme se ferme pas
boucle = True

while boucle == True :
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            boucle = False
        
    keys = pygame.key.get_pressed()   
    
    #gestion du mouvement de la raquette gauche du J1
    if keys[pygame.K_z] :
        if raquette_gauche.getPos()[1]>0 :
            raquette_gauche.monter()
    if keys[pygame.K_s] :
        if raquette_gauche.getPos()[1]+raquette_gauche.getHauteur()<taillefen[1]:
            raquette_gauche.descendre()
    
    #gestion du mouvement de la raquette droite du J2
    if keys[pygame.K_UP] :
        if raquette_droite.getPos()[1]>0 :
            raquette_droite.monter()
    if keys[pygame.K_DOWN] :
        if raquette_droite.getPos()[1]+raquette_droite.getHauteur()<taillefen[1]:
            raquette_droite.descendre()
    
    #Pour le mouvement de la balle
    blle.mouvement()
    
    
    #Si la balle touche un mur
    if blle.getPosH() <= 0 or blle.getPosB() >= taillefen[1]:
        blle.toucherHB()
        son_rebond_mur.play()
    
    #Si la balle touche la raquette gauche, on rebondit + augmente la vitesse
    if ( raquette_gauche.getPos()[0] < blle.getPosG() < raquette_gauche.getPos()[0]+raquette_gauche.getLargeur()
        and raquette_gauche.getPos()[1] < blle.getPosB() < raquette_gauche.getPos()[1] + raquette_gauche.getHauteur()) :
        son_rebond_raquette.play()
        blle.toucherGD()
    
    #Si la balle touche la raquette droite, on rebondit + augmente la vitesse
    if (raquette_droite.getPos()[0] < blle.getPosD() < raquette_droite.getPos()[0]+raquette_droite.getLargeur()
        and raquette_droite.getPos()[1] < blle.getPosB() < raquette_droite.getPos()[1] + raquette_droite.getHauteur()) :
        son_rebond_raquette.play()
        blle.toucherGD()
    
    #Si le J2 gagne un point (car le J1 à gauche a laissé filer la balle)
    if blle.getPosG() < 0 :
        pointsdroite += 1
        blle.retourAzero()
      
    #Si le J1 gagne un point (car le J2 à droite a laissé filer la balle) 
    elif blle.getPosD() > taillefen[0] :
        pointsgauche += 1
        blle.retourAzero()
    
    #Si le J1 gagne
    if pointsgauche > 4 :
        boucle = False
        pterm = True
        gagnant = "1"
    
    #Si le J2 gagne
    elif pointsdroite > 4 :
        pterm = True
        boucle = False
        gagnant = "2"
     
    #remise à 0 de l'écran puis affichage des images
    fenetre.fill((0,0,0))
    fenetre.blit(decor,(0,0))
    fenetre.blit(img_rq_gauche,raquette_gauche.getPos())
    fenetre.blit(img_rq_droite,raquette_droite.getPos())
    fenetre.blit(balle,blle.getPos())
    imgpointsgauche = font.render(str(pointsgauche), True, (0,0,0))
    imgpointsdroite = font.render(str(pointsdroite), True, (0,0,0))
    fenetre.blit(imgpointsgauche,(205,75))
    fenetre.blit(imgpointsdroite,(520,75))
    
    #actualisation de l'écran
    pygame.display.flip()
    
    #ça tourne à 60 fps
    clock.tick(60)

#On ferme le mixer
pygame.mixer.music.stop()

#On ferme proprement Pygame    
pygame.quit()

#Si la partie s'est finie par une victoire (pas une fermeture de l'écran)
if pterm == True :
    messagebox.showinfo('Partie terminée !','Le joueur '+gagnant+' a gagné !')