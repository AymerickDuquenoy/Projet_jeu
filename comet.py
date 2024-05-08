import pygame
import random


#créer une classe pour gérer cette comet 
class Comet(pygame.sprite.Sprite) : 
    
    def __init__(self, comet_event): 
        super().__init__()
        # definir l'image associée à cette comette
        self.image = pygame.image.load('assets/comet.png')
        self.rect = self.image.get_rect()
        self.velocity = random.randint(3, 5)
        self.rect.x = random.randint(20, 800)
        self.rect.y = - random.randint(0, 800)
        self.comet_event = comet_event
        
    def remove(self) : 
        self.comet_event.all_comets.remove(self)
        #jouer le son 
        self.comet_event.game.sound_manager.play('meteorite')
        
        #verifier si le nombre de comettes est de 0
        if len(self.comet_event.all_comets) == 0 :
            print("L'evenement est fini")
            # remettre la barre à 0 
            self.comet_event.reset_percent()
            # apparaitre les 2 premiers monstre 
            self.comet_event.game.start()
             
    def fall(self,screen) : 
        self.rect.y += self.velocity
        # ne tombe pas sur le sol 
        if self.rect.y >= 500 : 
            print("sol")
            #retirer la boule de feu 
            self.remove()
            
            # si il n'y a plus de boule de feu
            if len(self.comet_event.all_comets) == 0 : 
                print("L'evenement est fini")
                # remettre la jauge au départ
                self.comet_event.reset_percent()
                self.comet_event.fall_mode = False 
            
        # verifier si la boule de feu touche le joueur
        if self.comet_event.game.check_collision(self,self.comet_event.game.all_players) : 
            print("Joueur touché !")
            self.remove()
            #subir 20 points de degats
            self.comet_event.game.player.damage(20,screen)
            