import pygame
pygame.font.init()   # Initialize the pygame font system
screen = pygame.display.set_mode((650, 750))   # Defining pygame window dimensions 
pygame.display.set_caption("SUDOKU SOLVER")    

# x and y are selected cell's coordinates
x = -1  
y = -1  
dif = 500 / 9    # defining size of each grid cell
val = 0  
grid = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]
font1 = pygame.font.SysFont("cambriacambriamath", 40)  # for numbers in cells
font2 = pygame.font.SysFont("cambriacambriamath", 25)  # for instructions and messages
x_offset = (650 - 500) // 2  
y_offset = 100  

# Get cell coordinated from mouse position
def get_cord(pos):  # pos is tuple(x, y)
    global x, y
    x = (pos[0] - x_offset) // dif  
    y = (pos[1] - y_offset) // dif  

# Highlight the selected cell
def draw_box():
    if x >= 0 and y >= 0:  
        for i in range(2):
            # for horizontal lines
            pygame.draw.line(screen, (255, 0, 0), (x_offset + x * dif - 3, y_offset + (y + i) * dif),
                             (x_offset + x * dif + dif + 3, y_offset + (y + i) * dif), 7)
            # for vertical lines
            pygame.draw.line(screen, (255, 0, 0), (x_offset + (x + i) * dif, y_offset + y * dif),
                             (x_offset + (x + i) * dif, y_offset + y * dif + dif), 7)

# Function to draw the Sudoku grid
def draw():
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                pygame.draw.rect(screen, (0, 153, 153), (x_offset + i * dif, y_offset + j * dif, dif + 1, dif + 1))
                text1 = font1.render(str(grid[i][j]), 1, (0, 0, 0))  #1 is used to remove jaggered edges
                screen.blit(text1, (x_offset + i * dif + 15, y_offset + j * dif + 15))  

    for i in range(10):  
        if i % 3 == 0:
            thick = 7
        else:
            thick = 1
       # Draw vertical lines (columns)
        pygame.draw.line(screen, (0, 0, 0), (x_offset + i * dif , y_offset), 
                         (x_offset + i * dif , y_offset + 500), thick)
        
        # Draw horizontal lines (rows)
        pygame.draw.line(screen, (0, 0, 0), (x_offset - 3, y_offset + i * dif), 
                         (x_offset + 500 + 3, y_offset + i * dif), thick)

def draw_val(val):
    text1 = font1.render(str(val), 1, (0, 0, 0))
    screen.blit(text1, (x_offset + x * dif + 15, y_offset + y * dif + 15))

# Raise error when wrong value entered
def raise_error1():
    text1 = font1.render("WRONG !!!", 1, (255, 0, 0))
    screen.blit(text1, (x_offset + 180, y_offset + 520))  

def raise_error2():
    text1 = font1.render("Wrong !!! Not a valid Key", 1, (255, 0, 0))
    screen.blit(text1, (x_offset + 100, y_offset + 520))  

# Check if the value entered in board is valid
def valid(m, i, j, val):
    for it in range(9):
        if m[i][it] == val:
            return False
        if m[it][j] == val:
            return False
    # To reach the starting cell of sub-grid
    it = i // 3
    jt = j // 3
    for i in range(it * 3, it * 3 + 3):
        for j in range(jt * 3, jt * 3 + 3):
            if m[i][j] == val:
                return False
    return True

# Solves the sudoku board using Backtracking Algorithm
def solve(grid, i, j):
    while grid[i][j] != 0:
        if i < 8:
            i += 1
        elif i == 8 and j < 8:
            i = 0
            j += 1
        elif i == 8 and j == 8:
            return True
    pygame.event.pump()  # Ensures event queue in Pygame is updated
    for it in range(1, 10):
        if valid(grid, i, j, it) == True:
            grid[i][j] = it
            global x, y  
            x = i
            y = j
            screen.fill((255, 255, 255))  # Clears the screen
            draw()  
            draw_box()  
            pygame.display.update()
            pygame.time.delay(20)  
            if solve(grid, i, j) == 1:  # Recursion call
                return True
            else:
                grid[i][j] = 0  # Backtracking
            screen.fill((255, 255, 255))
            draw()
            draw_box()
            pygame.display.update()
            pygame.time.delay(50)
    return False

def instruction():
    text1 = font2.render("PRESS D TO RESET TO DEFAULT / R TO EMPTY BOARD", 1, (0, 0, 0))
    text2 = font2.render("ENTER VALUES AND PRESS ENTER TO VISUALIZE", 1, (0, 0, 0))
    screen.blit(text1, (x_offset + 20, 20))  
    screen.blit(text2, (x_offset + 35, 50))  

def result():
    text1 = font1.render("FINISHED!! PRESS R or D", 1, (0, 0, 0))
    screen.blit(text1, (x_offset + 80, y_offset + 570)) 

run = True
flag1 = 0  # to track active interaction with a cell 
flag2 = 0  # to triger the solving process 
rs = 0     # acts as an indicator of whether the puzzle has been solved
error = 0  # used to track any invalid action

# The loop that keeps the window running
while run:
    screen.fill((255, 255, 255))
    instruction()  
    draw()  
    draw_box()  
    pygame.display.update()  

    for event in pygame.event.get():   # pygame.event.get() is a list of all the user-actions
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag1 = 1
            pos = pygame.mouse.get_pos()   
            get_cord(pos)   
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= 1
                flag1 = 1
            if event.key == pygame.K_RIGHT:
                x += 1
                flag1 = 1
            if event.key == pygame.K_UP:
                y -= 1
                flag1 = 1
            if event.key == pygame.K_DOWN:
                y += 1
                flag1 = 1
            if event.key == pygame.K_1:
                val = 1
            if event.key == pygame.K_2:
                val = 2
            if event.key == pygame.K_3:
                val = 3
            if event.key == pygame.K_4:
                val = 4
            if event.key == pygame.K_5:
                val = 5
            if event.key == pygame.K_6:
                val = 6
            if event.key == pygame.K_7:
                val = 7
            if event.key == pygame.K_8:
                val = 8
            if event.key == pygame.K_9:
                val = 9
            if event.key == pygame.K_RETURN:
                flag2 = 1  # indicating triggering of solving function
            # If R pressed clear the sudoku board
            if event.key == pygame.K_r:
                rs = 0  
                error = 0  
                flag2 = 0
                grid = [[0] * 9 for x in range(9)]  
            # If D is pressed reset the board to default 
            if event.key == pygame.K_d:
                rs = 0
                error = 0
                flag2 = 0
                grid = [
                    [7, 8, 0, 4, 0, 0, 1, 2, 0],
                    [6, 0, 0, 0, 7, 5, 0, 0, 9],
                    [0, 0, 0, 6, 0, 1, 0, 7, 8],
                    [0, 0, 7, 0, 4, 0, 2, 6, 0],
                    [0, 0, 1, 0, 5, 0, 9, 3, 0],
                    [9, 0, 4, 0, 6, 0, 0, 0, 5],
                    [0, 7, 0, 3, 0, 0, 0, 1, 2],
                    [1, 2, 0, 0, 0, 7, 4, 0, 0],
                    [0, 4, 9, 2, 0, 6, 0, 0, 7]
                    ]  

    if flag2 == 1:   
        if solve(grid, 0, 0) == False:
            error = 1
        else:
            rs = 1  # sudoku solved if rs = 1
        flag2 = 0

    if val != 0:         
        draw_val(val)
        if valid(grid, int(x), int(y), val) == True:
            grid[int(x)][int(y)] = val
            flag1 = 0
        else:
            grid[int(x)][int(y)] = 0
            raise_error2() 
            pygame.display.update()
            pygame.time.delay(1000)
        val = 0
    
    if error == 1:
        raise_error1() 
        pygame.display.update()
        pygame.time.delay(1000)
    if rs == 1:
        result()
        pygame.display.update()
        pygame.time.delay(1000)
    draw() 
    if flag1 == 1:
        draw_box()     
        instruction() 
        pygame.display.update()
pygame.quit()