import pygame  # type: ignore
import sys
import time

from const import *
from game import Game
from square import Square
from move import Move


class Main():

    def __init__(self):
        self.game=Game(player1_type='human',player2_type='AI')


        pygame.init()#Initie l'application
        self.screen = pygame.display.set_mode((width,height)) #Ouvre une fenetre pyagme
        pygame.display.set_caption("Chess") #Donne un titre à la fenetre

    def AI_turn(self,AI,board,game):
        move = AI.random_choose(self.game.board)
        if move.piece != None:
            board.confirm_move(move.piece, move)
            game.next_turn()
    
    def player_turn(self,board,game,dragger,player):
        
        for event in pygame.event.get():

                # 1) Click 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    #Calcul de la case (row,col) de la position cliquée
                    position = event.pos #recup position
                    
                    if player.color == 'white':
                        clicked_row = int(position[1]//square_size) #Ligne
                        clicked_col = int(position[0]//square_size) #Colonne
                    else:
                        clicked_row = 7-int(position[1]//square_size) #Ligne
                        clicked_col = 7-int(position[0]//square_size) #Colonne


                    #Si on selectionne une pièce, on la garde en mémoire
                    if board.squares[clicked_row][clicked_col].piece != None and board.squares[clicked_row][clicked_col].piece.color == player.color:
                        dragger.update_drag_position(position) #update la position de la case cliquée
                        dragger.piece = self.game.board.squares[clicked_row][clicked_col].piece
                        dragger.start_drag(dragger.piece) # On indique qu'on a commencé à deplacer une piece
                        board.calculate_possible_moves(dragger.piece) # on calcule les déplacements possibles de la piece

                # 2) Déclick
                if event.type == pygame.MOUSEBUTTONUP and dragger.piece != None:

                    #Calcul de la case (row,col) de la position décliquée
                    position = event.pos #recup position
                    if player.color == 'white':
                        declicked_row = int(position[1]//square_size) #Ligne
                        declicked_col = int(position[0]//square_size) #Colonne
                    else:
                        declicked_row = 7-int(position[1]//square_size) #Ligne
                        declicked_col = 7-int(position[0]//square_size) #Colonne
    
                    #Si une autre case est selectionnée, on déplace la piece cliquée sur cette case
                    move = Move(dragger.piece,Square(dragger.piece.row,dragger.piece.col),Square(declicked_row,declicked_col))
                            
                    #Si le déplacement choisit est valide et qu'elle appartient au bon joueur
                    if board.valid_move(dragger.piece,move):
                        board.confirm_move(dragger.piece, move)
                        game.next_turn()
                        
                    dragger.stop_drag() #On indique que l'on a cesser de déplacer la piece

                # 3) Souris en mouvement 
                if event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_drag_position(event.pos)
                    
                # 4) Touche appuyée
                if event.type == pygame.KEYDOWN : 

                    #Recommencer la partie
                    if event.key == pygame.K_r:
                        self.reset_game()

                        
                    if event.key == pygame.K_p:
                        self.reset_game(change_color=True)


                # 5) Quitter
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def update_display(self, game, dragger, screen):
        """Fonction pour mettre à jour l'affichage après chaque coup ou pendant un drag d'une piece."""
        game.show_background(screen)  # Dessine l'échiquier
        game.show_last_move(screen)   # Dessine le dernier déplacement
        game.show_pieces(screen)      # Redessine toutes les pièces

        if dragger.dragging:
            game.show_piece_possible_moves(screen)  # Montre les déplacements possibles
            dragger.show_drag(screen) # Montre la pièce en train de se déplacer

        pygame.display.update()  # Actualisation de l'affichage

    def reset_game(self,change_color = False):
        """Réinitialise le jeu en réaffectant les instances."""
        if change_color == True:
            color = 'white' if self.game.player_color == 'black' else 'black'
            self.game.reset(color)
        else:
            self.game.reset(self.game.player_color)

        # Réaffecter les variables locales après réinitialisation
        self.game = self.game  # Réinstancier le jeu
        self.board = self.game.board  # Réinstancier le plateau
        self.dragger = self.game.dragger  # Réinstancier le dragger
        self.AI = self.game.AI  # Réinstancier l'AI

    def mainloop(self):
        player = self.game.player1

        while True:

            self.update_display(self.game,self.game.dragger,self.screen)  

            if self.game.next_player == self.game.player1:     

                if self.game.player1.is_human():
                    self.player_turn(self.game.board,self.game,self.game.dragger,self.game.player1)
                    self.update_display(self.game,self.game.dragger,self.screen)   
                    
                else:
                    time.sleep(0.01)
                    self.AI_turn(self.game.player1.AI,self.game.board,self.game)
                    self.update_display(self.game,self.game.dragger,self.screen)   
            
            else:
                if self.game.player2.is_human():
                    self.player_turn(self.game.board,self.game,self.game.dragger,self.game.player2)
                    self.update_display(self.game,self.game.dragger,self.screen)   
                    
                else:
                    time.sleep(0.01)
                    self.AI_turn(self.game.player2.AI,self.game.board,self.game)
                    self.update_display(self.game,self.game.dragger,self.screen) 


            if player == self.game.previous_player:
                #Verifie s'il y a echec et mat
                if self.game.board.is_checkmate(self.game.next_player.color):
                    joueur = 'blancs' if self.game.next_player == 'black' else 'noirs'
                    print(f'Échec et mat ! Victoire des {joueur} !')

                    # Boucle figée en attendant fermeture
                    game_over = True
                    while game_over:
                        for event in pygame.event.get():
                            
                            if event.type == pygame.KEYDOWN : 
                                #Recommencer la partie
                                if event.key == pygame.K_r:
                                    self.reste_game()

                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                        self.game.show_background(self.screen)
                        self.game.show_last_move(self.screen)
                        self.game.show_pieces(self.screen)

                        # Affiche le message de fin 
                        font = pygame.font.SysFont(None, 48)
                        text = font.render(f'Échec et mat ! Victoire des {joueur} !', True, (0, 0, 0))
                        rect = text.get_rect(center=(width // 2, height // 2))
                        self.screen.blit(text, rect)

                        pygame.display.update()
                
                #Verifie s'il y a pat
                if self.game.board.is_pat(self.game.next_player.color):
                    
                    # Boucle figée en attendant fermeture
                    game_over = True
                    while game_over:
                        for event in pygame.event.get():
                            
                            if event.type == pygame.KEYDOWN : 
                                #Recommencer la partie
                                if event.key == pygame.K_r:
                                    self.reste_game()

                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                        self.game.show_background(self.screen)
                        self.game.show_last_move(self.screen)
                        self.game.show_pieces(self.screen)

                        # Affiche le message de fin 
                        font = pygame.font.SysFont(None, 48)
                        text = font.render(f'Egalité !', True, (0, 0, 0))
                        rect = text.get_rect(center=(width // 2, height // 2))
                        self.screen.blit(text, rect)

                        pygame.display.update()

                #S'il y a une promotion en cours 
                if self.game.board.is_promoting(self.game.board.last_move):

                    #Boucle figée en attendant choix 
                    if self.game.previous_player.is_human():
                        game_promoting = True
                        while game_promoting:

                            for event in pygame.event.get():

                                self.game.show_background(self.screen)
                                self.game.show_last_move(self.screen)
                                self.game.show_pieces(self.screen)
                                self.game.show_promotion(self.screen, self.game.board.last_move.piece)


                                if event.type == pygame.MOUSEBUTTONDOWN:

                                    #Calcul de la case (row,col) de la position cliquée
                                    position = event.pos #recup position
                                    
                                    if self.game.previous_player.color == 'white':
                                        clicked_row = int(position[1]//square_size) #Ligne
                                        clicked_col = int(position[0]//square_size) #Colonne
                                    else:
                                        clicked_row = 7-int(position[1]//square_size) #Ligne
                                        clicked_col = 7-int(position[0]//square_size) #Colonne

                                    
                                    if ((self.game.board.last_move.piece.color == 'white' and clicked_row in [0,1,2,3]) or (self.game.board.last_move.piece.color != 'white' and clicked_row in [4,5,6,7]) ) and clicked_col == self.game.board.last_move.piece.col:
                                        self.game.board.promote(self.game.board.last_move.piece,clicked_row)
                                        game_promoting = False
                                        self.game.dragger.stop_drag()

                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                
                            pygame.display.update()

                    else: 
                        if self.game.board.last_move.piece.color == self.game.player1.color:
                            promotion_choice = self.game.player1.AI.choose_promotion(self.game.board.last_move)
                        else:
                            promotion_choice = self.game.player2.AI.choose_promotion(self.game.board.last_move)
                        self.game.board.promote(self.game.board.last_move.piece,promotion_choice)
                        self.game.board.last_move.type='has promote'
                player = self.game.next_player
        
main=Main()
main.mainloop()