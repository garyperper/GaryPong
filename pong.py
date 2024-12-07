#Imports
import pygame
import random
from pygame.locals import *
from PIL import Image
from Raquette import *
import tkinter as tk
from tkinter import messagebox


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
pygame.display.set_caption("Pyong !")

#création de la font
font = pygame.font.Font("./PixeloidMono.ttf", 36) 


#affichage du terrain
decor = pygame.image.load("./img/terrain.jpg").convert()
fenetre.blit(decor,(0,0))

#création et affichage des raquettes
raquette_gauche = Raquette('raquette_gauche.png',0,taillefen)
img_rq_gauche = pygame.image.load(raquette_gauche.getNomImage()).convert_alpha()
fenetre.blit(img_rq_gauche,raquette_gauche.getPos())
raquette_droite = Raquette('raquette_droite.png',taillefen[0]-100,taillefen)
img_rq_droite = pygame.image.load(raquette_droite.getNomImage()).convert_alpha()
fenetre.blit(img_rq_droite,raquette_droite.getPos())

#création de l'image de la balle
balle = pygame.image.load('./img/balle_tennis.png').convert_alpha()

#affichage des points
imgpointsgauche = font.render(str(pointsgauche), True, (0,0,0))
imgpointsdroite = font.render(str(pointsdroite), True, (0,0,0))
fenetre.blit(imgpointsgauche,(205,75))
fenetre.blit(imgpointsdroite,(520,75))

#gestion de la balle + affichage
taille_balle = 40
balle_x,balle_y = taillefen[0]//2,taillefen[1]//2
balle_vitessex, balle_vitessey = random.choice([1, -1]), random.choice([1, -1])
fenetre.blit(balle,(balle_x,balle_y))

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
    balle_x += balle_vitessex
    balle_y += balle_vitessey
    
    
    #Si la balle touche un mur
    if balle_y <= 0 or balle_y + taille_balle >= taillefen[1]:
        balle_vitessey = -balle_vitessey
        son_rebond_mur.play()
    
    #Si la balle touche la raquette gauche, on rebondit + augmente la vitesse
    if (balle_x+taille_balle > 0 and balle_x+taille_balle < raquette_gauche.getLargeur()
        and raquette_gauche.getPos()[1] < balle_y+taille_balle 
        and raquette_gauche.getPos()[1]+raquette_gauche.getLargeur() > balle_y+taille_balle) :
        son_rebond_raquette.play()
        if balle_vitessex < 0 :
            balle_vitessex = -(balle_vitessex-0.4)
        else :
            balle_vitessex = -(balle_vitessex+0.4)
    
    #Si la balle touche la raquette droite, on rebondit + augmente la vitesse
    if (balle_x+taille_balle > taillefen[0]-raquette_droite.getLargeur() 
        and balle_x+taille_balle < taillefen[0]
        and raquette_droite.getPos()[1] < balle_y+taille_balle 
        and raquette_droite.getPos()[1]+raquette_droite.getLargeur() > balle_y+taille_balle) :
        son_rebond_raquette.play()
        if balle_vitessex < 0 :
            balle_vitessex = -(balle_vitessex-0.4)
        else :
            balle_vitessex = -(balle_vitessex+0.4)
    
    #Si le J2 gagne un point (car le J1 à gauche a laissé filer la balle)
    if balle_x < 0 :
        pointsdroite += 1
        balle_x,balle_y = taillefen[0]//2,taillefen[1]//2
        balle_vitessex, balle_vitessey = random.choice([1, -1]), random.choice([1, -1])
      
    #Si le J1 gagne un point (car le J2 à droite a laissé filer la balle) 
    elif balle_x+taille_balle > taillefen[0] :
        pointsgauche += 1
        balle_x,balle_y = taillefen[0]//2,taillefen[1]//2
        balle_vitessex, balle_vitessey = random.choice([1, -1]), random.choice([1, -1])
    
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
    fenetre.blit(balle,(balle_x,balle_y))
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