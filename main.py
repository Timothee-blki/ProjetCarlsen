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


        while True:

            ### AFFICHAGE PRINCIPAL ###
            game.show_background(screen)  # Dessine l'échiquier
            game.show_last_move(screen)
            game.show_pieces(screen)  # Redessine toutes les pièces            
            
            #S'il y a une promotion en cours 
            if game.promoting == True:
                game.show_promotion(screen, dragger.piece)

            #Si une piece est en déplacement:
            elif dragger.dragging:
 
                game.show_piece_possible_moves(screen,board) #montre les déplacements possibles 
                dragger.show_drag(screen) # montre la piece





            ### CONTROLE D'EVENEMENT ###

            for event in pygame.event.get():

                # 1) Click 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    #Calcul de la case (row,col) de la position cliquée
                    position = event.pos #recup position
                    
                    clicked_row = int(position[1]//square_size) #Ligne
                    clicked_col = int(position[0]//square_size) #Colonne

                    
                    if game.promoting:
                        if ((dragger.piece.color == 'white' and clicked_row in [0,1,2,3]) or (dragger.piece.color != 'white' and clicked_row in [4,5,6,7]) )and clicked_col == dragger.piece.col:
                            game.promoting = False
                            board.promote(dragger.piece,clicked_row)
                            dragger.stop_drag()


                    #Si on selectionne une pièce, on la garde en mémoire
                    elif self.game.board.squares[clicked_row][clicked_col].piece != None and self.game.board.squares[clicked_row][clicked_col].piece.color == game.next_player:
                        dragger.update_drag_position(position) #update la position de la case cliquée
                        dragger.piece = self.game.board.squares[clicked_row][clicked_col].piece
                        dragger.start_drag(dragger.piece) # On indique qu'on a commencé à deplacer une piece
                        board.calculate_possible_moves(dragger.piece) # on calcule les déplacements possibles de la piece


                # 2) Déclick
                if event.type == pygame.MOUSEBUTTONUP and dragger.piece != None and game.promoting == False:

                    #Calcul de la case (row,col) de la position décliquée
                    position = event.pos #recup position
                    declicked_row = int(position[1]//square_size) #Ligne
                    declicked_col = int(position[0]//square_size) #Colonne
 

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
                        dragger.update_drag_position(event.pos)
                
                # 4) Touche appuyée
                if event.type == pygame.KEYDOWN : 

                    #Recommencer la partie
                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger
                    
                    if event.key == pygame.K_p:

                        #recommence la partie
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger

                        #change la couleur
                        game.player_color = 'black'

                # 5) Quitter
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            

            pygame.display.update()
        



main=Main()
main.mainloop()