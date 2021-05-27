# Players Object
class player:
    def __init__(self, name):
        self.name = name

    def get_best_score(self, name):
        self.file = name + '.txt'
        if os.path.isfile(self.file): #module qui verifie que le file existe. Si oui, read, sinon return 0
            _playerFile = open(self.file, 'r') #r serve per poter leggere
            return float(_playerFile.read())
            _playerFile.close()
        else:
            return 0

    def save_best_score(self, nowscore):
        self.nowscore = str(nowscore)
        _playerFile = open(self.file, 'w') #mode Write et ça le vide pour ecrire nouveau record
        _playerFile.write(self.nowscore)
        _playerFile.close()

#ask player name
def ask_player_name(n):
    _player = ""
    while len(_player) == 0:
        _player = input("\nPlayer " + n + " enter your name: ")
    return _player

#ask level (E or D)
def ask_level():
    _level = ""
    while _level.upper() != "E" and _level.upper() != "D":
        _level=input("\nThere are 2 levels of difficulty: \n \nE is Easy \nD is difficult \n \nThe level chosen is ")
    return _level.upper()

# print board with available numbers
def game_board():
    print("\t     |     |")
    print("\t  {}  |  {}  |  {}".format(gameboard[0], gameboard[1], gameboard[2]))
    print('\t_____|_____|_____')
    print("\t     |     |")
    print("\t  {}  |  {}  |  {}".format(gameboard[3], gameboard[4], gameboard[5]))
    print('\t_____|_____|_____')
    print("\t     |     |")
    print("\t  {}  |  {}  |  {}".format(gameboard[6], gameboard[7], gameboard[8]))
    print("\t     |     | \n")

#Tic Tac Toe game
# check if number input is still available
def check_shot(number, number_list):
    if number > 9 or number < 1:
        return "ko"
    if number in number_list:
        return "ok"
    return "ko"

#Tic Tac Toe game
# check if number input is still available
def get_first_free(number_list):
    for n in range(0, 10):
        if n in number_list:
            return n

#Tic Tac Toe game
def check_winner(win_sol_all, player_list):
    # check if there i a win line
    for nSerie in range(0, len(win_sol_all)):
        result = all(elem in player_list for elem in win_sol_all[nSerie])
        if result:
            return True
    return False

#Tic Tac Toe game
def check_2_of_3(all_serie_of_3, player_list, number_list):
    # check if there 2 elem in winSol_n, and return the third one... if available
    if len(player_list) != 2:
        return False
    for nSerie in range(0, len(all_serie_of_3)):
        if (player_list[0] in all_serie_of_3[nSerie]) and (player_list[1] in all_serie_of_3[nSerie]):
            w_list = all_serie_of_3[nSerie]  # wList = winSol_n with 2 of 3 ok
            for n in range(0, 3):
                if player_list[0] != w_list[n] and player_list[1] != w_list[n]:
                    w_num = w_list[n]  # wNum = third (missing) num in winSol_n
                    if check_shot(w_num, number_list) == "ok":
                        return w_num
    return 0

# init data
gameboard = [1, 2, 3, 4, 5, 6, 7, 8, 9]
shots_list_player_X= []
shots_list_player_O= []
win_sol_1 = [1, 2, 3]
win_sol_2 = [4, 5, 6]
win_sol_3 = [7, 8, 9]
win_sol_4 = [1, 4, 7]
win_sol_5 = [2, 5, 8]
win_sol_6 = [3, 6, 9]
win_sol_7 = [1, 5, 9]
win_sol_8 = [3, 5, 7]
win_sol_all = [win_sol_1, win_sol_2, win_sol_3, win_sol_4, win_sol_5, win_sol_6, win_sol_7, win_sol_8]

#Game Difficult
def game_1player_D(_name_player_X):  # against the PC
    _tot_time_player_X = 0
    _the_winner_is = "nobody"

    for n_play in range(1, 6):
        # player X is playing...
        # print(" ")
        x = game_board()
        clock = datetime.datetime.now().timestamp()
        shot_player_X = int(input(_name_player_X + " enter a cell number within the range (1-9): "))
        shot_ok = check_shot(shot_player_X, gameboard)
        while shot_ok != "ok":
            x = game_board()
            shot_player_X = int(input(str(
                shot_player_X) + " was already played or is not valid. Please enter another cell number within the range (1-9): "))
            shot_ok = check_shot(shot_player_X, gameboard)

        # stop time for playerX and cumul time
        _tot_time_player_X += (datetime.datetime.now().timestamp() - clock)
        # update board and shots played by Player X
        print(" ")
        gameboard[shot_player_X - 1] = "x"
        shots_list_player_X.append(shot_player_X)

        # check if player X is the winner
        if check_winner(win_sol_all, shots_list_player_X):
            print(_name_player_X + " YOU WIN!", "\n")
            _the_winner_is = "X"
            break

        # "PC" is playing...
        if n_play < 5:
            if n_play == 1:  # 1st shot = 5 or first availaible
                shot_player_O = 5
                if check_shot(5, gameboard) == "ok":
                    shot_player_O = 5
                else:
                    shot_player_O = get_first_free(gameboard)
            else:
                shot_player_O = check_2_of_3(win_sol_all, shots_list_player_X,
                                        gameboard)  # defending!! stop player X choosing the 3rd of winSol
                if shot_player_O == 0:
                    shot_player_O = check_2_of_3(win_sol_all, shots_list_player_O,
                                            gameboard)  # attacking!! search 3rd of winSol in PC shotslist
                    if shot_player_O == 0:
                        shot_player_O = get_first_free(gameboard)

            # update board and shots played by Player X
            gameboard[shot_player_O - 1] = "o"
            shots_list_player_O.append(shot_player_O)
            print(" ")
            print("PC has played... \n ")

            # check if PC is the winner
            if check_winner(win_sol_all, shots_list_player_O):
                _the_winner_is = "_PC"
                break
    return [_tot_time_player_X, 0, _the_winner_is]

#Game Easy
def game_1player_E(_name_player_X):  # against the PC
    _tot_time_player_X = 0
    # _totTimePlayerO = 0
    _the_winner_is = "nobody"

    for n_play in range(1, 6):
        # player X is playing...
        # print(" ")
        x = game_board()
        clock = datetime.datetime.now().timestamp()
        shot_player_X = int(input(_name_player_X + " enter a cell number within the range (1-9): "))
        shot_ok = check_shot(shot_player_X, gameboard)
        while shot_ok != "ok":
            # print(" ")
            x = game_board()
            shot_player_X = int(input(str(
                shot_player_X) + " was already played or is not valid. Please enter another cell number within the range (1-9): "))
            shot_ok = check_shot(shot_player_X, gameboard)

        # stop time for playerX and cumul time
        _tot_time_player_X += (datetime.datetime.now().timestamp() - clock)
        # update board and shots played by Player X
        print(" ")
        gameboard[shot_player_X - 1] = "x"
        shots_list_player_X.append(shot_player_X)

        # check if player X is the winner
        if check_winner(win_sol_all, shots_list_player_X):
            print(_name_player_X+ " YOU WIN!", "\n")
            _the_winner_is = "X"
            break

        # "PC" is playing...
        if n_play < 5:
            #shotPlayerO = getFirstFree(GameBoard)
            shot_player_O = random.randrange(10)
            while check_shot(shot_player_O, gameboard) != "ok":
                shot_player_O = random.randrange(10)

            # update board and shots played by Player X
            gameboard[shot_player_O - 1] = "o"
            shots_list_player_O.append(shot_player_O)
            print(" ")
            print("PC has played... \n ")

            # check if PC is the winner
            if check_winner(win_sol_all, shots_list_player_O):
                _the_winner_is = "_PC"
                break
    return [_tot_time_player_X, 0, _the_winner_is]

def display_final_result(_the_winner_is, _name_player_X, _tot_time_player_X, _tot_time_player_O):
    x = game_board()

    if _the_winner_is == "X":
        ##create Objet to manage the file of player with bestscore
        player_X = player(_name_player_X)
        best_score_X = player_X.get_best_score(_name_player_X)
        print(_name_player_X + " won in " + str(_tot_time_player_X) + " seconds")
        print("\n" + _name_player_X + "'s last best time was " + str(best_score_X))
        if best_score_X == 0 or str(_tot_time_player_X) < str(best_score_X):
            print("\n" + _name_player_X + "'s new best time is " + str(_tot_time_player_X))
            player_X.save_best_score(str(_tot_time_player_X))

    elif _the_winner_is == "_PC":
        print(_name_player_X + " YOU LOST!")

    else:
        print("NO WINNER... try again!")

def user_menu():
    print("===============================")
    print("\t    Main Menu")
    print("===============================\n")
    print("\t    Your choice\n")
    print("\t    1. Play Game")
    print("\t    2. Display best score")
    print("\t    3. Exit Game\n")
    print("===============================")

    while True:
        your_choice = int(input("\nPlease enter your choice : "))
        if (your_choice > 0 and your_choice < 5):
            if your_choice == 1:
                # ask player's name
                name_player_X = ask_player_name("X")
                level=ask_level()
                print()
                if level.upper() == "D":
                    x = game_1player_D(name_player_X)
                else:
                    x = game_1player_E(name_player_X)
                tot_time_player_X = round(x[0], 2)
                tot_time_player_O = 0
                display_final_result(x[2], name_player_X,tot_time_player_X, tot_time_player_O)
            elif your_choice == 2:
                name_player_score = ask_player_name("X")
                player_X = player(name_player_score)
                print("\n Your best score is : " + str(player_X.get_best_score(name_player_score)))
            elif your_choice == 3:
                False
            break
        else:
            print("\nINVALID INPUT... Please enter a number between 1 and 3")

# end of Functions definitions
import datetime, os.path, random

# execute Program
user_menu()
