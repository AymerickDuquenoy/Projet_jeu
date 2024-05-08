import pygame
from player import Player
from monster import Monster
from comet_event import CometFallEvent
from monster import Mummy, Alien
from sounds import SoundManager
pygame.init() 

#creer une seconde classe qui va representer notre jeu 
class Game: 
    def __init__(self) :
        #definir si notre jeu a commencé ou non 
        self.is_playing = False
        #definir sur on est sur le tuto ou non 
        self.rules = False
        #generer notre joueur 
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        #generer l'evenement 
        self.comet_event = CometFallEvent(self)
        #groupe de monstre
        self.all_monsters =pygame.sprite.Group()
        self.pressed = {}
        #mettre le score à 0
        self. font = pygame.font.Font("assets/my_custom_font.ttf", 25)
        self.score = 0
        # gerer le son 
        self.sound_manager = SoundManager()
        #Gestion du score a la fin
        self.score_statu = False
        self.high_score = 0
        
    # afficher score fin de partie 
    def end_score(self,screen) : 
        end_text = self.font.render(f"Score: {self.score} ", 1, (0, 0, 0))
        text = self.font.render("Appuie sur espace pour continuer.",1,(0,0,0))
        high_score = self.font.render(f"votre score max : {self.high_score}", 1, (0,0,0))
        screen.blit(end_text, (300,300))
        screen.blit(text, (300,360))
        screen.blit(high_score, (300,330))
    
    def add_score(self, point = 10):
        self.score += point
        
    def game_over(self,screen) :
        #remettre le jeu à neuf, retirer les monstres, remettre le joueur a 100 de vie, jeu en attente 
        self.all_monsters = pygame.sprite.Group()
        self.comet_event.all_comets = pygame.sprite.Group()
        self.comet_event.reset_percent()
        self.player.health = self.player.max_health
        # jouer le son
        self.sound_manager.play('game_over')
        self.score_statu = True
        
        # changement du score max a la fin si supérieur a l'ancien 
        if self.score > self.high_score : 
            self.high_score = self.score
        
        

    

    def start(self) : 
        self.is_playing = True
        self.spawn_monster(Mummy)
        self.spawn_monster(Mummy)
        self.spawn_monster(Alien)
 
        
        
    def rule(self, screen) : 
        self.rules = True
        regle = self.font.render("Vous devez tuer des monstres pour gagner des points. ", 1,(0,0,0))
        mouvement_droite = self.font.render("Pour vous déplacer à droite appuyé sur : >",1,(0,0,0))
        mouvement_gauche = self.font.render("Pour vous déplacer à gauche appuyé sur : <",1,(0,0,0))
        tire= self.font.render("Pour tirer, appuyer sur : espace.", 1,(0,0,0))
        screen.blit(regle,(200,200))
        screen.blit(mouvement_droite,(200,240))
        screen.blit(mouvement_gauche,(200,280))
        screen.blit(tire,(200,320))
        
        
    def update(self,screen) : 
        # afficher le score sur l'ecran
        score_text = self.font.render(f"Score: {self.score} ", 1, (0, 0, 0))
        screen.blit(score_text, (20,20))
        
        # appliquer l'image de mon joueur 
        screen.blit(self.player.image,self.player.rect)
        
        #actualiser la barre de vie du joueur 
        self.player.update_health_bar(screen)
        
        #actualiser animation du joueur 
        self.player.update_animation()
        
        #actualiser la barre d'evenement du jeu 
        self.comet_event.update_bar(screen)
        
        #appliquer l'ensemble des images de mon groupe de monstre
        self.all_monsters.draw(screen)
        
        #recuperer les projectiles du joueur
        for projectile in self.player.all_projectiles:
            projectile.move()
            
        #recuperer les monstres de notre jeu 
        for monster in self.all_monsters:
            monster.forward(screen)
            monster.update_health_bar(screen)
            monster.update_animation()
            
        # recuperer les comets de notre jeu 
        for comet in self.comet_event.all_comets:
            comet.fall(screen)
        
        #appliquer l'ensemble des images de mon groupe de projectiles
        self.player.all_projectiles.draw(screen)
        
        # appliquer l'ensemble des images de mon groupe de comettes 
        self.comet_event.all_comets.draw(screen)
        
        #verifier si le joueur souhaite aller à gauche ou a droite 
        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < 1080 : 
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0 :
            self.player.move_left()
       
            
        
        
        #mettre à jour l'ecran
        pygame.display.flip()
    
      
            
    def spawn_monster(self,monster_name ):
        self.all_monsters.add(monster_name.__call__(self))
        
    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite,group, False, pygame.sprite.collide_mask)