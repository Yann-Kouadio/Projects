from random import shuffle, randint

class Deck:
    """
        Create a deck of card
    """

    __card_symbols = {'club': '♣', 'diamond': '♦', 'heart': '♥', 'spade': '♠'}
    __cards = list()

    # Create a deck of card with the default symbols or the user symbols
    def __init__(self):
        self.__create_card()

    # Function to create the deck
    @staticmethod
    def __create_card():
        numbers = list(range(2, 11)) + list(['J', 'Q', 'K', 'A'])
        new_deck = list()

        for symbol in Deck.__card_symbols.values():
            new_deck += list(map(lambda x: f"{x} {symbol}", numbers))

        Deck.__cards = new_deck

    # Function to retrieve the deck symbol
    @staticmethod
    def get_card_symbol():
        return Deck.__card_symbols

    # Function to retrieve the deck
    @staticmethod
    def get_cards():
        return Deck.__cards

    # shuffle the card
    @staticmethod
    def shuffle_cards():
        for i in range(randint(3,10)):
            shuffle(Deck.__cards)

    # overwrite the default str: Give detail when using print on the class
    def __str__(self):
        result = ''

        for i in range(0, len(Deck.__cards), 13):
            result += f"{Deck.__cards[i:i + 13]} \n"

        return result

class Players:
    """
        Create a player
    """

    # Initialize player variables
    def __init__(self, name, deposit):
        self.__name = name
        self.__deposit = deposit
        self.__hand = None
        self.__hand_result = 0
        self.__bet = 0
        self.__as_value = list()

    # Update player hands
    # hands has to be stored as a tuple
    def update_hand(self, hand):
        self.__hand = hand

    # Update bet
    def update_bet(self, bet):
        self.__bet = bet

    # Update as_value
    def update_as_value(self, as_value):
        self.__as_value.append(as_value)

    # Update deposit
    def update_deposit(self, value):
        self.__deposit += value

    # Remove previous hand a get a new one
    def empty_hand(self):
        self.__hand = list()
        self.__as_value = list()
        self.__hand_result = 0
        self.__bet = 0

    # Compute and return the current score
    def compute_score(self):
        result = 0

        for i, card in enumerate(self.__hand):
            val = card.split()[0]

            if val in 'JQK':
                result += 10

            elif val == 'A':
                if len(self.__as_value) == 1:
                    result += self.__as_value[0]
                else:
                    result += self.__as_value[i]

            else:
                result += int(val)

        self.__hand_result = result

        return self.__hand_result

    # Check if the player has a AS card
    def has_as(self):
        result = [False, 0]

        for card in self.__hand:
            if card.split()[0] == 'A':
                result[0] = True
                result[1] += 1

        return result

    # Get name
    def get_name(self):
        return self.__name

    # Get deposit
    def get_deposit(self):
        return self.__deposit

    # Get hand result
    def get_hand_result(self):
        return self.__hand_result

    # Get bet
    def get_bet(self):
        return self.__bet

    # Get as value
    def get_as_value(self):
        return self.__as_value

    # Get player hands
    def get_hand(self):
        return self.__hand

def players_variables_init():
    """
        Initialize players variables
    """

    # Player creation
    while True:
        try:
            numb_player = int(input("\t How many players will play ? "))
        except ValueError:
            print("\t\t - Please enter a number > 0")
        else:
            if numb_player > 0:
                break

    print('')

    player_dict = {}

    for i in range(numb_player):
        while True:
            player_name = input(f"\t Player {i+1}, please enter your name (default = player {i+1}) : ").capitalize()
            # Verify that the name of the player does not exist
            if len(player_name) > 0:
                if player_name not in list(map(lambda player: player.get_name(), player_dict.values())) + ['Dealer']:
                    break
                else:
                    print("\t\t - This name is already used")
            else:
                if len(player_name) == 0:
                    player_name = f"Player {i+1}"
                    break

        while True:
            try:
                player_deposit = int(input(f"\t {player_name}, please enter your deposit ( >= 50) : "))
            except ValueError:
                print("\t\t - Please enter a number >= 50")
            else:
                if player_deposit < 50:
                    player_deposit = 50

                break

        # Create a new player
        player = Players(name=player_name, deposit=player_deposit)

        # Test the new object
        print(f"\t\t - {player.get_name()}, your deposit is {player.get_deposit()}")
        print("")

        # Add it to the dict player
        player_dict[i] = player

    # Create the computer
    player_dict[i+1] = Players(name='Dealer', deposit=0)

    return player_dict

def deck_variables_init():
    """
        Initialize the deck
    """
    return Deck()

def ask_for_bet(players_dict):
    """
       Ask the player to bet
    """

    end_game = False
    new_players_dict = {}
    count = 0

    # Remove the Dealer and ask all the player
    for i in range(len(players_dict) - 1):
        player = players_dict[i]

        input_result = input(f"\t {player.get_name()}, please enter your bet (min = 10) \n"
                                 f"\t\t - Enter any negative value if you don't want to play this turn \n"
                                 f"\t\t - Enter 'leave' if you want to leave the table \n"
                                 f"\t\t - Enter 'stop' if you want to end the game : ").strip()

        while True:
            try:
                result = int(input_result)
            except (TypeError, ValueError):
                if input_result.lower() == 'stop':
                    end_game = True
                    break
                elif input_result.lower() == 'leave':
                    del players_dict[i]
                    print(f"\n\t *** {player.get_name()} has left the table ***")
                    break
                elif len(input_result) == 0:
                    player.update_bet(10)
                    # Add this player to the new dict of player
                    new_players_dict[count] = player
                    count += 1
                    break
                else:
                    input_result = input("\t\t\t - Please enter a number >= 10 : ")
            else:
                if 10 <= result <= player.get_deposit():
                    player.update_bet(result)
                    # Add this player to the new dict of player
                    new_players_dict[count] = player
                    count += 1
                    break
                elif result > player.get_deposit():
                    input_result = input("\t\t\t - You cannot bet more than your deposit \n"
                                         "\t\t - Please enter a new bet : ")

                elif result < 0:
                    print(f"\n\t *** {player.get_name()} does not play this turn ***")
                    break
                else:
                    input_result = input("\t\t\t - Please enter a number >= 10")

        print('')

    # Add the computer to the new dict
    new_players_dict[count] = players_dict[i+1]

    if len(players_dict) <= 1:
        end_game = True

    return end_game, new_players_dict

def deal_cards(deck, players_dict, first_deal=True, player_id=None):
    """
       Deal the card
    """
    cards = deck.get_cards()

    if first_deal:
        for i in list(range(len(players_dict))) * 2:
            player = players_dict[i]

            if player.get_hand():
                player.update_hand(player.get_hand() + (cards.pop(0),))
            else:
                player.update_hand((cards.pop(0),))
    else:
        if player_id is not None:
            player = players_dict[player_id]
            player.update_hand(player.get_hand() + (cards.pop(0),))
        else:
            raise TypeError("deal_cards() missing 1 required positional argument: 'player_id'")

def update_player_deposit(player, action, reward=0):
    """
        Update player deposit
    """

    if action == 'burst' or action == 'lost':
        player.update_deposit(value=-player.get_bet())
    elif action == 'win':
        player.update_deposit(value=reward)

    print(f"\t\t - Your deposit is {player.get_deposit()} \n")

def check_player_state(players_dict, full_check=True, player_id=None):
    """
       Verify a player can still play or if we have a winner
    """
    def check(player, winner):
        win = burst = False
        hand_result = player.get_hand_result()

        if hand_result > 21:
            print(f"\t ### {player.get_name()} burst")
            update_player_deposit(player=player, action='burst')
            burst = True
        elif hand_result == 21:
            win = True

        if win:
            winner.append(player)

        return win, burst

    winner = burst = False
    winner_list = list()

    # Check for all the players
    if full_check:
        # Loop through all the players except the dealer
        for i in range(len(players_dict) - 1):
            player = players_dict[i]
            winner, burst = check(player=player, winner=winner_list)

            if burst:
                del players_dict[i]
    else:
        if player_id is not None:
            player = players_dict[player_id]
            winner, burst = check(player=player, winner=winner_list)

            if burst:
                del players_dict[player_id]
        else:
            raise TypeError("check_player_state() missing 1 required positional argument: 'player_id'")

    return winner, burst, winner_list

def insert_as_value():
    as_value = input("\t\t\t - Please choose a value for your AS card (1 or 11) : ")

    while as_value != '1' and as_value != '11':
        as_value = input("\t\t\t - Please choose a value for your AS card (1 or 11) : ")

    return int(as_value)

def display_hand(players_dict, full_display=True, player_id=None):
    """
        Display the hand and value of the players
    """

    def display_player_hand(player):
        """
            Display the hand and value of a player
        """

        has_as, number = player.has_as()

        print(f"\t\t - Hand : {player.get_hand()}")

        # Check if the current player has a AS card if yes ask for value
        if has_as:
            # Verify the the AS value does not already exist
            as_value_len = len(player.get_as_value())

            if as_value_len < number:
                for i in range(as_value_len, number):
                    player.update_as_value(insert_as_value())

            computed_score = player.compute_score()
            print(f"\t\t - Value : {computed_score}")
        else:
            computed_score = player.compute_score()
            print(f"\t\t - Value : {computed_score}")

        print(f"\t\t - Bet : {player.get_bet()}")
        print(f"\t\t - Deposit : {player.get_deposit()}")
        print('')

    def display_dealer_hand(player, first_round=True):
        """
            Display the hand and value of the dealer or computer
        """

        if first_round:
            print(f"\t\t - Hand : {player.get_hand()[1]}")
        else:
            print(f"\t\t - Hand : {player.get_hand()}")

            has_as, number = player.has_as()

            if has_as:
                # Verify the the AS value does not already exist
                as_value_len = len(player.get_as_value())

                if as_value_len < number:
                    for i in range(as_value_len, number):
                        as_value = player.get_as_value()

                        if as_value:
                            if 11 + sum(as_value) > 21:
                                player.update_as_value(1)
                            else:
                                player.update_as_value(11)
                        else:
                            player.update_as_value(11)

                computed_score = player.compute_score()
                print(f"\t\t - Value : {computed_score}")
            else:
                computed_score = player.compute_score()
                print(f"\t\t - Value : {computed_score}")

        print('')

    if full_display:
        for player in players_dict.values():
            print(f"\t {player.get_name()} : ")

            # Display the cards and value for the players
            if player.get_name() != 'Dealer':
                display_player_hand(player)
            # Display only one card for the dealer
            else:
                display_dealer_hand(player)

    # Individual display
    else:
        if player_id is not None:
            player = players_dict[player_id]

            if player.get_name() != 'Dealer':
                display_player_hand(player)
            else:
                display_dealer_hand(player, first_round=False)
        else:
            raise TypeError("display_hand() missing 1 required positional argument: 'player_id'")

def ask_for_move(player):
    """
       Ask for the player move and return the result
    """

    print(f"\t {player.get_name()} your turn ")

    move_input = input(f"\t\t What is your move : \n"
                       f"\t\t\t 1 - Hit \n"
                       f"\t\t\t 2 - Stand ? ")

    while move_input not in '12' or len(move_input) < 1:
        move_input = input("\t\t\t - Please choose between 1 or 2 : ")

    return move_input

def dealer_turn_play(players_dict, player_id, deck):
    """
       Function that select automatically the dealer' moves
    """
    print("\t\t Dealer Move : ")

    player = players_dict[player_id]

    hand_score = player.get_hand_result()

    while hand_score < 17:
        print("\t\t\t - Dealer Hit")
        deal_cards(deck=deck, players_dict=players_dict, first_deal=False, player_id=player_id)
        # Display the new hand
        display_hand(players_dict=players_dict, full_display=False, player_id=player_id)
        # Get new Score
        hand_score = player.get_hand_result()

    if hand_score <= 21:
        print("\t\t\t - Dealer Stand \n")

def display_result(player, dealer, result, first_round=False):
    player_name = player.get_name()
    player_hand = player.get_hand()
    player_hand_result = player.get_hand_result()
    player_bet = player.get_bet()
    dealer_hand = dealer.get_hand()
    dealer_hand_result = dealer.get_hand_result()

    if result == 'draw':
        print(f"\n\t {player_name} : *** Round draw ***")
        print(f"\t\t - Hand : {player_hand} -> {player_hand_result}")
        print(f"\t\t - Dealer Hand : {dealer_hand} -> {dealer_hand_result}")
        print(f"\t\t - Deposit : {player.get_deposit()} \n")

    elif result == 'win':
        print(f"\n\t {player_name} : *** Round won ***")

        if first_round:
            print(f"\t\t - Hand : {player_hand} -> {player_hand_result} *** Blackjacks ***")
            reward = int((player_bet * 150) / 100)
        else:
            print(f"\t\t - Hand : {player_hand} -> {player_hand_result}")
            reward = player_bet

        print(f"\t\t - Dealer Hand : {dealer_hand} -> {dealer_hand_result}")
        print(f"\t\t - Bet : {player_bet} -> Won : {reward}")

        update_player_deposit(player=player, action='win', reward=reward)
        # player.update_deposit(value=reward)
        # print(f"\t\t - Deposit : {player.get_deposit()} \n")

    elif result == 'lost':
        print(f"\n\t {player_name} : *** Round lost ***")
        print(f"\t\t - Hand : {player_hand} -> {player_hand_result}")
        print(f"\t\t - Dealer Hand : {dealer_hand} -> {dealer_hand_result}")
        print(f"\t\t - Bet : {player_bet} -> Loose : {player_bet}")

        update_player_deposit(player=player, action='lost', reward=player_bet)

def dealer_hand_vs_player_hand(dealer, players_dict, first_round, winner_list):
    """
       Compare the hand of the dealer and player to find winner
    """
    dealer_hand_result = dealer.get_hand_result()

    if first_round:
        if dealer_hand_result == 21:
            for player in winner_list:
                display_result(player=player, dealer=dealer, result='draw')
        else:
            for player in winner_list:
                display_result(player=player, dealer=dealer, result='win', first_round=True)
    else:
        if dealer_hand_result > 21:
            print("\t\t ### Dealer Burst")

            # Since we have deleted all the players that has been burst we can say that
            # all the player inside players_dict won

            for player in players_dict.values():
                if player.get_name() != 'Dealer':
                    display_result(player=player, dealer=dealer, result='win')
        else:
            # Loop through all the players and choose players that hand beat the dealer hand
            for player in players_dict.values():
                if player.get_name() != 'Dealer':
                    player_hand_result = player.get_hand_result()

                    if player_hand_result > dealer_hand_result:
                        display_result(player=player, dealer=dealer, result='win')
                    elif player_hand_result == dealer_hand_result:
                        display_result(player=player, dealer=dealer, result='draw')
                    else:
                        display_result(player=player, dealer=dealer, result='lost')

def is_bankrupt(player):
    result = False

    if player.get_deposit() < 10 and player.get_name() != 'Dealer':
        result = True
        print(f"\n\t Sorry {player.get_name()} you don't have enough money to continue \n")

    return result

def start_game(deck, players_dict, game_number):
    """
       Start running the game
    """

    print("\t #########################")
    print(f"\t Game {game_number} has started ...")
    print("\t #########################\n")

    first_round = True

    # Ask for bet
    end_game, current_player_dict = ask_for_bet(players_dict=players_dict)

    if not end_game and len(current_player_dict) > 1:
        # Deal the first round
        deal_cards(deck=deck, players_dict=current_player_dict)

        # Display first hands
        display_hand(players_dict=current_player_dict)

        # First check if we have winner
        winner, burst, winner_list = check_player_state(players_dict=current_player_dict)

        if not winner and len(current_player_dict) > 1:
            first_round = False

            # Loop through all the players except the dealer
            for i in range(len(current_player_dict) - 1):
                player = current_player_dict[i]

                while True:
                    # Ask if the player want to  hit or stand
                    move_input = ask_for_move(player=player)

                    if int(move_input) == 1:
                        # Deal one card more
                        deal_cards(deck=deck, players_dict=players_dict, first_deal=False, player_id=i)
                        print('')
                        # Display the new hand
                        display_hand(players_dict=players_dict, full_display=False, player_id=i)
                        # First check player state
                        winner, burst, winner_list = check_player_state(players_dict=current_player_dict, full_check=False, player_id=i)

                        if winner or burst:
                            break
                    else:
                        print("")
                        break

        # Dealer turn
        player = current_player_dict[i+1]
        print(f"\t {player.get_name()} your turn")
        # Display dealer hand
        display_hand(players_dict=current_player_dict, full_display=False, player_id=i+1)

        # Do dealer move only if we don't have winners
        if not first_round:
            dealer_turn_play(players_dict=current_player_dict, player_id=i+1, deck=deck)

        # Compare player and dealer hand and display result
        dealer_hand_vs_player_hand(dealer=player, players_dict=current_player_dict, first_round=first_round,
                                   winner_list=winner_list)

        # Empty players hand and check if player can play again

        players_dict_copy = players_dict.copy()

        for key in players_dict.keys():
            player = players_dict[key]
            player.empty_hand()

            if is_bankrupt(player):
                del players_dict_copy[key]

        players_dict = players_dict_copy

        if len(players_dict) <= 1:
            end_game = True
            print("\t Not enough player to continue")

    return not end_game

def game_init():
    """
        Initialize the game
    """

    print('\t****************************************************')
    print(f"\t {' ' * 5} Welcome to the BlackJack Universe 💖")
    print('\t****************************************************')
    print('')

    # Initialize players variables
    players_dict = players_variables_init()
    next_game = True
    game_number = 1

    while next_game:
        deck = deck_variables_init()
        # Shuffle the deck
        deck.shuffle_cards()

        # start the game
        next_game = start_game(deck=deck, players_dict=players_dict, game_number=game_number)

        game_number += 1

    print("\n\t Game End")
    print("\t Thank for your time, Bye ;-)")


if __name__ == '__main__':
    game_init()
