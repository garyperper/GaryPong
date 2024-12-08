from PIL import Image
import random


class Balle:
    
    def __init__(self,nomImage:str,dimfen:tuple,vitessebase:int,acc:float) :
        self.__nomImage = './img/'+str(nomImage)
        imgPIL = Image.open(self.__nomImage)
        self.__dimfen = dimfen
        self.__taille = imgPIL.size
        self.__posx = self.__dimfen[0]//2
        self.__posy = self.__dimfen[1]//2
        self.__vitessebase = [vitessebase,-vitessebase]
        self.__ballevitessex,self.__ballevitessey = random.choice(self.__vitessebase), random.choice(self.__vitessebase)
        self.__acc = acc
        return None
    
    def getPosG(self):
        return self.__posx
    
    def getPosD(self):
        return self.__posx+self.__taille[0]

    def getPosH(self):
        return self.__posy
    
    def getPosB(self):
        return self.__posy+self.__taille[1]

    def getPos(self):
        return(self.__posx,self.__posy)
    
    def toucherHB(self) :
        self.__ballevitessey = -self.__ballevitessey
        return None
    
    def toucherGD(self) :
        if self.__ballevitessex < 0 :
            self.__ballevitessex = -(self.__ballevitessex-0.4)
        else :
            self.__ballevitessex = -(self.__ballevitessex+0.4)
        return None
    
    def retourAzero(self):
        self.__posx = self.__dimfen[0]//2
        self.__posy = self.__dimfen[1]//2
        self.__ballevitessex,self.__ballevitessey = random.choice(self.__vitessebase), random.choice(self.__vitessebase)
        return None
    
    def getNomImage(self):
        return self.__nomImage
    
    def mouvement(self):
        self.__posx += self.__ballevitessex
        self.__posy += self.__ballevitessey