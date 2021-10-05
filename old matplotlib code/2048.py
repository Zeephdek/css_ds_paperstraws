import numpy as np
import keyboard
import random
import time
import os

def main():
    global main_array, array_shape, game_status, score, possible_added_numbers
    score = 0
    game_status = True

    ##FULLY MODULAR BOI
    array_shape = [4,4] #default = [4,4]
    possible_added_numbers = [2,4] #default = [2,4]
 

    def create_array():
        return np.zeros(array_shape,dtype=np.int16)

    def print_array():
        print(main_array)

    def random_coord():
        x = random.randint(0,array_shape[0]-1)
        y = random.randint(0,array_shape[1]-1)
        return x,y

    def ini_game():
        num1_value = random.choice(possible_added_numbers)
        x1, y1 = random_coord()
       
        main_array[y1, x1] = num1_value

        #if random.randrange(0,2,1) == 0:
        #num2_value = #random.randrange(2,6,2)
        x2, y2 = random_coord()
        if x1 == x2 and y1 == y2:
            x2, y2 = random_coord()

        main_array[y2, x2] = num1_value #Num1 and Num2 are the same

    def get_empty_squares():
        empty_squares = []
        for y, row in enumerate(main_array):
            for x, value in enumerate(row):
                if value == 0:
                    empty_squares.append([x,y])

        return empty_squares

    def gameinput(key):
        global score
        turn_score = 0

        #print('Game Turn: {}.'.format(key))

        already_added_coords = []

        org_array = create_array()

        for y, row in enumerate(main_array):
            for x, value in enumerate(row): 
                org_array[y,x] = value

        #checks for empty space movement then checks for square stacking
        ###########################################################
        #old checking code
        if key == "up_old":
            for y, row in enumerate(main_array):
                for x, value in enumerate(row): 

                    if y > 0:
                        if main_array[y-1,x] == 0 and y-1 > -1:
                            main_array[y,x] = 0
                            if main_array[y-2,x] == 0 and y-2 > -1:
                                
                                if main_array[y-3,x] == 0 and y-3 > -1:
                                    main_array[y-3,x] = value
                                else:
                                    main_array[y-2,x] = value
                            else:
                                main_array[y-1,x] = value
                        else:
                            main_array[y,x] = value

        elif key == "left_old":
            for y, row in enumerate(main_array):
                for x, value in enumerate(row): 

                    if x > 0:
                        if main_array[y,x-1] == 0 and x-1 > -1:
                            main_array[y,x] = 0
                            if main_array[y,x-2] == 0 and x-2 > -1:
                                
                                if main_array[y,x-3] == 0 and x-3 > -1:
                                    main_array[y,x-3] = value
                                else:
                                    main_array[y,x-2] = value
                            else:
                                main_array[y,x-1] = value
                        else:
                            main_array[y,x] = value

        #####################################################lol

        elif key == "up":
            for y in range(0,array_shape[1]):
                #print(y)
                for x in range(0,array_shape[0]):
                    value = main_array[y,x]
                    #print(x,y,value)
                    if value != 0:
                        #print("Value: {}".format(value))
                        for i in range(1,array_shape[1]+1):
                            
                            if y-i > -1:
                            #print(i)
                                main_array[y,x] = 0
                                if main_array[y-i,x] == 0:
                                    #print("Found zero at [{},{}].".format(x,y-i))
                                    if y-i-1 <= -1:
                                        main_array[y-i,x] = value
                                    continue
                                elif main_array[y-i,x] == value and [y-i,x] not in already_added_coords:
                                    #print("Found same value at [{},{}], adding {} to {}.".format(x,y-i,value,main_array[y-i,x]))
                                    main_array[y-i,x] += value

                                    turn_score += main_array[y-i,x]

                                    already_added_coords.append([y-i,x])
                                    break
                                else:
                                    #print("Found nonzero at [{},{}], [{},{}] is now {}.".format(x,y-i,x,y-i+1,value))
                                    main_array[y-(i-1),x] = value
                                    break
                            else:
                                break

        elif key == "left":  ####SOMEHOW 64 + 64 = -128, and -128 + -128 = 2, sort of broken (fixed)
            for y in range(0,array_shape[1]):
                #print(y)
                for x in range(0,array_shape[0]):
                    value = main_array[y,x]
                    #print(x,y,value)
                    if value != 0:
                        #print("Value: {}".format(value))
                        for i in range(1,array_shape[0]+1):
                            
                            if x-i > -1:
                            #print(i)
                                main_array[y,x] = 0
                                if main_array[y,x-i] == 0:
                                    #print("Found zero at [{},{}].".format(x-i,y))
                                    if x-i-1 <= -1:
                                        main_array[y,x-i] = value
                                    continue
                                elif main_array[y,x-i] == value and [y,x-i] not in already_added_coords:
                                    #print("Found same value at [{},{}], adding {} to {}.".format(x-i,y,value,main_array[y,x-i]))
                                    main_array[y,x-i] += value

                                    turn_score += main_array[y,x-i]

                                    already_added_coords.append([y,x-i])
                                    break
                                else:
                                    #print("Found nonzero at [{},{}], [{},{}] is now {}.".format(x-i,y,x-i+1,y,value))
                                    main_array[y,x-(i-1)] = value
                                    break
                            else:
                                break

        elif key == "down":
            for y in reversed(range(0,array_shape[1])):
                #print(y)
                for x in reversed(range(0,array_shape[0])):
                    value = main_array[y,x]
                    #print(x,y,value)
                    if value != 0:
                        #print("Value: {}".format(value))
                        for i in range(1,array_shape[1]+1):
                            
                            if y+i < array_shape[1]:
                            #print(i)
                                main_array[y,x] = 0
                                if main_array[y+i,x] == 0:
                                    #print("Found zero at [{},{}].".format(x,y+i))
                                    if y+i+1 >= array_shape[1]:
                                        main_array[y+i,x] = value
                                    continue
                                elif main_array[y+i,x] == value and [y+i,x] not in already_added_coords:
                                    #print("Found same value at [{},{}], adding {} to {}.".format(x,y+i,value,main_array[y+i,x]))
                                    main_array[y+i,x] += value

                                    turn_score += main_array[y+i,x]

                                    already_added_coords.append([y+i,x])
                                    break
                                else:
                                    #print("Found nonzero at [{},{}], [{},{}] is now {}.".format(x,y+i,x,y+i-1,value))
                                    main_array[y+(i-1),x] = value
                                    break
                            else:
                                break

        elif key == "right": #broken
            for y in reversed(range(0,array_shape[1])):
                for x in reversed(range(0,array_shape[0])):
                    value = main_array[y,x]
                    if value != 0:
                        #print("Value: {}".format(value))
                        for i in range(1,array_shape[0]+1):
                            
                            if x+i < array_shape[0]:
                            #print(i)
                                main_array[y,x] = 0
                                if main_array[y,x+i] == 0:
                                    if x+i+1 >= array_shape[1]:
                                        main_array[y,x+i] = value
                                    continue
                                elif main_array[y,x+i] == value and [y,x+i] not in already_added_coords:
                                    main_array[y,x+i] += value

                                    turn_score += main_array[y,x+i]

                                    already_added_coords.append([y,x+i])
                                    break
                                else:
                                    main_array[y,x+(i-1)] = value
                                    break
                            else:
                                break
        #print(org_array,main_array)
        score += turn_score
        if np.array_equal(org_array, main_array):
            del org_array
            return False
        else:
            del org_array
            return main_array
        
        #addition error. below

        #
        #C:\Utilities\Scripts\2048.py:143: RuntimeWarning: overflow encountered in byte_scalars
        #main_array[y,x-i] += value
        #

    def add_turn_value(empty_squares):
        if len(empty_squares) == 0:
            loss_cond = True #Actualy not certain, can still move squares, loss and win conds are wip
        else:
            try:    
                bingo_number = random.randint(0,len(empty_squares)-1) #-1 is confusing
                x,y = [empty_squares[bingo_number][i] for i in (0,1)]

                new_value = random.choice(possible_added_numbers)
                
                main_array[y,x] = new_value

                #print("Number ({}) added to [{},{}], chosen from {}.".format(new_value,x,y,empty_squares))
            except:
                loss_cond = True #Doesnt work lol

    def loss_cond_checker(): 
        #main_array = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
        loss = False
        if np.amin(main_array) == 0:
            pass
        else:
            alive = False
            for y in range(0,array_shape[1]):
                for x in range(0,array_shape[0]): 
                    if y + 1 < array_shape[1]:
                        if main_array[y,x] == main_array[y+1,x]:
                            alive = True

                    if x + 1 < array_shape[0]:
                        if main_array[y,x] == main_array[y,x+1]:
                            alive = True

                if alive == True:
                    break

            if not alive:
                loss = True


        return loss #bsically if there is even a zero or two squares with the same number next to each other.

    main_array = create_array()
    ini_game()
    #print_array()

    turn = 0
    print("""2048 "Console" Edition
Use Up, Down, Left, Right Arrow keys to play. 
Goal is to reach 2048.



{game}
            """.format(game = main_array))
    while game_status == True:
        #print(loss_cond)
        #print(loss_cond_checker())
        if loss_cond_checker():
            break
        
        
        while True:
            if keyboard.is_pressed('up'):
                key = 'up'
                break
            elif keyboard.is_pressed('down'):
                key = 'down'
                break
            elif keyboard.is_pressed('left'):
                key = 'left'
                break
            elif keyboard.is_pressed('right'):
                key = 'right'
                break

        gameinput_result = gameinput(key)
        
        if type(gameinput_result) is np.ndarray:
            add_turn_value(get_empty_squares()) ##If no movement from game input don't add, also print
             #refreshing the screen console
            max_value = np.amax(main_array)
            if max_value == 2048:
                max_value = "2048!"

            gameUpdater = """2048 "Console" Edition
Turn: {turn_number}
Score: {score}
Highest Number: {max_value}


{game}
            """.format(turn_number = turn, key = key, game = main_array, score = score, max_value = max_value)
            #Keypress detected: {key}
            os.system('cls')
            print(gameUpdater) 
            turn += 1
        time.sleep(0.16)

    ##losing. 
    print("You have lost :(.")
    input("GOODBYE.")



if __name__ =="__main__":
    main()
