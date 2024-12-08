from PIL import Image

class Raquette:
    
    def __init__(self,nomImage:str,joueur:int,dimfen:tuple,vitesse:int) :
        self.__nomImage = './img/'+str(nomImage)
        imgPIL = Image.open(self.__nomImage)
        self.__hauteur = imgPIL.size[1]
        self.__largeur = imgPIL.size[0]
        if joueur == 1 :
            self.__posx = 0
        elif joueur == 2 :
            self.__posx = dimfen[0] - self.__largeur
        else :
            raise Exception('Numéro de joueur invalide !')
        self.__posy = dimfen[1]//2
        self.__vitesse = vitesse
        return None
    
    def getPos(self) :
        return (self.__posx,self.__posy)
    
    def getNomImage(self):
        return self.__nomImage
    
    def monter(self) :
        self.__posy -= self.__vitesse
        return None
    
    def descendre(self) :
        self.__posy += self.__vitesse
        return None
    
    def getHauteur(self):
        return self.__hauteur
    
    def getLargeur(self):
        return self.__largeur