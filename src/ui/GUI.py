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

    
    def simulate_circle_falling(self, row, selected_column, piece):

        starting_y = int(self.square_size / 2)

        speed = 20

        print(self.height - int(row * self.square_size + self.square_size / 2))

        while starting_y <= self.height - int(row * self.square_size + self.square_size / 2):

            pygame.draw.rect(self.screen, self.background_color, (0, 0, self.width, self.square_size))
            pygame.draw.circle(self.screen, piece, (int(selected_column * self.square_size + self.square_size / 2),
                                                     starting_y + speed), self.circle_radius)
            starting_y += speed

            pygame.display.update()
            pygame.time.wait(20)

            self.draw_board()

        return True


    def start(self):
        
        print("Running...")
        
        started = None
        
        done = False

        turn = 0

        while not done:

            if started == None:
                
                self._service.clear_board()
                self.screen.fill(self.background_color)
                label1 = pygame.font.SysFont("monospace", 32, bold=True).render("Press 1 to start game vs. computer", True, self.computer_coin_color)
                label2 = pygame.font.SysFont("monospace", 32, bold=True).render("Press 2 to start 1v1 game", True, self.player_coin_color)
                self.screen.blit(label1, (0, 0))
                self.screen.blit(label2, (0, 64))

                pygame.display.flip()

                while started == None:
                    
                    for event in pygame.event.get():
                        if event.type == pygame.constants.QUIT:
                            sys.exit()
                        if event.type == pygame.constants.KEYDOWN:
                            if event.key == pygame.K_1:
                                started = 1
                            elif event.key == pygame.K_2:
                                started = 2
                
                self.screen.fill(color=self.background_color)

            self.draw_board()
            pygame.display.update()

            if started == 1:

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
                            
                            row = self._service.fake_push_to_col(col_push)

                            if self.simulate_circle_falling(row, col_push-1, self.player_coin_color):
                                self._service.player_push_to_col(col_push)
                                self.draw_board()

                            if self._service.check_winner() != None:
                                
                                label = self.font.render("Player wins!", 1, self.player_coin_color)
                                self.screen.blit(label, (40,10))
                                pygame.display.update()

                                started = None
                                pygame.time.wait(3000)
                                break

                            else:
                        
                                try:
                                    self._service.check_draw()
                                except DrawException:
                                    
                                    label = self.font.render("Draw!", 1, self.computer_coin_color)
                                    self.screen.blit(label, (40,10))
                                    pygame.display.update()

                                    started = None
                                    pygame.time.wait(3000)
                                    break

                                col = self._service.computer_determine_push_to_col()
                                row = self._service.fake_push_to_col(col)

                                if self.simulate_circle_falling(row, col-1, self.computer_coin_color):

                                    self._service.computer_push_to_col(col)
                                    self.draw_board()

                                try:
                                    self._service.check_draw()
                                except DrawException:
                                    
                                    label = self.font.render("Draw!", 1, self.computer_coin_color)
                                    self.screen.blit(label, (40,10))
                                    pygame.display.update()

                                    started = None
                                    pygame.time.wait(3000)
                                    break

                                if self._service.check_winner() != None:

                                    label = self.font.render("Computer wins!", 1, self.computer_coin_color)
                                    self.screen.blit(label, (40,10))
                                    pygame.display.update()

                                    started = None
                                    pygame.time.wait(3000)
                                    break

                        except ColumnOverflowException:
                            pass
                        except InvalidColumnException:
                            pass 

            elif started == 2:
            
                if turn == 0:
                    turn_color = self.computer_coin_color
                else:
                    turn_color = self.player_coin_color

                for event in pygame.event.get():

                    if event.type == pygame.constants.QUIT:
                        sys.exit()

                    if event.type == pygame.constants.MOUSEMOTION:
                        
                        pygame.draw.rect(self.screen, self.background_color, (0,0, self.width, self.square_size))
                        
                        posx = event.pos[0]
                        
                        pygame.draw.circle(self.screen, turn_color, (posx, int(self.square_size/2)), self.circle_radius - 3)

                        pygame.display.update()

                    if event.type == pygame.constants.MOUSEBUTTONDOWN:
                    
                        pygame.draw.rect(self.screen, self.background_color, (0,0, self.width, self.square_size))
                        
                        posx = event.pos[0]

                        col_push = int(posx / self.square_size) + 1

                        try:
                            
                            row = self._service.fake_push_to_col(col_push)

                            if self.simulate_circle_falling(row, col_push-1, turn_color):

                                if turn == 0:
                                    self._service.computer_push_to_col(col_push)
                                else:
                                    self._service.player_push_to_col(col_push)

                                self.draw_board()

                                turn = 1-turn

                            if self._service.check_winner() != None:
                                
                                label = self.font.render(f"Player {turn+1} wins!", 1, turn_color)
                                self.screen.blit(label, (40,10))
                                pygame.display.update()

                                started = None
                                pygame.time.wait(3000)
                                break

                        # else:
                    
                            # try:
                            #     self._service.check_draw()
                            # except DrawException:
                                
                            #     label = self.font.render("Draw!", 1, self.computer_coin_color)
                            #     self.screen.blit(label, (40,10))
                            #     pygame.display.update()

                            #     started = None
                            #     pygame.time.wait(3000)
                            #     break

                            # col = self._service.computer_determine_push_to_col()
                            # row = self._service.fake_push_to_col(col)

                            # if self.simulate_circle_falling(row, col-1, self.computer_coin_color):

                            #     self._service.computer_push_to_col(col)
                            #     self.draw_board()

                            # try:
                            #     self._service.check_draw()
                            # except DrawException:
                                
                            #     label = self.font.render("Draw!", 1, self.computer_coin_color)
                            #     self.screen.blit(label, (40,10))
                            #     pygame.display.update()

                            #     started = None
                            #     pygame.time.wait(3000)
                            #     break

                            # if self._service.check_winner() != None:

                            #     label = self.font.render("Computer wins!", 1, self.computer_coin_color)
                            #     self.screen.blit(label, (40,10))
                            #     pygame.display.update()

                            #     started = None
                            #     pygame.time.wait(3000)
                            #     break

                        except ColumnOverflowException:
                            pass
                        except InvalidColumnException:
                            pass

          
        print("Exited GUI.")