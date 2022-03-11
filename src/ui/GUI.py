import pygame
import os, sys
from service.Service import Service
from domain.BoardExceptions import *
from service.ServiceExceptions import *

class GUI:
    
    def __init__(self):
        
        self._rows = 7
        self._cols = 7
        self._service = Service(self._rows, self._cols)

        self.square_size = 120
        self.width = self._cols * self.square_size
        self.height = (self._rows+1) * self.square_size

        self.size = (self.width, self.height)
        self.circle_radius = 40

        self.background_color = (30, 30, 30)
        self.board_color = (41, 120, 160)
        self.player_coin_color = (194, 249, 112)
        self.computer_coin_color = (232, 109, 90)
        
        pygame.font.init()
        self.font = pygame.font.SysFont("consolas", 75)

        self.screen = pygame.display.set_mode(self.size)
        
    
    
    def draw_board(self):

        board = self._service.board_matrix()
 
        for c in range(1, self._cols + 1):

            for r in range(1, self._rows + 1):
                
                pygame.draw.rect(self.screen, self.board_color, ((c-1) * self.square_size, (r-1) * self.square_size + self.square_size, self.square_size, self.square_size))

                pygame.draw.circle(self.screen, self.background_color, ( int((c-1) * self.square_size + self.square_size / 2), int((r-1)* self.square_size + self.square_size + self.square_size / 2) ), self.circle_radius)
        
        for c in range(1, self._cols + 1):
            
            for r in range(1, self._rows + 1):

                if board[r][c] == '\u26D4':
                    pygame.draw.circle(self.screen, self.computer_coin_color, ( int((c-1) * self.square_size + self.square_size / 2), self.height - int((self._rows - r) * self.square_size + self.square_size / 2) ), self.circle_radius - 3)

                elif board[r][c] == '\u26A1': 
                    pygame.draw.circle(self.screen, self.player_coin_color, ( int((c-1) * self.square_size + self.square_size / 2), self.height - int((self._rows - r) * self.square_size + self.square_size / 2) ), self.circle_radius - 3)

        pygame.display.update()


    def start(self):
        
        print("Running...")
        self.draw_board()
        pygame.display.update()

        done = False
        
        while not done:

            for event in pygame.event.get():

                if event.type == pygame.constants.QUIT:
                    sys.exit()

                if event.type == pygame.constants.MOUSEMOTION:
                    
                    pygame.draw.rect(self.screen, self.background_color, (0,0, self.width, self.square_size))
                    
                    posx = event.pos[0]
                    
                    pygame.draw.circle(self.screen, self.player_coin_color, (posx, int(self.square_size/2)), self.circle_radius - 3)
                
                pygame.display.update()

                if event.type == pygame.constants.MOUSEBUTTONDOWN:
                     
                    pygame.draw.rect(self.screen, self.background_color, (0,0, self.width, self.square_size))
                        
                    posx = event.pos[0]

                    col_push = int(posx / self.square_size) + 1

                    try:
                        
                        self._service.player_push_to_col(col_push)

                        self.draw_board()

                        if self._service.check_winner() != None:
                            
                            label = self.font.render("Player wins!", 1, self.player_coin_color)
                            self.screen.blit(label, (40,10))
                            pygame.display.update()

                            done = True
                            pygame.time.wait(3000)
                            break

                        else:
                    
                            try:
                                self._service.check_draw()
                            except DrawException:
                                
                                label = self.font.render("Draw!", 1, self.computer_coin_color)
                                self.screen.blit(label, (40,10))
                                pygame.display.update()

                                done = True
                                pygame.time.wait(3000)
                                break

                            self._service.computer_push_to_col()
                            self.draw_board()

                            try:
                                self._service.check_draw()
                            except DrawException:
                                
                                label = self.font.render("Draw!", 1, self.computer_coin_color)
                                self.screen.blit(label, (40,10))
                                pygame.display.update()

                                done = True
                                pygame.time.wait(3000)
                                break

                            if self._service.check_winner() != None:

                                label = self.font.render("Computer wins!", 1, self.computer_coin_color)
                                self.screen.blit(label, (40,10))
                                pygame.display.update()

                                done = True
                                pygame.time.wait(3000)
                                break

                    except ColumnOverflowException:
                        pass
                    except InvalidColumnException:
                        pass         
        print("Exited GUI.")