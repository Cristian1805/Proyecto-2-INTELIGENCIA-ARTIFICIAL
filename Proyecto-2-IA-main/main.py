#Autores:
#Cristian Camilo Lozano 
#Manuel Perdomo 

from tkinter import *
from typing import Match 
import numpy as np
import random

size_of_board = 600
number_of_dots = 6
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
dot_color = '#000000'  
player1_color = '#0492CF'
player1_color_light = '#67B0CF'
machine_color = '#EE4035'
machine_color_light = '#EE7E77'
Green_color = '#7BC043'
dot_width = 0.25*size_of_board/number_of_dots
edge_width = 0.1*size_of_board/number_of_dots
distance_between_dots = size_of_board / (number_of_dots)

class CuerdasyCorrales():
    
    def __init__(self):
        self.window = Tk()
        self.window.title('Cuerdas y Corrales')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)
        self.player1_starts = True
        self.refresh_board()
        self.play_again()

    def play_again(self):
        self.refresh_board()
        self.board_status = np.zeros(shape=(number_of_dots - 1, number_of_dots - 1))
        print(self.board_status)
    
        self.row_status = np.zeros(shape=(number_of_dots, number_of_dots - 1))
        self.col_status = np.zeros(shape=(number_of_dots - 1, number_of_dots))
        
        self.player1_starts = not self.player1_starts
        self.player1_turn = not self.player1_starts
#---------------
        self.reset_board = False
        self.turntext_handle = []

        self.already_marked_boxes = []
        self.display_turn_text()

    def mainloop(self):
        self.window.mainloop()



#______________________________________________________________________________________


    def is_grid_occupied(self, logical_position, type):
        
        #"Valida si la linea esta o no ocupada ya "
    
        r = logical_position[0]
        
        print("R========= %i" %r)
        
        
        c = logical_position[1]
        
        print("C=========%i" %c)
        
        occupied = True

        if type == 'row' and self.row_status[c][r] == 0:
            occupied = False
            print("Fila desocupada")
            
        if type == 'col' and self.col_status[c][r] == 0:
            occupied = False
            print("Columna desocupada")
        
        else: 
            print("Fila Ocupada")
            
        return occupied

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        print("Posicion Coordenadas click: "+str( grid_position) )
        
        position = (grid_position-distance_between_dots/4)//(distance_between_dots/2)

        type = False
        logical_position = []
        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            r = int((position[0]-1)//2)
            c = int(position[1]//2)
            logical_position = [r, c]
            type = 'row'
            
            print("Pinta Una linea horizontal")
            
            
        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            c = int((position[1] - 1) // 2)
            r = int(position[0] // 2)
            logical_position = [r, c]
            type = 'col'

            print("Pinta Una linea vertical")
            
            print("Logical Position" + str(logical_position))
            
        return logical_position, type

    def mark_box(self):
        boxes = np.argwhere(self.board_status == -4)
        
        print("Cajas Completas")
        print(boxes)
        for box in boxes:
            print (box)
            if list(box) not in self.already_marked_boxes and list(box) !=[]:
                self.already_marked_boxes.append(list(box))
                color = player1_color_light
                self.shade_box(box, color)

        boxes = np.argwhere(self.board_status == 4)
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) !=[]:
                self.already_marked_boxes.append(list(box))
                color = machine_color_light
                self.shade_box(box, color)

    def update_board(self, type, logical_position):
        r = logical_position[0]
        c = logical_position[1]
        
        print("c=="+ str(c))
        print("r=="+ str(r))
        
        
        val = 1
        if self.player1_turn:
            val =- 1

        if c < (number_of_dots-1) and r < (number_of_dots-1):
            self.board_status[c][r] += val

        if type == 'row':
            self.row_status[c][r] = 1
            if c >= 1:
                self.board_status[c-1][r] += val

        elif type == 'col':
            self.col_status[c][r] = 1
            if r >= 1:
                self.board_status[c][r-1] += val

    def is_gameover(self):
        return (self.row_status == 1).all() and (self.col_status == 1).all()

    def make_edge(self, type, logical_position):
        if type == 'row':
            start_x = distance_between_dots/2 + logical_position[0]*distance_between_dots
            end_x = start_x+distance_between_dots
            start_y = distance_between_dots/2 + logical_position[1]*distance_between_dots
            end_y = start_y
        elif type == 'col':
            start_y = distance_between_dots / 2 + logical_position[1] * distance_between_dots
            end_y = start_y + distance_between_dots
            start_x = distance_between_dots / 2 + logical_position[0] * distance_between_dots
            end_x = start_x

        if self.player1_turn:
            color = player1_color
        else:
            color = machine_color
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=edge_width)

    def display_gameover(self):
        player1_score = len(np.argwhere(self.board_status == -4))
        machine_score = len(np.argwhere(self.board_status == 4))

        if player1_score > machine_score:
            # Player 1 wins
            text = 'Winner: Player 1 '
            color = player1_color
        elif machine_score > player1_score:
            text = 'Winner: Machine '
            color = machine_color
        else:
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 40 bold", fill=Green_color,
                                text=score_text)

        score_text = 'Player 1 : ' + str(player1_score) + '\n'
        score_text += 'Machine : ' + str(machine_score) + '\n'
        # score_text += 'Tie                    : ' + str(self.tie_score)
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 30 bold", fill=Green_color,
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)

    def refresh_board(self):
        for i in range(number_of_dots):
            x = i*distance_between_dots+distance_between_dots/2
            self.canvas.create_line(x, distance_between_dots/2, x,
                                    size_of_board-distance_between_dots/2,
                                    fill='gray', dash = (2, 2))
            self.canvas.create_line(distance_between_dots/2, x,
                                    size_of_board-distance_between_dots/2, x,
                                    fill='gray', dash=(2, 2))

        for i in range(number_of_dots):
            for j in range(number_of_dots):
                start_x = i*distance_between_dots+distance_between_dots/2
                end_x = j*distance_between_dots+distance_between_dots/2
                self.canvas.create_oval(start_x-dot_width/2, end_x-dot_width/2, start_x+dot_width/2,
                                        end_x+dot_width/2, fill=dot_color,
                                        outline=dot_color)

#____________________________________________________________Turno Player 1

    def display_turn_text(self):
        text = 'Turno del : '
        if self.player1_turn:
            text += 'Player1'
            color = player1_color
        
            self.canvas.delete(self.turntext_handle)
            self.turntext_handle = self.canvas.create_text(size_of_board - 5*len(text),
                                                       size_of_board-distance_between_dots/8,
                                                       font="cmr 15 bold", text=text, fill=color)

        
        else:
            text += 'Machine'
            color = machine_color
            self.canvas.delete(self.turntext_handle)
            self.turntext_handle = self.canvas.create_text(size_of_board - 5*len(text),
                                                       size_of_board-distance_between_dots/8,
                                                       font="cmr 15 bold", text=text, fill=color)




    def shade_box(self, box, color):
        start_x = distance_between_dots / 2 + box[1] * distance_between_dots + edge_width/2
        start_y = distance_between_dots / 2 + box[0] * distance_between_dots + edge_width/2
        end_x = start_x + distance_between_dots - edge_width
        end_y = start_y + distance_between_dots - edge_width
        self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')


    def click(self, event):
        if not self.reset_board:
            print("X===,Y==")
            print([event.x,event.y])
            grid_position = [event.x, event.y]
            logical_positon, valid_input = self.convert_grid_to_logical_position(grid_position)
            if valid_input and not self.is_grid_occupied(logical_positon, valid_input):
                self.update_board(valid_input, logical_positon)
                self.make_edge(valid_input, logical_positon)
                self.mark_box()
                self.refresh_board()
                self.player1_turn = not self.player1_turn

                if self.is_gameover():
                    # self.canvas.delete("all")
                    self.display_gameover()
                else:
                    self.display_turn_text()
                    self.cpu()
        else:
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False

    def cpu(self):
        print("CPUUUUUU")
        aleatorio=random.randint(0,59)

        print("aleatoriox %i"%aleatorio)
        print("aleatorioy %i"%aleatorio)
        
        arreglox=[49,50,49,48,50,117,105,110,98,82,111,199,193,202,200,193,194,150,150,150,150,150,248,248,248,248,248,299,299,299,299,299,299,349,349,349,349,349,403,403,403,403,403,403,447,447,447,447,447,497,497,497,497,497,550,550,550,550,550]
        arregloy=[87,207,309,400,515,54,148,247,349,450,550,51,152,251,350,447,551,103,201,303,407,507,88,211,298,403,505,49,147,252,347,453,547,95,195,301,401,509,51,146,250,347,447,545,204,296,387,488,94,150,249,350,450,550,91,206,296,397,505]
        
        print("Arreglo X %i"%len(arreglox))
        print("Arreglo Y %i"% len(arregloy))
        
        x=arreglox[aleatorio]
        y=arregloy[aleatorio]
        
        print("X=={},Y=={}".format(x,y))
        
        if not self.reset_board:
            grid_position = [x, y]
            logical_positon, valid_input = self.convert_grid_to_logical_position(grid_position)
            prueba=self.is_grid_occupied(logical_positon, valid_input)
            print("Pruebaaaaa: ")
            print(prueba)  
            if valid_input and not self.is_grid_occupied(logical_positon, valid_input):
                self.update_board(valid_input, logical_positon)
                self.make_edge(valid_input, logical_positon)
                self.mark_box()
                self.refresh_board()
                self.player1_turn = False
                self.player1_turn = not self.player1_turn
                if self.is_gameover():
                    # self.canvas.delete("all")
                    self.display_gameover()
                else:
                    self.display_turn_text()
            
            else:
                while prueba != False:
                    print("ENTROOOOOOOOOOOOOOOOOO")
                    arreglox=[49,51,49,48,50,117,105,110,98,82,111,199,193,202,200,193,194,150,150,150,150,150,248,248,248,248,248,299,299,299,299,299,299,349,349,349,349,349,403,403,403,403,403,403,447,447,447,447,447,497,497,497,497,497,550,550,550,550,550]
                    arregloy=[87,193,309,400,515,54,148,247,349,450,550,51,152,251,350,447,551,103,201,303,407,507,88,211,298,403,505,49,147,252,347,453,547,95,195,301,401,509,51,146,250,347,447,545,204,296,387,488,94,150,249,350,450,550,91,206,296,397,505]
                    aleatorio=random.randint(0,59)
                    
                    x=arreglox[aleatorio]
                    y=arregloy[aleatorio]
                
                    grid_position = [x, y]
                    logical_positon, valid_input = self.convert_grid_to_logical_position(grid_position)
                    prueba = self.is_grid_occupied(logical_positon, valid_input)
                    print("Fila OCupada RE-----INTENTANDO")

                self.update_board(valid_input, logical_positon)
                self.make_edge(valid_input, logical_positon)
                self.mark_box()
                self.refresh_board()
                self.player1_turn = False
                self.player1_turn = not self.player1_turn    
    
            if self.is_gameover():
                self.display_gameover()
            else:
                self.display_turn_text()
    
                    
        else:
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False      

game_instance = CuerdasyCorrales()
game_instance.mainloop() 

  