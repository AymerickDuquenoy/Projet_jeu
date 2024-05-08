import pygame
import math
from game import Game
pygame.mixer.init()
pygame.init() 


# Création de la musique
menu_musique = pygame.mixer.Sound('assets/musique/musique_menu.mp3')
menu_musique.set_volume(0.1)

game_musique = pygame.mixer.Sound('assets/musique/musique_jeu.mp3')
game_musique.set_volume(0.1)
# definir une clock 
clock = pygame.time.Clock()
FPS = 60

# generer la fenetre de notre jeu 
pygame.display.set_caption("mon premier jeu")
screen = pygame.display.set_mode((1080,720))

# importer de charger l'arrierre plan de notre jeu 
background = pygame.image.load('assets/bg.jpg')

# importer charger notre bannière 
banner = pygame.image.load('assets/banner.png')
banner = pygame.transform.scale(banner,(500,500))
banner_rect = banner.get_rect()
banner_rect.x = math.ceil(screen.get_width() / 4)

# importer charger notre bouton pour lancer la partie 
play_button = pygame.image.load('assets/button.png')
play_button = pygame.transform.scale(play_button, (400,150))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil(screen.get_width()/ 3.33)
play_button_rect.y = math.ceil(screen.get_height() / 2)

# import charger notre bouton pour voir les régles 
rules_button = pygame.image.load('assets/rules.png')
rules_button = pygame.transform.scale(rules_button,(100,100))
rules_button_rect = rules_button.get_rect()
rules_button_rect.x = 950
rules_button_rect.y = 600

# fleche retour 
return_boutton = pygame.image.load('assets/return.png')
return_boutton = pygame.transform.scale(return_boutton,(100,100))
return_boutton_rect = return_boutton.get_rect()
return_boutton_rect.x = 100
return_boutton_rect.y = 600

# charger notre jeu
game = Game()



running = True 

#boucle tant que cette condition est vrai 
while running:
    
    #appliquer l'arriere plan de notre jeu 
    screen.blit(background, (0,-200))
    
   
    #verifier si notre jeu a commencé ou non 
    if game.is_playing :
        menu_musique.stop()
        game_musique.play()
        if game.score_statu == False : 
            #déclencher les instructions de la partie 
            game.update(screen)
        else : 
            game.end_score(screen)
    # verifier si notre jeu n'a pas commencé 
    else: 
        game_musique.stop()
        menu_musique.play()
        if game.rules : 
            game.rule(screen)
            screen.blit(return_boutton,(return_boutton_rect))
        else:
            # ajouter mon ecran de bienvenue 
            screen.blit(play_button, (play_button_rect))
            screen.blit(banner,(banner_rect)) 
            screen.blit(rules_button,(rules_button_rect))
         
            
        
        
    # si le joueur ferme cette fenetre
    for event in pygame.event.get() : 
        # que l'evenement est fermeture de fenetre
        if event.type == pygame.QUIT : 
                running = False 
                pygame.quit()
         # detecter si un joueur lache une touche du clavier  
        elif event.type == pygame.KEYDOWN :
                game.pressed[event.key] = True
                
            #detecter si la touche espace est enclenchée pour lancer notre projectile
                if event.key == pygame.K_SPACE : 
                    if game.is_playing :
                        game.player.launch_projectile()
                    else : 
                        #mettre le jeu en mode "lancé"
                        game.start()
                        #jouer le son
                        game.sound_manager.play('click')
                        # mise a jour en fin de jeu 
                    if  game.score_statu == True : 
                        game.score_statu = False
                        game.is_playing = False
                        game.score = 0
                        
                        
                    
        elif event.type == pygame.KEYUP :
                game.pressed[event.key] = False
                
        elif event.type == pygame.MOUSEBUTTONDOWN : 
            # verification pour savoir si la souris est en collision avec le bouton jouer 
            if play_button_rect.collidepoint(event.pos) :
                #mettre le jeu en mode "lancé"
                game.start()
                #jouer le son
                game.sound_manager.play('click')
            # verification pour savoir si la souris est en collision avec le bouton des règles  
            if rules_button_rect.collidepoint(event.pos) : 
                game.rules = True
            if return_boutton_rect.collidepoint(event.pos) : 
                game.rules = False
            
            
            
                
    # fixer le nombre de fps sur ma clock 
    clock.tick(FPS)
    
      #mettre à jour l'ecran
    pygame.display.flip()
      