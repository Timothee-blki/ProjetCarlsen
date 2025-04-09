import pygame  # type: ignore
import sys

from const import *
from game import Game
from square import Square
from move import Move


class Main():

    def __init__(self):
        self.game=Game()


        pygame.init()#Initie l'application
        self.screen = pygame.display.set_mode((width,height)) #Ouvre une fenetre pyagme
        pygame.display.set_caption("Chess") #Donne un titre à la fenetre

    def mainloop(self):
        
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        AI = self.game.AI

        move = Move(None,Square(0,0),Square(0,0))


        while True:

            ### AFFICHAGE PRINCIPAL ###
            game.show_background(screen)  # Dessine l'échiquier
            game.show_last_move(screen)
            game.show_pieces(screen)  # Redessine toutes les pièces            

            #Si une piece est en déplacement:
            if dragger.dragging:
 
                game.show_piece_possible_moves(screen,board) #montre les déplacements possibles 
                dragger.show_drag(screen) # montre la piece


            if game.next_player == game.player_color:

                ### CONTROLE D'EVENEMENT ###

                for event in pygame.event.get():

                    # 1) Click 
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        
                        #Calcul de la case (row,col) de la position cliquée
                        position = event.pos #recup position
                        
                        if game.player_color == 'white':
                            clicked_row = int(position[1]//square_size) #Ligne
                            clicked_col = int(position[0]//square_size) #Colonne
                        else:
                            clicked_row = 7-int(position[1]//square_size) #Ligne
                            clicked_col = 7-int(position[0]//square_size) #Colonne


                        #Si on selectionne une pièce, on la garde en mémoire
                        if self.game.board.squares[clicked_row][clicked_col].piece != None and self.game.board.squares[clicked_row][clicked_col].piece.color == game.next_player:
                            dragger.update_drag_position(position,game.next_player) #update la position de la case cliquée
                            dragger.piece = self.game.board.squares[clicked_row][clicked_col].piece
                            dragger.start_drag(dragger.piece) # On indique qu'on a commencé à deplacer une piece
                            board.calculate_possible_moves(dragger.piece) # on calcule les déplacements possibles de la piece

                    # 2) Déclick
                    if event.type == pygame.MOUSEBUTTONUP and dragger.piece != None:

                        #Calcul de la case (row,col) de la position décliquée
                        position = event.pos #recup position
                        if game.player_color == 'white':
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
                            if dragger.piece.name == 'pawn' and move.final_cell.row in [0,7]:
                                game.show_promotion(screen,dragger.piece)
                                game.next_turn()
                                break
                            game.next_turn()
                        dragger.stop_drag() #On indique que l'on a cesser de déplacer la piece

                    # 3) Souris en mouvement 
                    if event.type == pygame.MOUSEMOTION:
                        if dragger.dragging:
                            dragger.update_drag_position(event.pos,game.player_color)
                    
                    # 4) Touche appuyée
                    if event.type == pygame.KEYDOWN : 

                        #Recommencer la partie
                        if event.key == pygame.K_r:
                            game.reset(game.player_color)
                            game = self.game
                            board = self.game.board
                            dragger = self.game.dragger
                        
                        if event.key == pygame.K_p:
                            #recommence la partie

                            #change la couleur
                            player_color = 'black' if game.player_color == 'white' else 'white'
                            game.reset(player_color)
                            game = self.game
                            board = self.game.board
                            dragger = self.game.dragger

                            AI = self.game.AI

                    # 5) Quitter
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            else:
                move = AI.random_choose(self.game.board)
                if move.piece != None:
                    board.confirm_move(move.piece, move)
                game.next_turn()

            #Verifie si La partie est finie
            if board.is_checkmate(game.next_player):
                joueur = 'blancs' if game.next_player == 'black' else 'noirs'
                print(f'Échec et mat ! Victoire des {joueur} !')

                # Boucle figée en attendant fermeture
                game_over = True
                while game_over:
                    for event in pygame.event.get():
                        
                        if event.type == pygame.KEYDOWN : 
                            #Recommencer la partie
                            if event.key == pygame.K_r:
                                game.reset(game.player_color)
                                game = self.game
                                board = self.game.board
                                dragger = self.game.dragger
                                game_over=False


                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                    game.show_background(screen)
                    game.show_last_move(screen)
                    game.show_pieces(screen)

                    # Affiche le message de fin 
                    font = pygame.font.SysFont(None, 48)
                    text = font.render(f'Échec et mat ! Victoire des {joueur} !', True, (0, 0, 0))
                    rect = text.get_rect(center=(width // 2, height // 2))
                    screen.blit(text, rect)

                    pygame.display.update()
            
            #S'il y a une promotion en cours 
            if board.is_promoting(move):

                #Boucle figée en attendant choix 
                if game.next_player != game.player_color:
                    game_promoting = True
                    while game_promoting:

                    

                        for event in pygame.event.get():

                            game.show_background(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            game.show_promotion(screen, move.piece)


                            if event.type == pygame.MOUSEBUTTONDOWN:

                                #Calcul de la case (row,col) de la position cliquée
                                position = event.pos #recup position
                                
                                if game.player_color == 'white':
                                    clicked_row = int(position[1]//square_size) #Ligne
                                    clicked_col = int(position[0]//square_size) #Colonne
                                else:
                                    clicked_row = 7-int(position[1]//square_size) #Ligne
                                    clicked_col = 7-int(position[0]//square_size) #Colonne

                                
                                if ((move.piece.color == 'white' and clicked_row in [0,1,2,3]) or (move.piece.color != 'white' and clicked_row in [4,5,6,7]) ) and clicked_col == move.piece.col:
                                    board.promote(move.piece,clicked_row)
                                    game_promoting = False
                                    dragger.stop_drag()

                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            
                        pygame.display.update()

                else: 
                    promotion_choice = AI.choose_promotion(move)
                    board.promote(move.piece,promotion_choice)
                    move.type='has promote'


            pygame.display.update()
        



main=Main()
main.mainloop()