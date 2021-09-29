import sys, pygame , random, time
import db_manager

########################################################################################################################
#   GLOBAL VARIABLES    ################################################################################################

pw = "6yzKjs3Mdu"
uname = "sql6411632"
connection = db_manager.create_server_connection("sql6.freemysqlhosting.net", uname, pw)

use_db_query = "USE sql6411632"
db_manager.execute_query(connection, use_db_query)

pygame.init()
WINDOWWIDTH = 800
WINDOWHEIGHT = 512
FPS = 30

user_id = 0
user_name = None

CARWIDTH = WINDOWWIDTH / 9
CARHEIGHT = WINDOWHEIGHT / 4
RECTWIDTH = WINDOWWIDTH / 32
RECTHEIGHT = WINDOWHEIGHT / 16
COINSIZE = WINDOWWIDTH / 16
YDIFF = WINDOWHEIGHT / 8

STEP = 5

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
lime = (180,255,100)
cyan = (0, 255, 255, 255)
dark_blue = (72, 61, 139, 255)
pink = (255, 192, 203, 255)

clock = pygame.time.Clock()
DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

car = pygame.image.load('Assets/car.png')
road = pygame.image.load('Assets/road.png')
coin = pygame.image.load('Assets/coin.png')
inc = pygame.image.load('Assets/inc.png')
background_image = pygame.image.load('Assets/space_background_1.PNG').convert()
background_image_2 = pygame.image.load('Assets/space_background_2.PNG').convert()
background_image_3 = pygame.image.load('Assets/space_background_3.PNG').convert()

point_sound = pygame.mixer.Sound('Assets/eat.ogg')

smallfont = pygame.font.Font(None, 28)
menufont = pygame.font.Font(None, 48)
overfont = pygame.font.Font(None, 60)

pygame.display.set_caption("CAR GAME")


########################################################################################################################
#   GAME LOOP   ########################################################################################################

def gamedloop(user_name, status):
    #   CALLING START MENU  ############################################################################################
    if status == 0 :
        main_menu(user_name, 0)
    ####################################################################################################################

    # points
    points = 0

    RECTX, RECTY = WINDOWWIDTH / 2, 0
    CARX, CARY = WINDOWWIDTH / 2, WINDOWHEIGHT / 2 + CARHEIGHT
    COINX, COINY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0
    INCX, INCY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0

    # initial direction
    direction = -1  # -1 is left,1 is right

    ####################################################################################################################
    #   GAME PHYSICS    ################################################################################################
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = -1
                elif event.key == pygame.K_RIGHT:
                    direction = 1
                elif event.key == pygame.K_UP:
                    direction = 0
                elif event.key == pygame.K_ESCAPE:
                    pause()
        if direction == -1:
            CARX -= STEP
        elif direction == 1:
            CARX += STEP
        DISPLAY.fill(white)
        DISPLAY.blit(road, (0, 0))
        if (check_coin(CARX, CARY, COINX, COINY)):
            COINX, COINY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0
            points += 1

        RECTY += STEP
        RECTY = RECTY % YDIFF
        COINY += STEP
        INCY += 2 * STEP

        if COINY >= WINDOWHEIGHT:
            COINX, COINY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0
        if INCY >= WINDOWHEIGHT:
            INCX, INCY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0

        for i in range(-1, 8):
            pygame.draw.rect(DISPLAY, black, [RECTX, RECTY + i * YDIFF, RECTWIDTH, RECTHEIGHT])
        DISPLAY.blit(coin, (COINX, COINY))
        DISPLAY.blit(car, (CARX, CARY))

        DISPLAY.blit(inc, (INCX, INCY))

        text = smallfont.render('Score: ' + str(points), True, black)
        DISPLAY.blit(text, (0, 0))

        car_crash(CARX, CARY, INCX, INCY, points, user_name)
        if check_step_out(CARX):
            if CARX < 0.1 * WINDOWWIDTH:
                for i in range(0, 20):
                    DISPLAY.fill(white)
                    DISPLAY.blit(road, (0, 0))
                    if (check_coin(CARX, CARY, COINX, COINY)):
                        COINX, COINY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0
                        points += 1

                    RECTY += STEP
                    RECTY = RECTY % YDIFF
                    COINY += STEP
                    INCY += 2 * STEP
                    CARX -= STEP
                    CARY -= STEP

                    if COINY >= WINDOWHEIGHT:
                        COINX, COINY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0
                    if INCY >= WINDOWHEIGHT:
                        INCX, INCY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0

                    new_car = pygame.transform.rotate(car, 10 + 3 * i)

                    for i in range(-1, 8):
                        pygame.draw.rect(DISPLAY, black, [RECTX, RECTY + i * YDIFF, RECTWIDTH, RECTHEIGHT])
                    DISPLAY.blit(coin, (COINX, COINY))
                    DISPLAY.blit(new_car, (CARX, CARY))

                    DISPLAY.blit(inc, (INCX, INCY))

                    text = smallfont.render('Score: ' + str(points), True, black)
                    DISPLAY.blit(text, (0, 0))
                    clock.tick(FPS)
                    pygame.display.update()
            if CARX > 0.78 * WINDOWWIDTH:
                for i in range(0, 20):
                    DISPLAY.fill(white)
                    DISPLAY.blit(road, (0, 0))
                    if (check_coin(CARX, CARY, COINX, COINY)):
                        COINX, COINY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0
                        points += 1

                    RECTY += STEP
                    RECTY = RECTY % YDIFF
                    COINY += STEP
                    INCY += 2 * STEP
                    CARX += STEP
                    CARY -= STEP

                    if COINY >= WINDOWHEIGHT:
                        COINX, COINY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0
                    if INCY >= WINDOWHEIGHT:
                        INCX, INCY = random.randrange(0.2 * WINDOWWIDTH, 0.8 * WINDOWWIDTH, STEP), 0

                    new_car = pygame.transform.rotate(car, -(10 + 3 * i))

                    for i in range(-1, 8):
                        pygame.draw.rect(DISPLAY, black, [RECTX, RECTY + i * YDIFF, RECTWIDTH, RECTHEIGHT])
                    DISPLAY.blit(coin, (COINX, COINY))
                    DISPLAY.blit(new_car, (CARX, CARY))

                    DISPLAY.blit(inc, (INCX, INCY))

                    text = smallfont.render('Score: ' + str(points), True, black)
                    DISPLAY.blit(text, (0, 0))
                    clock.tick(FPS)
                    pygame.display.update()

            ############################################################################################################
            #   CALLING GAME OVER   ####################################################################################
            post_game_processing(user_name, points)
            ############################################################################################################

        clock.tick(FPS)
        pygame.display.update()


########################################################################################################################
#   IGNORE IMPLEMENTATION DETAILS   ####################################################################################

def check_coin(CARX, CARY, COINX, COINY):
    if (CARX - COINX) <= COINSIZE and (COINX - CARX) <= CARWIDTH:
        if (CARY - COINY) <= COINSIZE and (COINY - CARY) <= CARHEIGHT:
            point_sound.play()
            return True


def car_crash(CARX, CARY, INCX, INCY, points, user_name):
    if (CARX - INCX) <= CARWIDTH and (INCX - CARX) <= CARWIDTH:
        if (CARY - INCY) <= CARHEIGHT and (INCY - CARY) <= CARHEIGHT:
            post_game_processing(user_name, points)


########################################################################################################################
########################################      GAME SCREENS                            ##################################

########################################################################################################################
#   LOGIN   ############################################################################################################

# error -> 1 = print password wrong
def login(error):
    user_name, password = user_input(error)

    # validate user_name and password and proceed appropriately
    # -1 = wrong password, 0 = success, 1 = name not found
    flag = db_manager.validate_password(connection, user_name, password)

    if flag == 0 :
        gamedloop(user_name, 0)

    elif flag == -1 :
        login(1)

    elif flag == 1 :
        user_doesnt_exist(user_name, password)

########################################################################################################################
#   USER DOESNT EXIST   ################################################################################################

def user_doesnt_exist(user_name,password):
    point = 0

    while 1:

        DISPLAY.blit(background_image, [0, 0])
        message1 = menufont.render('User does not exist.', True, white)
        message2 = menufont.render('Select YES to signup, NO to go back', True, pink)

        DISPLAY.blit(message1, (WINDOWWIDTH / 10, WINDOWHEIGHT / 10))
        DISPLAY.blit(message2, (WINDOWWIDTH / 10, WINDOWHEIGHT * 3 / 10))

        if point == 0:
            yes = menufont.render('YES', True, red)
            no = menufont.render('NO', True, white)
        elif point == 1:
            yes = menufont.render('YES', True, white)
            no = menufont.render('NO', True, red)
        DISPLAY.blit(yes, (WINDOWWIDTH / 10, 5 * WINDOWHEIGHT / 10))
        DISPLAY.blit(no, (WINDOWWIDTH / 10, 7 * WINDOWHEIGHT / 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    point += 1
                elif event.key == pygame.K_UP:
                    point -= 1
                elif event.key == pygame.K_RETURN:
                    #IF YES
                    if point == 0:
                    # SAVE THE USER ID AND PASSWORD
                        db_manager.insert_into_user(connection, user_name, password)
                    # GO TO START MENU OF THE GAME PAGE
                        main_menu(user_name, 0)

                    #IF NO
                    elif point == 1:
                    # GO TO LOGIN PAGE
                        login(0)

        point = point % 2
        clock.tick(FPS)
        pygame.display.update()

########################################################################################################################
#   MAIN MENU   ########################################################################################################

def main_menu(user_name, status):
    # if status is  1, then print friend added successfully
    point = 0
    friend_added = menufont.render('friend added successfully', True, green)
    while 1:
        DISPLAY.blit(background_image, [0, 0])
        if status == 1 :
            DISPLAY.blit(friend_added, (4  * WINDOWWIDTH / 10,  9 * WINDOWHEIGHT / 10))
        if point == 0:
            start = menufont.render('START GAME', True, red)
            friend = menufont.render('ADD FRIENDS', True, white)
            quit = menufont.render('QUIT GAME', True, white)

        elif point == 1 :
            start = menufont.render('START GAME', True, white)
            friend = menufont.render('ADD FRIENDS', True, red)
            quit = menufont.render('QUIT GAME', True, white)

        elif point == 2:
            start = menufont.render('START GAME', True, white)
            friend = menufont.render('ADD FRIENDS', True, white)
            quit = menufont.render('QUIT GAME', True, red)

        DISPLAY.blit(start, (WINDOWWIDTH / 10, WINDOWHEIGHT / 10))
        DISPLAY.blit(friend, (WINDOWWIDTH / 10, WINDOWHEIGHT * 3 / 10))
        DISPLAY.blit(quit, (WINDOWWIDTH / 10,  5 * WINDOWHEIGHT / 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    point += 1
                elif event.key == pygame.K_UP:
                    point -= 1
                elif event.key == pygame.K_RETURN:
                    if point == 0:
                        gamedloop(user_name, 1)

                    elif point == 1 :
                        friend_screen(0, user_name)

                    elif point == 2:
                        pygame.quit()
                        sys.exit()

        point = point % 3
        clock.tick(FPS)
        pygame.display.update()

########################################################################################################################
#   ADD FRIENDS   ######################################################################################################

def friend_screen(error, user_name) :

    friend = friend_input(error)
    flag = db_manager.validate_friend(connection, friend)

    # success
    if flag == 0 :
        db_manager.insert_into_friend(connection, user_name, friend)
        main_menu(user_name, 1)

    else :
        friend_screen(1, user_name)

########################################################################################################################
#   POST GAME PROCESSING    ############################################################################################

def post_game_processing(user_name, points) :

    result = get_highscore(connection)
    process_hs(connection, user_name, points, result)

########################################################################################################################
#   GAME OVER SCREEN NO HIGHSCORE    ###################################################################################

def post_game(user_name, score, hs_score, hs_name):

    point = 0

    message1 = menufont.render('SCORE - ' + str(score), True, white)
    message2 = menufont.render('score to beat -> ' + str(hs_score) + ' set by ' + hs_name, True, white)

    while 1:
        DISPLAY.blit(background_image, [0, 0])
        if point == 0:
            start = menufont.render('PLAY AGAIN', True, red)
            leaderboard = menufont.render('LEADERBOARD', True, white)
            quit = menufont.render('QUIT GAME', True, white)
        elif point == 1:
            start = menufont.render('PLAY AGAIN', True, white)
            leaderboard = menufont.render('LEADERBOARD', True, red)
            quit = menufont.render('QUIT GAME', True, white)
        elif point == 2:
            start = menufont.render('PLAY AGAIN', True, white)
            leaderboard = menufont.render('LEADERBOARD', True, white)
            quit = menufont.render('QUIT GAME', True, red)

        DISPLAY.blit(message1, (WINDOWWIDTH / 10, WINDOWHEIGHT / 10))
        DISPLAY.blit(message2, (WINDOWWIDTH / 10, 2 * WINDOWHEIGHT / 10))
        DISPLAY.blit(start, (WINDOWWIDTH / 10, WINDOWHEIGHT * 5 / 10))
        DISPLAY.blit(leaderboard, (WINDOWWIDTH / 10,  7 * WINDOWHEIGHT / 10))
        DISPLAY.blit(quit, (WINDOWWIDTH / 10, 9 * WINDOWHEIGHT / 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    point += 1
                elif event.key == pygame.K_UP:
                    point -= 1
                elif event.key == pygame.K_RETURN:
                    if point == 0:
                        gamedloop(user_name, 1)
                    elif point == 1:
                        #leaderboard
                        leaderboard_selector(user_name)

                    elif point == 2:
                        pygame.quit()
                        sys.exit()

        point = point % 3
        clock.tick(FPS)
        pygame.display.update()

########################################################################################################################
#   GAME OVER SCREEN NO HIGHSCORE    ###################################################################################

def post_game_hs(user_name, score, hs_score, hs_name):

    point = 0

    while 1:
        DISPLAY.blit(background_image, [0, 0])
        message1 = menufont.render('score - ' + str(score) + ' HIGHSCORE !!!', True, white)
        message2 = menufont.render('YOU JUST BEAT ' + hs_name, True, white)
        if point == 0:
            start = menufont.render('PLAY AGAIN', True, red)
            leaderboard = menufont.render('LEADERBOARD', True, white)
            quit = menufont.render('QUIT GAME', True, white)
        elif point == 1:
            start = menufont.render('PLAY AGAIN', True, white)
            leaderboard = menufont.render('LEADERBOARD', True, red)
            quit = menufont.render('QUIT GAME', True, white)
        elif point == 2:
            start = menufont.render('PLAY AGAIN', True, white)
            leaderboard = menufont.render('LEADERBOARD', True, white)
            quit = menufont.render('QUIT GAME', True, red)

        DISPLAY.blit(message1, (WINDOWWIDTH / 10, WINDOWHEIGHT / 10))
        DISPLAY.blit(message2, (WINDOWWIDTH / 10, WINDOWHEIGHT * 2 / 10))
        DISPLAY.blit(start, (WINDOWWIDTH / 10, WINDOWHEIGHT * 5 / 10))
        DISPLAY.blit(leaderboard, (WINDOWWIDTH / 10,  7 * WINDOWHEIGHT / 10))
        DISPLAY.blit(quit, (WINDOWWIDTH / 10, 9 * WINDOWHEIGHT / 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    point += 1
                elif event.key == pygame.K_UP:
                    point -= 1
                elif event.key == pygame.K_RETURN:
                    if point == 0:
                        gamedloop(user_name, 1)
                    elif point == 1:
                        #leaderboard
                        print()
                    elif point == 2:
                        pygame.quit()
                        sys.exit()

        point = point % 3
        clock.tick(FPS)
        pygame.display.update()

########################################################################################################################
#   LEADERBOARD SELECTOR   #############################################################################################

def leaderboard_selector(user_name) :
    point = 0

    prompt = menufont.render('SELECT LEADERBOARD', True, white)
    while 1:
        DISPLAY.blit(background_image, [0, 0])

        if point == 0:
            global_message = menufont.render('GLOBAL LEADERBOARD', True, red)
            local_message = menufont.render('FRIENDS LEADRERBOARD', True, white)
            back = menufont.render('back', True, white)

        elif point == 1:
            global_message = menufont.render('GLOBAL LEADERBOARD', True, white)
            local_message = menufont.render('FRIENDS LEADRERBOARD', True, red)
            back = menufont.render('back', True, white)

        elif point == 2 :
            global_message = menufont.render('GLOBAL LEADERBOARD', True, white)
            local_message = menufont.render('FRIENDS LEADRERBOARD', True, white)
            back = menufont.render('back', True, red)

        DISPLAY.blit(prompt, (WINDOWWIDTH / 10, WINDOWHEIGHT / 10))
        DISPLAY.blit(global_message, (WINDOWWIDTH / 10, WINDOWHEIGHT * 3 / 10))
        DISPLAY.blit(local_message, (WINDOWWIDTH / 10, 5 * WINDOWHEIGHT / 10))
        DISPLAY.blit(back, (WINDOWWIDTH / 10, 7 * WINDOWHEIGHT / 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    point += 1
                elif event.key == pygame.K_UP:
                    point -= 1
                elif event.key == pygame.K_RETURN:
                    if point == 0:
                        print()
                        ################# call global leaderboard(user_name)
                        global_leaderboard(user_name)

                    elif point == 1:
                        print()
                        ################# call local leaderboarf(user_name)
                        friends_leaderboard(user_name)

                    elif point == 2:
                        return

        point = point % 3
        clock.tick(FPS)
        pygame.display.update()

########################################################################################################################
#   GLOBAL LEADERBOARD  ################################################################################################

def global_leaderboard(user_name) :
    global_message = menufont.render('GLOBAL LEADERBOARD', True, white)


########################################################################################################################
#   FRIENDS LEADERBOARD  ###############################################################################################

def friends_leaderboard(user_name) :
    local_message = menufont.render('FRIENDS LEADERBOARD', True, white)

########################################################################################################################
########################################################################################################################
########################################################################################################################
#   PAUSE GAME  ########################################################################################################

def pause():
    pause = overfont.render('PAUSED', True, red)
    DISPLAY.blit(pause, (0.4 * WINDOWWIDTH, WINDOWHEIGHT / 3))
    pygame.display.update()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return


########################################################################################################################
########################################################################################################################

def check_step_out(CARX):
    if CARX < 0.1 * WINDOWWIDTH or CARX > 0.78 * WINDOWWIDTH:
        return True
    return False


########################################################################################################################
#   WAIT FOR KEY PRESS  ################################################################################################

def wait_for_key_press():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

########################################################################################################################
#   USER INPUT  ########################################################################################################

def user_input(error) :

    clock = pygame.time.Clock()
    input = ''

    done = False

    counter = 0

    while not done:

        for event in pygame.event.get() :
            if done :
                break
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Do something with the password and reset it.
                    user_name = input  # I just print it to see if it works.
                    print(user_name)
                    input = ''
                    done = True

                elif event.key == pygame.K_BACKSPACE :
                    input = '' if len(input) == 1 else input[0 : len(input) - 1]

                else:  # Add the character to the password string.h
                    input += event.unicode

        #DISPLAY.fill((30, 30, 30))
        if counter < 2 :
            DISPLAY.blit(background_image, [0, 0])
        elif counter < 4 :
            DISPLAY.blit(background_image_2, [0, 0])
        elif counter < 6 :
            DISPLAY.blit(background_image_2, [0, 0])

        counter += 1
        counter = counter % 6

        # Render the asterisks and blit them.
        user_name_prompt = menufont.render("ENTER PLAYER NAME : ", True, lime)
        username_surface = menufont.render(input, True, white)
        error_prompt = menufont.render("password doesnt match username", True, red)

        DISPLAY.blit(user_name_prompt, (30, 30))
        DISPLAY.blit(username_surface, (3 * WINDOWWIDTH / 5, 30))
        if error == 1 :
            DISPLAY.blit(error_prompt, (30, 9 * WINDOWHEIGHT / 10))

        pygame.display.flip()
        clock.tick(30)

    #   password    #######################

    done = False

    password = ''

    while not done:
        for event in pygame.event.get():
            if done:
                break
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Do something with the password and reset it.
                    password = input  # I just print it to see if it works.
                    print(password)
                    input = ''
                    done = True

                elif event.key == pygame.K_BACKSPACE:
                    input = '' if len(input) == 1 else input[0: len(input) - 1]

                else:  # Add the character to the password string.h
                    input += event.unicode

        #DISPLAY.fill((30, 30, 30))
        DISPLAY.blit(background_image, [0, 0])

        # Render the asterisks and blit them.
        #(70, 200, 150)
        user_name_prompt = menufont.render("ENTER PLAYER NAME : ", True, lime)
        password_prompt = menufont.render("ENTER PASSWORD : ", True, white)
        username_surface = menufont.render(user_name, True, white)
        password_surface = menufont.render('*' * len(input), True, white)
        error_prompt = menufont.render("password doesnt match username", True, red)

        DISPLAY.blit(user_name_prompt, (30, 30))
        DISPLAY.blit(username_surface, (3 * WINDOWWIDTH / 5, 30))
        DISPLAY.blit(password_prompt, (30, 120))
        DISPLAY.blit(password_surface, (3 * WINDOWWIDTH / 5, 120))
        if error == 1:
            DISPLAY.blit(error_prompt, (30, 9 * WINDOWHEIGHT / 10))

        pygame.display.flip()
        clock.tick(30)

    print("user input successfull")
    return user_name, password

########################################################################################################################
#   GET FRIEND INPUT  ##################################################################################################

def friend_input(error) :

    clock = pygame.time.Clock()
    input = ''

    done = False

    while not done:
        for event in pygame.event.get() :
            if done :
                break
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Do something with the password and reset it.
                    user_name = input  # I just print it to see if it works.
                    print(user_name)
                    input = ''
                    done = True

                elif event.key == pygame.K_BACKSPACE :
                    input = '' if len(input) == 1 else input[0 : len(input) - 1]

                else:  # Add the character to the password string.h
                    input += event.unicode

        #DISPLAY.fill((30, 30, 30))
        DISPLAY.blit(background_image, [0, 0])

        # Render the asterisks and blit them.
        lol_prompt = menufont.render("U HAVE FRIENDS ? ", True, lime)
        user_name_prompt = menufont.render("FRIEND NAME : ", True, lime)
        username_surface = menufont.render(input, True, white)
        error_prompt = menufont.render("player does not exist", True, red)

        DISPLAY.blit(lol_prompt, (30, 30))
        DISPLAY.blit(user_name_prompt, (30, 100))
        DISPLAY.blit(username_surface, (3 * WINDOWWIDTH / 5, 100))
        if error == 1 :
            DISPLAY.blit(error_prompt, (30, 9 * WINDOWHEIGHT / 10))

        pygame.display.flip()
        clock.tick(30)

    return user_name

########################################################################################################################
#   GET HIGHSCORE DETAILS   ############################################################################################

def get_highscore(connection) :

    query = """ SELECT user_name AS high_name, MAX(score) as max_score
                FROM game_data_car
                LIMIT 1
            """
    result = db_manager.read_query(connection, query)

    return result

########################################################################################################################
#   PROCESSING HIGHSCORE RESULTS   #####################################################################################

def process_hs(connection, user_name, cur_score, hs_tuple) :

    print(hs_tuple)

    if not hs_tuple[0][0] == None :
        hs_name = hs_tuple[0][0]
        hs_score = int(hs_tuple[0][1])
    else :
        hs_name = "yourself"
        hs_score = -1

    db_manager.insert_into_game_data_car(connection, user_name, cur_score)
    # you have just set a highscore
    if cur_score >= hs_score :
        post_game_hs(user_name, cur_score, hs_score, hs_name)

    else :
        post_game(user_name, cur_score, hs_score, hs_name)


########################################################################################################################
#   AFTER INITIAIZATION     ############################################################################################

login(0)