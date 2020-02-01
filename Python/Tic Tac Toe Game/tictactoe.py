"""
    TIC TAC TOE GAME
    You can play it with your numpad
"""
import pandas as pd


def game_init(players_dict, player_number=2):
    """
        This function is used to initialize the players information and start the game
    """

    # Let the player choose their symbol
    for i in range(player_number):
        while True:
            nameInput = input(
                f"\t{players_dict[i]['name']}, please enter your name (default = {players_dict[i]['name']}) : ")

            if i == 0:
                if len(nameInput) > 0 and nameInput.capitalize() != players_dict[i + 1]['name']:
                    players_dict[i]['name'] = nameInput.capitalize()
                    break
                elif len(nameInput) == 0:
                    break

            else:
                if len(nameInput) > 0 and nameInput.capitalize() != players_dict[i - 1]['name']:
                    players_dict[i]['name'] = nameInput.capitalize()
                    break
                elif len(nameInput) == 0:
                    break

        while True:
            symbolInput = input(
                f"\t{players_dict[i]['name']}, please choose your symbol (default = {players_dict[i]['symbol']}) : ")

            if i == 0:
                if len(symbolInput) > 0 and symbolInput != players_dict[i + 1]['symbol']:
                    players_dict[i]['symbol'] = symbolInput.upper()
                    break
                elif len(symbolInput) == 0:
                    break

            else:
                if len(symbolInput) > 0 and symbolInput != players_dict[i - 1]['symbol']:
                    players_dict[i]['symbol'] = symbolInput.upper()
                    break
                elif len(symbolInput) == 0:
                    break

        print(f"\t\t- Your symbol is : {players_dict.get(i)['symbol']}")
        print('')

    # Ask to the player if their are ready to start
    readyInput = input("\tAre you ready to play? Enter Yes or No")

    while readyInput.lower() not in ['yes', 'y', 'ye', '']:
        readyInput = input("\tAre you ready to play? Enter Yes or No")

    return players_dict, True


def display_board(board):
    """
        Display the board, it will look like:
        |  |  |
        |  |  |
        |  |  |
    """
    for i in range(9, 0, -3):
        print('{:^5} | {:^5} | {:^5}'.format(board[i - 2], board[i - 1], board[i]))


def get_diag(data_frame):
    """
        Return the two diagonals of a dataframe
    """

    keys = data_frame.keys()

    diag1 = list()
    diag2 = list()

    if len(keys) == len(data_frame[keys[0]]):
        for i, key in enumerate(keys):
            diag1.append(data_frame.iloc[i][key])
            diag2.append(data_frame.iloc[len(keys) - (i + 1)][key])

    return diag1, diag2


def has_winner(data_frame, iterator, player_symbol):
    """
        Loop through all the rows, cols and diags of the dataframe to find a winner
    """
    result = False
    keys = data_frame.keys()

    if iterator == 'row':
        for i in range(0, len(keys)):
            rowVal = list(set(data_frame.iloc[i]))

            if len(rowVal) == 1 and rowVal[0] == player_symbol:
                result = True

    if iterator == 'col':
        for key in keys:
            colVal = list(set(data_frame.iloc[:][key]))

            if len(colVal) == 1 and colVal[0] == player_symbol:
                result = True

    if iterator == 'diag':
        diag1, diag2 = get_diag(data_frame)
        diag1 = list(set(diag1))
        diag2 = list(set(diag2))

        if len(diag1) == 1 and diag1[0] == player_symbol:
            result = True

        elif len(diag2) == 1 and diag2[0] == player_symbol:
            result = True

    return result


def check_winner(board_list, player_symbol):
    result = False

    # Create a dataframe from the board list
    boardDict = {'col1': list(), 'col2': list(), 'col3': list()}

    for i in range(0, len(board_list) - 1, 3):
        boardDict['col1'].append(board_list[i + 1])
        boardDict['col2'].append(board_list[i + 2])
        boardDict['col3'].append(board_list[i + 3])

    boardDataFrame = pd.DataFrame(boardDict)

    iterators = ['row', 'col', 'diag']

    for item in iterators:
        result = has_winner(data_frame=boardDataFrame, iterator=item, player_symbol=player_symbol)

        if result:
            break

    return result


def play_game(board_list, players_dict):
    print("\n\tGame starts ...")
    print('')

    # Display the board
    display_board(board=board_list)
    print('')

    # Variables initialization
    activePlayer = 0
    gameEnd = False
    i = 0

    while i < len(board_list) - 1 and not gameEnd:
        inputValue = input(f"\t {players_dict[activePlayer]['name']} please choose your position (1-9) : ")

        # Verify that the input is not a space and is a number between 1 and 9
        # Verify that also it has not already been inserted
        incorrectInput = True
        while incorrectInput:
            if inputValue in '123456789' and len(inputValue) == 1:
                if len(board_list[int(inputValue)]) == 0:
                    incorrectInput = False
                else:
                    print("\t\t\t - Sorry, movement not allow")

            if incorrectInput:
                inputValue = input("\t\t - Please choose a value between 1-9 : ")

        # Add the update the value in the boardList and display the updated board
        playerSymbol = players_dict[activePlayer]['symbol']
        board_list[int(inputValue)] = playerSymbol
        print('')
        display_board(board=board_list)

        # Verify if we have a winner
        gameEnd = check_winner(board_list=board_list, player_symbol=playerSymbol)

        # Change the active player
        if not gameEnd:
            activePlayer = 1 if activePlayer == 0 else 0

        i += 1
        print('')

    if gameEnd:
        print(f"{players_dict[activePlayer]['name']} won the game")
    else:
        print('\tWe have a draw')

    print('')


def start_game():
    print('\t****************************************************')
    print(f"\t {' ' * 10} Welcome to Tic Tac Toe!")
    print('\tPlease consider your numpad as the grid for the game')
    print('\t****************************************************')
    print('')

    """
        variables initialization
    """
    playersDict = {0: {'name': 'Player 1', 'symbol': 'X'},
                   1: {'name': 'Player 2', 'symbol': 'O'}}
    boardList = [''] * 10

    """
       game initializations
    """
    playersDict, gameHasStarted = game_init(players_dict=playersDict)

    while gameHasStarted:
        play_game(board_list=boardList, players_dict=playersDict)

        replay = input("Do you want to play again (Yes or No) ? ")

        boardList = [''] * 10

        if replay.lower() not in ['yes', 'ye', 'y']:
            gameHasStarted = False
            print("\nThank for your time, Bye ;-)")


if __name__ == '__main__':
    start_game()
