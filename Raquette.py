import pygame
from PIL import Image

class Raquette:
    
    def __init__(self,nomImage,x,dimfen) :
        self.__nomImage = './img/'+str(nomImage)
        self.__posx = x
        imgPIL = Image.open(self.__nomImage)
        self.__hauteur = imgPIL.size[1]
        self.__largeur = imgPIL.size[0]
        self.__posy = dimfen[1]//2
        return None
    
    def getPos(self) :
        return (self.__posx,self.__posy)
    
    def getNomImage(self):
        return self.__nomImage
    
    def monter(self) :
        self.__posy -= 1
        return None
    
    def descendre(self) :
        self.__posy += 1
        return None
    
    def getHauteur(self):
        return self.__hauteur
    
    def getLargeur(self):
        return self.__largeur