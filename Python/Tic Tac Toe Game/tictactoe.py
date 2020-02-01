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
            name_input = input(
                f"\t{players_dict[i]['name']}, please enter your name (default = {players_dict[i]['name']}) : ")

            if i == 0:
                if len(name_input) > 0 and name_input.capitalize() != players_dict[i + 1]['name']:
                    players_dict[i]['name'] = name_input.capitalize()
                    break
                if len(name_input) == 0:
                    break

            else:
                if len(name_input) > 0 and name_input.capitalize() != players_dict[i - 1]['name']:
                    players_dict[i]['name'] = name_input.capitalize()
                    break
                if len(name_input) == 0:
                    break

        while True:
            symbol_input = input(
                f"\t{players_dict[i]['name']}, please choose your symbol (default = {players_dict[i]['symbol']}) : ")

            if i == 0:
                if len(symbol_input) > 0 and symbol_input.upper() != players_dict[i + 1]['symbol']:
                    players_dict[i]['symbol'] = symbol_input.upper()
                    break
                if len(symbol_input) == 0:
                    break

            else:
                if len(symbol_input) > 0 and symbol_input.upper() != players_dict[i - 1]['symbol']:
                    players_dict[i]['symbol'] = symbol_input.upper()
                    break
                if len(symbol_input) == 0:
                    break

        print(f"\t\t- Your symbol is : {players_dict.get(i)['symbol']}")
        print('')

    # Ask to the player if their are ready to start
    ready_input = input("\tAre you ready to play? Enter Yes or No")

    while ready_input.lower() not in ['yes', 'y', 'ye', '']:
        ready_input = input("\tAre you ready to play? Enter Yes or No")

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
            row_val = list(set(data_frame.iloc[i]))

            if len(row_val) == 1 and row_val[0] == player_symbol:
                result = True

    if iterator == 'col':
        for key in keys:
            col_val = list(set(data_frame.iloc[:][key]))

            if len(col_val) == 1 and col_val[0] == player_symbol:
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
    """
        Create data frame from the list, and loop through each col, row and diag
    """
    result = False

    # Create a dataframe from the board list
    board_dict = {'col1': list(), 'col2': list(), 'col3': list()}

    for i in range(0, len(board_list) - 1, 3):
        board_dict['col1'].append(board_list[i + 1])
        board_dict['col2'].append(board_list[i + 2])
        board_dict['col3'].append(board_list[i + 3])

    board_dataframe = pd.DataFrame(board_dict)

    iterators = ['row', 'col', 'diag']

    for item in iterators:
        result = has_winner(data_frame=board_dataframe, iterator=item, player_symbol=player_symbol)

        if result:
            break

    return result


def play_game(board_list, players_dict):
    """
        Main game function
    """

    print("\n\tGame starts ...")
    print('')

    # Display the board
    display_board(board=board_list)
    print('')

    # Variables initialization
    active_player = 0
    game_end = False
    i = 0

    while i < len(board_list) - 1 and not game_end:
        input_value = input(f"\t {players_dict[active_player]['name']} please choose your position (1-9) : ")

        # Verify that the input is not a space and is a number between 1 and 9
        # Verify that also it has not already been inserted
        incorrect_input = True
        while incorrect_input:
            if input_value in '123456789' and len(input_value) == 1:
                if len(board_list[int(input_value)]) == 0:
                    incorrect_input = False
                else:
                    print("\t\t\t - Sorry, movement not allow")

            if incorrect_input:
                input_value = input("\t\t - Please choose a value between 1-9 : ")

        # Add the update the value in the boardList and display the updated board
        player_symbol = players_dict[active_player]['symbol']
        board_list[int(input_value)] = player_symbol
        print('')
        display_board(board=board_list)

        # Verify if we have a winner
        game_end = check_winner(board_list=board_list, player_symbol=player_symbol)

        # Change the active player
        if not game_end:
            active_player = 1 if active_player == 0 else 0

        i += 1
        print('')

    if game_end:
        print(f"{players_dict[active_player]['name']} won the game")
    else:
        print('\tWe have a draw')

    print('')


def start_game():
    """
        Start and initialize the games variables
    """

    print('\t****************************************************')
    print(f"\t {' ' * 10} Welcome to Tic Tac Toe!")
    print('\tPlease consider your numpad as the grid for the game')
    print('\t****************************************************')
    print('')

    # variables initialization
    players_dict = {0: {'name': 'Player 1', 'symbol': 'X'},
                    1: {'name': 'Player 2', 'symbol': 'O'}}
    board_list = [''] * 10

    # game initializations
    players_dict, game_has_started = game_init(players_dict=players_dict)

    while game_has_started:
        play_game(board_list=board_list, players_dict=players_dict)

        replay = input("Do you want to play again (Yes or No) ? ")

        board_list = [''] * 10

        if replay.lower() not in ['yes', 'ye', 'y']:
            game_has_started = False
            print("\nThank for your time, Bye ;-)")


if __name__ == '__main__':
    start_game()
