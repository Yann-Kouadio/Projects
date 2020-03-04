from random import shuffle, randint
from collections import OrderedDict

# Global variables
default_deposit_amount = 50
default_bet_amount = 10
default_bank_name = "Dealer".capitalize()


class Deck:
    """
        Create a deck of card
    """

    __card_symbols = {'club': '♣', 'diamond': '♦', 'heart': '♥', 'spade': '♠'}

    def __init__(self):
        """ Create a deck """
        self.__cards = list()
        self.__create_card()

    def __create_card(self):
        """ Combine the symbols and the values """
        numbers = list(range(2, 11)) + list(['J', 'Q', 'K', 'A'])
        new_deck = list()

        for symbol in Deck.__card_symbols.values():
            new_deck += list(map(lambda value: f"{value} {symbol}", numbers))

        self.__cards = new_deck

    @property
    def cards(self):
        """ retrieve the deck """
        return self.__cards

    def shuffle_cards(self, number):
        """ shuffle the card """
        for i in range(number):
            shuffle(self.__cards)

    def combine_deck(self, new_deck):
        """ fuse the two decks """
        self.__cards += new_deck.cards

    def __str__(self):
        """ overwrite the default str: Give detail when using print on the class """
        result = ''

        for i in range(0, len(self.__cards), 13):
            result += f"{self.__cards[i:i + 13]} \n"

        return result


class Player:
    """
        Create a player
    """

    def __init__(self, name, deposit):
        """ Initialize player variables """
        self.__name = name
        self.__set_deposit(value=deposit)
        self.__set_total_bet(value=0)
        self.__hand_list = list()
        self.__hand_number_list = [1]

    def create_hand(self, bet=0):
        """ add a new hand to the hand list """

        hand = Hand(bet=bet)

        # Add hand to the list
        self.__hand_list.append(hand)

        # Update total bet
        self.__set_total_bet(bet)

    def delete_hand(self, value):
        """ delete a specific hand from the hand list """
        self.__hand_list.pop(self.__hand_list.index(value))

    def __set_total_bet(self, value):
        """ Update total bet """
        self.__total_bet = value

    def __get_total_bet(self):
        """ Return Total Bet """
        return self.__total_bet

    def __set_deposit(self, value):
        """ Update deposit """
        self.__deposit = value

    def __get_deposit(self):
        """ Return Deposit """
        return self.__deposit

    def split_hand(self, value):
        """ Split hand into two new hand """
        new_hand_list = list()

        for hand in self.__hand_list:
            if hand == value:

                hand_number = hand.number

                # Create a new hand for each card
                for card in hand.cards:
                    as_values_list = value.as_values
                    as_value = None

                    if len(as_values_list) > 0:
                        as_value = [as_values_list.pop()]

                    new_hand = Hand(bet=hand.bet, card=card, as_values=as_value, split=True, number=hand_number)

                    new_hand_list.append(new_hand)

                    # Increase hand number
                    if hand_number+1 not in self.__hand_number_list:
                        hand_number += 1
                        self.__hand_number_list.append(hand_number)
                    else:
                        hand_number = self.__hand_number_list[-1]

            else:
                new_hand_list.append(hand)

        # Update Total Bet
        self.__set_total_bet(value=value.bet)

        self.__hand_list = new_hand_list

    def empty_hand(self):
        """ Empty the total bet and the hand list """
        self.__set_total_bet(value=0)
        self.__hand_list = list()
        self.__hand_number_list = [1]

    # Properties
    @property
    def name(self):
        """ Return Name """
        return self.__name

    @property
    def hands(self):
        """ Return a copy of the hand list"""
        return self.__hand_list

    total_bet = property(__get_total_bet, __set_total_bet)
    deposit = property(__get_deposit, __set_deposit)


class Hand:
    """
        Create hand
    """

    def __init__(self, bet=0, card=None, as_values=None, split=False, number=1):
        self.__hand_result = 0
        self.__number = number
        self.__has_been_split = split

        self.__set_hand(value=card)
        self.__set_bet(value=bet)
        self.__set_has_won(value=None)

        self.__as_values = list() if as_values is None else as_values

    def __set_hand(self, value):
        """ Update hand; hand has to be stored as a tuple """

        self.__hand = None

        if value is not None and not isinstance(value, tuple):
            self.__hand = (value,)
        elif isinstance(value, tuple):
            self.__hand = value

    def __get_hand(self):
        """ Return hand """
        return self.__hand

    def __set_bet(self, value):
        """ Update bet """
        self.__bet = value

    def __get_bet(self):
        """ Return Bet """
        return self.__bet

    def __set_has_won(self, value):
        """ Update hand state """
        self.__has_won = value

    def __get_has_won(self):
        """ Return hand state result """
        return self.__has_won

    def update_as_values(self, value):
        """ Update as_values list """
        self.__as_values.append(value)

    def compute_score(self):
        """ Compute and return the current score """
        result = 0
        as_values = self.__as_values.copy()

        for card in self.__hand:
            val = card.split()[0]

            if val in 'JQK':
                result += 10

            elif val == 'A':
                # Pop the first value inside the As list
                result += as_values.pop(0)

            else:
                result += int(val)

        self.__hand_result = result

    def has_as(self):
        """ Check if the hand has a AS card """
        result = [False, 0]

        for card in self.__hand:
            if card.split()[0] == 'A':
                result[0] = True
                result[1] += 1

        return result

    def has_blackjack(self):
        """ Check if the card as a blackjack and """
        result = False

        if len(self.__hand) == 2 and self.__hand_result == 21:
            result = True

        return result

    def has_double(self):
        """ Check if with have the same card twice """
        result = False

        card1, card2 = self.__hand
        if card1.split()[0] == card2.split()[0]:
            result = True

        return result

    # Properties
    @property
    def hand_result(self):
        """ Return hand result """
        return self.__hand_result

    @property
    def number(self):
        """ Return the hand number """
        return self.__number

    @property
    def has_been_split(self):
        """ Return has_been_split """
        return self.__has_been_split

    @property
    def as_values(self):
        """ Return the list of AS value """
        return self.__as_values

    cards = property(__get_hand, __set_hand)
    bet = property(__get_bet, __set_bet)
    has_won = property(__get_has_won, __set_has_won)


def deck_variables_init():
    """
        Initialize the deck
    """
    number = randint(2, 4)
    result = None

    print(f"\t ### We have a combination of {number} decks of cards")
    print(f"\t ### Each deck will be randomly shuffled n (between 4 and 6) times")

    # Create a deck and shuffle it, and append then together
    for i in range(number):
        deck = Deck()
        numb = randint(4, 6)
        deck.shuffle_cards(number=numb)
        if i == 0:
            result = deck
        else:
            result.combine_deck(new_deck=deck)

        print(f"\t Deck {i + 1} -> {numb} shuffles", end="")

    print('\n')

    return result


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

    player_dict = OrderedDict()

    # Track dealer id
    j = 0

    for i in range(numb_player):
        while True:
            player_name = input(f"\t Player {i + 1}, please enter your name (default = player {i + 1}) : ").capitalize()
            # Verify that the name of the player does not exist
            if len(player_name) > 0:
                if player_name not in list(map(lambda player_: player_.name, player_dict.values())) + [default_bank_name]:
                    break
                else:
                    print("\t\t - This name is already used")
            else:
                if len(player_name) == 0:
                    player_name = f"Player {i + 1}"
                    break

        while True:
            player_deposit = input(f"\t {player_name}, please enter your deposit ( >= {default_deposit_amount}) : ")

            try:
                player_deposit = int(player_deposit)
            except ValueError:
                if len(player_deposit) == 0:
                    player_deposit = default_deposit_amount
                    break
                else:
                    print(f"\t\t - Please enter a number >= {default_deposit_amount}")
            else:
                if player_deposit < default_deposit_amount:
                    player_deposit = default_deposit_amount

                break

        # Create a new player
        player = Player(name=player_name, deposit=player_deposit)

        # Test the new object
        print(f"\t\t - {player.name}, your deposit is {player.deposit}")
        print("")

        # Add it to the dict player
        player_dict[i] = player

        j = i

    # Create the computer
    player_dict[j + 1] = Player(name=default_bank_name, deposit=0)

    return player_dict


def ask_for_bet(players_dict):
    """
       Ask the player to bet
    """

    end_game = False
    new_players_dict = OrderedDict()

    # track new dict key
    count = 0

    # Track dealer id
    j = 0

    # Current dict key
    # Use the key to access the dict value to avoid KeyError when a player has been
    # deleted from the game
    keys = list(players_dict.keys())

    # Remove the Dealer and ask all the player
    for i in range(len(keys) - 1):
        player = players_dict[keys[i]]

        input_result = input(f"\t {player.name}, please enter your bet (min = {default_bet_amount}) \n"
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
                    del players_dict[keys[i]]
                    print(f"\n\t *** {player.name} has left the table ***")
                    break
                elif len(input_result) == 0:
                    # Create a new hand with this bet
                    player.create_hand(bet=default_bet_amount)
                    # Add this player to the new dict of player
                    new_players_dict[count] = player
                    count += 1
                    break
                else:
                    input_result = input(f"\t\t\t - Please enter a number >= {default_bet_amount} : ")
            else:
                if default_bet_amount <= result <= player.deposit:
                    # Create a new hand with this bet
                    player.create_hand(bet=result)
                    # Add this player to the new dict of player
                    new_players_dict[count] = player
                    count += 1
                    break
                elif result > player.deposit:
                    input_result = input("\t\t\t - You cannot bet more than your deposit \n"
                                         "\t\t - Please enter a new bet : ")

                elif result < 0:
                    print(f"\n\t *** {player.name} does not play this turn ***")
                    break
                else:
                    input_result = input(f"\t\t\t - Please enter a number >= {default_bet_amount}")

        j = i
        print('')

    # Add the computer to the new dict
    dealer = players_dict[keys[j + 1]]
    dealer.create_hand()
    new_players_dict[count] = dealer

    if len(players_dict) <= 1:
        end_game = True

    return end_game, new_players_dict


def deal_card(deck, hand):
    """
       Deal the card
    """

    # Get th list of cards from the deck class
    cards = deck.cards

    # Get the current player hand cards
    hand_cards = hand.cards

    # Check if hand_cards is not None,
    # Deal another card and combine the two cards to form a hand
    if hand_cards is not None:
        hand.cards = hand_cards + (cards.pop(0),)
    else:
        # Deal the first card
        hand.cards = (cards.pop(0),)


def insert_as_value():
    """
       Ask to the player the value of the AS card
    """
    as_value = input("\t\t\t - Please choose a value for your AS card (1 or 11) : ")

    while as_value not in ('1', '11'):
        as_value = input("\t\t\t - Please choose a value for your AS card (1 or 11) : ")

    return int(as_value)


def compute_player_hand_score(player, hand):
    """
        Compute current player hand score
    """

    # Check if the current player hand has a AS card if yes ask for value
    has_as, number = hand.has_as()

    if has_as:
        player_name = player.name

        # Verify the the AS value does not already exist
        as_value_len = len(hand.as_values)

        if as_value_len < number:
            if player_name != default_bank_name:
                print(f"\t {player_name} you have a AS card -> Hand {hand.number} -> {hand.cards} : ")

                if as_value_len > 0:
                    print(f"\t First AS : {hand.as_values}")

            for i in range(as_value_len, number):
                # If it is not the dealer ask for the value of the AS card
                if player_name != default_bank_name:
                    hand.update_as_values(insert_as_value())

                # Find it for the dealer
                else:
                    as_value = hand.as_values

                    if as_value:
                        if 11 + sum(as_value) > 21:
                            hand.update_as_values(1)
                        else:
                            hand.update_as_values(11)
                    else:
                        hand.update_as_values(11)

        # Compute the total score
        hand.compute_score()

        print('')
    else:
        hand.compute_score()


def display_hand(player, hand, first_round=False):
    """
        Display the current player hand
    """

    print(f"\t {player.name} : ")

    # Display player hand
    if player.name != default_bank_name:
        print(f"\t\t - Hand {hand.number} : {hand.cards}")
        print(f"\t\t - Value : {hand.hand_result}")
        print(f"\t\t - Hand Bet : {hand.bet}")
        print(f"\t\t - Total Bet : {player.total_bet}")
        print(f"\t\t - Deposit : {player.deposit}")

    # Display dealer hand
    else:
        # Only display one card for the first round
        if first_round:
            print(f"\t\t - Hand : ('X', '{hand.cards[1]}')")
        else:
            print(f"\t\t - Hand : {hand.cards}")
            print(f"\t\t - Value : {hand.hand_result}")

    print('')


def update_player_deposit(player, hand, action, reward=0):
    """
        Update player deposit
    """

    if action in ('burst', 'lost'):
        player.deposit -= hand.bet
    elif action == 'win':
        player.deposit += reward

    print(f"\t\t - Your deposit is {player.deposit} \n")


def check_player_hand_state(players_dict, key, player, hand):
    """
       Verify a player can still play or if we have a winner
    """

    player_out = False
    hand_burst = False

    hand_result = hand.hand_result

    if hand_result > 21:
        print(f"\t ### {player.name} -> Hand {hand.number} burst")

        # Update and display player deposit
        update_player_deposit(player=player, hand=hand, action='burst')

        # Delete the current hand
        player.delete_hand(value=hand)
        hand_burst = True

        if len(player.hands) <= 0:
            player_out = True

    elif hand_result == 21:
        hand.has_won = True

    if player_out:
        if players_dict.get(key):
            del players_dict[key]

    return player_out, hand_burst


def ask_for_move():
    """
       Ask for the player move and return the result
    """

    move_input = input(f"\t\t\t What is your move : \n"
                       f"\t\t\t\t 1 - Hit \n"
                       f"\t\t\t\t 2 - Stand \n"
                       f"\t\t\t\t 3 - Split \n"
                       f"\t\t\t\t 4 - Double Down ? ")

    while move_input not in '1234' or len(move_input) != 1:
        move_input = input("\t\t\t\t\t - Please choose between (1 - 4) : ")

    print('')

    return int(move_input)


def can_split(player, hand):
    """
        check if the player can split its card
    """

    result = False

    if len(hand.cards) == 2:

        if hand.has_double():
            if player.total_bet + hand.bet <= player.deposit:
                player.split_hand(value=hand)
                result = True
            else:
                print("\t\t\t\t - Sorry you don't have enough money to split")

        else:
            print("\t\t\t\t - Sorry you cannot split this hand")

    else:
        print("\t\t\t\t - Sorry can only split your initial hand")

    print('')

    return result


def can_double_down(player, hand):
    """
        check if the player can double down and ask for the amount
    """

    result = False
    current_bet = hand.bet
    deposit = player.deposit
    total_bet = player.total_bet
    hand_list = player.hands

    if len(hand_list) == 1 and len(hand.cards) == 2:
        if not hand.has_been_split:
            if total_bet + default_bet_amount <= deposit:
                while True:
                    try:
                        amount = int(input(f"\t\t\t - Please insert an amount up to '{current_bet}' : "))
                    except ValueError:
                        print("\t\t\t\t - Please enter a number")
                    else:
                        if amount == 0:
                            break
                        elif 0 < amount <= current_bet:
                            if amount + total_bet > deposit:
                                print("\t\t\t\t - Sorry you don't have enough money to bet this amount")
                            else:
                                # Update value
                                hand.bet += amount
                                player.total_bet += amount
                                result = True
                                break

                        else:
                            print(f"\t\t\t\t - Please insert an amount up to '{current_bet}'")
            else:
                print("\t\t\t\t - Sorry you don't have enough money to bet")
        else:
            print("\t\t\t\t - Sorry you cannot double a split hand")
    else:
        print("\t\t\t\t - Sorry can only double your initial hand")

    print('')

    return result


def loop_through_player_hands(deck, players_dict, key, player, hand_tracker=0):
    """
        Loop through all the current player hands and ask what move
        he will select (hit, stand, doubling down, split)
    """

    hands = player.hands

    # End the function since the player has no more hands to play
    if hand_tracker >= len(hands):
        return True
    else:
        # Get player current hand
        hand = hands[hand_tracker]

        # Compute current player hand score
        compute_player_hand_score(player=player, hand=hand)

        # Display current player hand
        display_hand(player=player, hand=hand)

        # Check players hand state
        player_out, hand_burst = check_player_hand_state(players_dict=players_dict, player=player, key=key, hand=hand)

        # Check if the player has a valid hand
        if not hand_burst:

            # Ask if the player want to  hit or stand or ...
            move_input = ask_for_move()

            # Hitting
            if move_input == 1:
                # Deal one more card
                deal_card(deck=deck, hand=hand)

                # Ask again for move
                loop_through_player_hands(deck=deck, players_dict=players_dict, key=key, player=player,
                                          hand_tracker=hand_tracker)

            # Splitting
            elif move_input == 3:
                result = can_split(player=player, hand=hand)

                if result:
                    # Get the new hand
                    for hand in player.hands:
                        if len(hand.cards) == 1:
                            # Deal one more care
                            deal_card(deck=deck, hand=hand)

                # Ask again for move
                loop_through_player_hands(deck=deck, players_dict=players_dict, key=key, player=player,
                                          hand_tracker=hand_tracker)

            # Doubling down
            elif int(move_input) == 4:
                result = can_double_down(player=player, hand=hand)

                if result:
                    # Deal one more card
                    deal_card(deck=deck, hand=hand)

                    # Compute new bet score
                    compute_player_hand_score(player=player, hand=hand)

                    # Display the hand with the new bet score
                    display_hand(player=player, hand=hand)

                    # Check players hand state
                    check_player_hand_state(players_dict=players_dict, player=player, key=key, hand=hand)

                    # Got to the next hand
                    loop_through_player_hands(deck=deck, players_dict=players_dict, key=key, player=player,
                                              hand_tracker=hand_tracker+1)

                else:
                    # Ask again for move
                    loop_through_player_hands(deck=deck, players_dict=players_dict, key=key, player=player,
                                              hand_tracker=hand_tracker)

            # Standing
            else:
                # Got to the next hand
                loop_through_player_hands(deck=deck, players_dict=players_dict, key=key, player=player,
                                          hand_tracker=hand_tracker+1)

        else:
            # Check if the player can still play
            if not player_out:
                # Got to the next hand
                loop_through_player_hands(deck=deck, players_dict=players_dict, key=key, player=player,
                                          hand_tracker=hand_tracker+1)


def dealer_turn_to_play(deck, dealer, hand):
    """
       Function that select automatically the dealer' moves
    """
    print(f"\t\t {default_bank_name} Move : ")

    hand_score = hand.hand_result

    while hand_score < 17:
        print(f"\t\t\t - {default_bank_name} Hit \n")

        # Deal one more card
        deal_card(deck=deck, hand=hand)

        # Compute new score
        compute_player_hand_score(player=dealer, hand=hand)

        # Display the new hand
        display_hand(player=dealer, hand=hand)

        # Get new Score
        hand_score = hand.hand_result

    if hand_score <= 21:
        print(f"\t\t\t - {default_bank_name} Stand \n")


def display_result(player, dealer, hand, result):
    """
        Display the final result
    """

    player_name = player.name
    player_hand = hand.cards
    player_hand_number = hand.number
    player_hand_result = hand.hand_result
    player_bet = hand.bet
    dealer_hand = dealer.hands[0].cards
    dealer_hand_result = dealer.hands[0].hand_result

    if result == 'draw':
        print(f"\n\t {player_name} : *** Round draw ***")
        print(f"\t\t - Hand {player_hand_number} : {player_hand} -> {player_hand_result}")
        print(f"\t\t - {default_bank_name} Hand : {dealer_hand} -> {dealer_hand_result}")
        print(f"\t\t - Deposit : {player.deposit} \n")

    elif result == 'win':
        print(f"\n\t {player_name} : *** Round won ***")

        if hand.has_blackjack():
            print(f"\t\t - Hand {player_hand_number} : {player_hand} -> {player_hand_result} *** Blackjacks ***")
            reward = int((player_bet * 150) / 100)
        else:
            print(f"\t\t - Hand {player_hand_number} : {player_hand} -> {player_hand_result}")
            reward = player_bet

        print(f"\t\t - {default_bank_name} Hand : {dealer_hand} -> {dealer_hand_result}")
        print(f"\t\t - Bet : {player_bet} -> Won : {reward}")

        update_player_deposit(player=player, hand=hand, action='win', reward=reward)

    elif result == 'lost':
        print(f"\n\t {player_name} : *** Round lost ***")
        print(f"\t\t - Hand {player_hand_number} : {player_hand} -> {player_hand_result}")
        print(f"\t\t - {default_bank_name} Hand : {dealer_hand} -> {dealer_hand_result}")
        print(f"\t\t - Bet : {player_bet} -> Loose : {player_bet}")

        update_player_deposit(player=player, hand=hand, action='lost', reward=player_bet)


def dealer_hand_vs_player_hand(dealer, dealer_hand, players_dict):
    """
       Compare the dealer and player hand to find the winner
    """
    dealer_hand_result = dealer_hand.hand_result

    if dealer_hand_result > 21:
        print(f"\t\t ### {default_bank_name} Burst")

        # Since we have deleted all the players that have burst we can say that
        # all the players inside players_dict won
        for player in players_dict.values():
            if player.name != default_bank_name:
                player_hands = player.hands

                for hand in player_hands:
                    display_result(player=player, dealer=dealer, hand=hand, result='win')
    else:
        # Loop through all the players and choose players that hand beat the dealer hand
        for player in players_dict.values():
            if player.name != default_bank_name:
                player_hands = player.hands

                for hand in player_hands:
                    player_hand_result = hand.hand_result

                    if player_hand_result > dealer_hand_result:
                        display_result(player=player, dealer=dealer, hand=hand, result='win')

                    elif player_hand_result == dealer_hand_result:
                        # If player has blackjack and dealer not, player win
                        if hand.has_blackjack() and not dealer_hand.has_blackjack():
                            display_result(player=player, dealer=dealer, hand=hand, result='win')
                        else:
                            display_result(player=player, dealer=dealer, hand=hand, result='draw')

                    else:
                        display_result(player=player, dealer=dealer, hand=hand, result='lost')


def is_bankrupt(player):
    """
        check if the player has enough found
    """
    result = False

    if player.deposit < default_bet_amount and player.name != default_bank_name:
        result = True
        print(f"\n\t Sorry {player.name} you don't have enough money to continue \n")

    return result


def start_game(deck, players_dict, game_number):
    """
       Start running the game
    """

    print("\t #########################")
    print(f"\t Game {game_number} has started ...")
    print("\t #########################\n")

    # Ask for bet
    end_game, current_player_dict = ask_for_bet(players_dict=players_dict)

    if not end_game and len(current_player_dict) > 1:

        # Deal the first round
        # Deal one card at the time until each players have two
        for i in list(range(len(current_player_dict))) * 2:
            player = current_player_dict[i]
            # Since it is the first round the players have only one hand
            player_hand = player.hands[0]

            deal_card(deck=deck, hand=player_hand)

        # Create a copy of the dict in order to be able to delete player when
        # their hand has burst
        current_player_dict_copy = current_player_dict.copy()

        # Compute the values and display the hands
        for key, player in current_player_dict_copy.items():

            # print(f"\t {player.name} your turn ... \n")

            # Player turn to play
            if player.name != default_bank_name:
                # Display dealer hand
                dealer = current_player_dict.get(list(current_player_dict.keys())[-1])
                display_hand(player=dealer, hand=dealer.hands[0], first_round=True)

                # Loop through all current player hands
                loop_through_player_hands(deck=deck, players_dict=current_player_dict, key=key, player=player)

            # Dealer turn to play
            else:
                hand = player.hands[0]

                # Compute current dealer hand score
                compute_player_hand_score(player=player, hand=hand)

                # Display dealer hand
                display_hand(player=player, hand=hand)

                # Do dealer move only if we still have player left
                if len(current_player_dict) > 1:
                    dealer_turn_to_play(deck=deck, dealer=player, hand=hand)

                # Compare player and dealer hand and display result
                dealer_hand_vs_player_hand(dealer=player, dealer_hand=hand, players_dict=current_player_dict)

        # Check if player has enough money to continue
        for key in current_player_dict_copy.keys():
            if is_bankrupt(current_player_dict_copy[key]):
                if players_dict.get(key):
                    del players_dict[key]

        # Check if the game has enough players to continue
        if len(players_dict) <= 1:
            end_game = True
            print("\t Not enough player to continue")

        # Check if we have enough cards to play again
        # Let assume that each player need at least 3 cards to play
        if len(deck.cards) < len(players_dict) * 3:
            end_game = True
            print("\t Not enough cards to continue")

    # Empty player hand
    for key in players_dict.keys():
        players_dict[key].empty_hand()

    return not end_game, players_dict


def game_init():
    """
        Initialize the game
    """

    print('\t****************************************************')
    print(f"\t {' ' * 5} Welcome to the BlackJack Universe 💖")
    print('\t****************************************************')
    print('')

    # Initialize deck
    deck = deck_variables_init()

    # Initialize players variables
    players_dict = players_variables_init()
    next_game = True
    game_number = 1

    while next_game:
        # start the game
        next_game, players_dict = start_game(deck=deck, players_dict=players_dict, game_number=game_number)
        game_number += 1

    print("\n\t Game End")
    print("\t Thank for your time, Bye ;-)")


if __name__ == '__main__':
    game_init()
