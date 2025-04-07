import pygame  # type: ignore
import os

from board import Board
from dragger import Dragger 
from piece import *
from const import *

class Game:

    def __init__(self,player_color = 'white'):
        self.board = Board()
        self.dragger = Dragger()
        self.next_player = 'white'
        self.player_color = player_color
        self.promoting = False

### METHODES D'AFFICHAGE

    def show_background(self, surface):
        '''
        Méthode pour créer les cases graphique de l'échiquier. Il s'agit du fond d'ecran, on dessine un carré par un carré
        '''
        # 1) Parcours de chaque case 
        for row in range(rows):
            for col in range (cols):
       
        # 2) Choix de la couleur en fonction de la position
                if (row + col)%2 == 0:
                    color=(234,235,200) if self.player_color == 'white' else (119,154,88)
                else:
                    color=(119,154,88) if self.player_color == 'white' else (234,235,200)
        # 3) Dessine le carré 
                square = (col*square_size,row*square_size,square_size,square_size) 
                pygame.draw.rect(surface,color,square)

        # 4) Dessine le nom des lignes et colonnes
                font = pygame.font.SysFont('monospace',18,bold=True)
                row_names = ['a','b','c','d','e','f','g','h'] if self.player_color == 'white' else ['h','g','f','e','d','c','b','a']
                col_names = ['8','7','6','5','4','3','2','1'] if self.player_color == 'white' else ['1','2','3','4','5','6','7','8']

                if col == 0 : #Dessine le nom des colonnes
                    if self.player_color == 'white':
                        name_color = (119,154,88) if (row)%2 == 0 else (234,235,200)
                    else:
                        name_color = (234,235,200) if (row)%2 == 0 else (119,154,88)
                    name_position = (5,5+row*square_size)
                    name = font.render(str(col_names[row]),1,name_color)
                    surface.blit(name,name_position)

                if row == 7 : #Dessine le nom des lignes
                    if self.player_color == 'white':
                        name_color = (119,154,88) if (row+col)%2 == 0 else (234,235,200)
                    else:
                        name_color = (234,235,200) if (row+col)%2 == 0 else (119,154,88)
                    name_position = (85+col*square_size,780)
                    name = font.render(str(row_names[col]),1,name_color)
                    surface.blit(name,name_position)

    def show_pieces(self,surface):
        '''
        Méthode affichant les pieces sur l'échiquier. On verifie pour chaque case s'il y a une piece. Si oui, on l'affiche 
        '''
        # 1) Parcours de board
        for row in range(rows):
            for col in range (cols):

        # 2) Verifie si un piece est associée à cette case
                if self.board.squares[row][col].has_piece(): #Il y a t-il une piece sur la case?
        
        # 3) Affiche l'image
                    piece = self.board.squares[row][col].piece # raccourci pour cette piece
                    
                    #Verifie que la piece n'est pas en déplacement pour l'afficher
                    if self.dragger.piece != piece:
                        img = pygame.image.load(piece.image) #je charge l'image de la piece
                        if self.player_color == 'white':
                            img_center = col*square_size + square_size//2, row*square_size + square_size//2 #Je calcule la position dans l'echiquier du centre de l'image
                        else:
                            img_center = (7-col)*square_size + square_size//2, (7-row)*square_size + square_size//2
                        piece.image_rect = img.get_rect(center = img_center) # je place l'image centrée sur la position calculée
                        surface.blit(img, piece.image_rect) #affiche l'image

    def show_piece_possible_moves(self,surface,board):

        piece = self.dragger.piece
        circle_radius = square_size // 5
        ring_radius = square_size // 2.1
        thickness = 7


        # loop all valid moves
        for move in piece.moves:
            if self.player_color=='white':
                center = ((move.final_cell.col +0.5) * square_size , (move.final_cell.row + 0.5) * square_size)
            else : 
                center= ((7-move.final_cell.col +0.5) * square_size , (7-move.final_cell.row + 0.5) * square_size)
            #if board.squares[move.final_cell.row][move.final_cell.col].has_piece():
            if move.type == 'capture' or move.type=='en passant':
                color = (140,30,30) if ((move.final_cell.col + move.final_cell.row)%2 == 0) else (100,10,10)
                pygame.draw.circle(surface, color, center, ring_radius, thickness)
            else:
                color = (30,110,30) if ((move.final_cell.col + move.final_cell.row)%2 == 0) else (10,80,10)
                pygame.draw.circle(surface, color, center, circle_radius)

    def show_last_move(self,surface):
        if self.board.last_move:
            last_cell = self.board.last_move.initial_cell
            actual_cell = self.board.last_move.final_cell

            color = (230, 230, 100)


            #Calcule les cases
            if self.player_color == 'white':
                last_square = (last_cell.col*square_size,last_cell.row*square_size,square_size,square_size) 
                actual_square = (actual_cell.col*square_size,actual_cell.row*square_size,square_size,square_size) 
            else: 
                last_square = ((7-last_cell.col)*square_size,(7-last_cell.row)*square_size,square_size,square_size) 
                actual_square = ((7-actual_cell.col)*square_size,(7-actual_cell.row)*square_size,square_size,square_size) 
                
            #Affiche les cases
            pygame.draw.rect(surface,color,last_square)
            pygame.draw.rect(surface,color,actual_square)

    def show_promotion(self,surface,piece):
        color = piece.color
        row = piece.row
        col = piece.col
        self.promoting = True

        if self.player_color == 'white':
            possible_piece = [
            Rook(color),
            Queen(color),
            Knight(color),
            Bishop(color)
        ]
        else:
            possible_piece =[
            Bishop(color),
            Knight(color),
            Queen(color),
            Rook(color)
            ]

        box_width = 100
        box_height = 4*100
        if self.player_color == 'white':
            box_x = int(col*square_size)
            box_y = 0 if color =='white' else 400 
        else:
            box_x = int((7-col)*square_size)
            box_y = 400 if color =='white' else 0 
        i=0

        # Arrière-plan de la boîte
        pygame.draw.rect(surface, (200, 200, 200), (box_x, box_y, box_width, box_height))
        pygame.draw.rect(surface, (0, 0, 0), (box_x, box_y, box_width, box_height), 3)  # bordure

        for piece in possible_piece:
            img = pygame.image.load(piece.image) #je charge l'image de la piece
            if self.player_color == 'white':
                img_center = col*square_size + square_size//2, (row+i)*square_size - (box_y-100)*box_y//400 + square_size//2 #Je calcule la position dans l'echiquier du centre de l'image
            else:
                img_center = (7-col)*square_size + square_size//2, (7-row+i)*square_size - (box_y-100)*box_y//400 + square_size//2
            piece.image_rect = img.get_rect(center = img_center) # je place l'image centrée sur la position calculée
            surface.blit(img, piece.image_rect) #affiche l'image
            i+=1



### METHODES DE JEU

    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def reset(self):
        self.__init__(self.player_color)


