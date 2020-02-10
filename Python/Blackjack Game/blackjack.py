from random import shuffle, randint

class Deck:
    """
        Create a deck of card
    """

    __card_symbols = {'club': '♣', 'diamond': '♦', 'heart': '♥', 'spade': '♠'}
    __cards = list()

    def __init__(self, cards=None):
        """ Create a deck """
        if cards is not None:
            if len(cards) == 52:
                Deck.__cards = cards
        else:
            self.__create_card()

    @staticmethod
    def __create_card():
        """ Combine the symbols and the values """
        numbers = list(range(2, 11)) + list(['J', 'Q', 'K', 'A'])
        new_deck = list()

        for symbol in Deck.__card_symbols.values():
            new_deck += list(map(lambda x: f"{x} {symbol}", numbers))

        Deck.__cards = new_deck

    @staticmethod
    def get_cards():
        """ retrieve the deck """
        return Deck.__cards

    @staticmethod
    def shuffle_cards(number):
        """ shuffle the card """
        for i in range(number):
            shuffle(Deck.__cards)

    def combine_deck(self, new_deck):
        """ fuse the deck and return a new one """
        self.__cards += new_deck.get_cards()

        return Deck(cards=self.__cards)

    def __str__(self):
        """ overwrite the default str: Give detail when using print on the class """
        result = ''

        for i in range(0, len(Deck.__cards), 13):
            result += f"{Deck.__cards[i:i + 13]} \n"

        return result

class Players:
    """
        Create a player
    """

    def __init__(self, name, deposit):
        """ Initialize player variables """
        self.__name = name
        self.__deposit = deposit
        self.__total_bet = 0
        self.__hand_list = list()

    def create_hand(self, bet=0):
        """ add a new hand to the hand list """

        hand = Hand(bet=bet)
        # Add hand to the list
        self.__hand_list.append(hand)

        # Update total bet
        self.update_total_bet(bet)

    def delete_hand(self, value):
        """ delete a specific hand from the hand list """
        self.__hand_list.pop(self.__hand_list.index(value))

    def update_total_bet(self, value):
        """ Update total bet """
        self.__total_bet += value

    def update_deposit(self, value):
        """ Update deposit """
        self.__deposit += value

    def split_hand(self, value):
        """ Split hand into two new hand """
        new_hand_list = list()

        for hand in self.__hand_list:
            if hand == value:
                hand_number = hand.get_number()

                # Create a new hand for each card
                for card in hand.get_hand():
                    as_values_list = value.get_as_values()
                    as_value = None

                    if len(as_values_list) > 0:
                        as_value = [as_values_list.pop()]

                    new_hand = Hand(bet=hand.get_bet(), hand=card, as_values=as_value, split=True, number=hand_number)

                    new_hand_list.append(new_hand)

                    # Increase hand number
                    hand_number += 1
            else:
                new_hand_list.append(hand)

        # Update Total Bet
        self.update_total_bet(value=value.get_bet())

        self.__hand_list = new_hand_list

    def empty_hand(self):
        """ Empty the total bet and the hand list """
        self.__total_bet = 0
        self.__hand_list = list()

    def get_name(self):
        """ Return Name """
        return self.__name

    def get_deposit(self):
        """ Return Deposit """
        return self.__deposit

    def get_total_bet(self):
        """ Return Total Bet """
        return self.__total_bet

    def get_hands(self):
        """ Return the list of hand """
        return self.__hand_list

class Hand:
    """
        Create hand
    """

    def __init__(self, bet=0, hand=None, as_values=None, split=False, number=1):
        self.__bet = bet
        self.__hand_result = 0
        self.__has_won = None
        self.__number = number

        self.__hand = None
        if hand is not None:
            self.__hand = (hand,)

        self.__as_values = list()
        if as_values is not None:
            self.__as_values = as_values

        self.__has_been_split = split

    def update_hand(self, value):
        """ Update hand; hand has to be stored as a tuple """
        self.__hand = value

    def update_as_values(self, value):
        """ Update as_values list """
        self.__as_values.append(value)

    def update_bet(self, value):
        """ Update bet """
        self.__bet += value

    def update_has_won(self, value):
        """ Update hand state """
        self.__has_won = value

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

    def get_hand(self):
        """ Return hand """
        return self.__hand

    def get_as_values(self):
        """ Return the list of AS value """
        return self.__as_values

    def get_bet(self):
        """ Return Bet """
        return self.__bet

    def get_hand_result(self):
        """ Return hand result """
        return self.__hand_result

    def get_has_won(self):
        """ Return hand state result """
        return self.__has_won

    def get_has_been_split(self):
        """ Return has_been_split """
        return self.__has_been_split

    def get_number(self):
        """ Return number """
        return self.__number

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
    # Track dealer id
    j = 0

    for i in range(numb_player):
        while True:
            player_name = input(f"\t Player {i + 1}, please enter your name (default = player {i + 1}) : ").capitalize()
            # Verify that the name of the player does not exist
            if len(player_name) > 0:
                if player_name not in list(map(lambda player_: player_.get_name(), player_dict.values())) + ['Dealer']:
                    break
                else:
                    print("\t\t - This name is already used")
            else:
                if len(player_name) == 0:
                    player_name = f"Player {i + 1}"
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

        j = i

    # Create the computer
    player_dict[j + 1] = Players(name='Dealer', deposit=0)

    return player_dict

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
            result = result.combine_deck(new_deck=deck)

        print(f"\t Deck {i + 1} -> {numb} shuffles", end="")

    print('\n')

    return result

def ask_for_bet(players_dict):
    """
       Ask the player to bet
    """

    end_game = False
    new_players_dict = {}
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
                    del players_dict[keys[i]]
                    print(f"\n\t *** {player.get_name()} has left the table ***")
                    break
                elif len(input_result) == 0:
                    # Create a new hand with this bet
                    player.create_hand(bet=10)
                    # Add this player to the new dict of player
                    new_players_dict[count] = player
                    count += 1
                    break
                else:
                    input_result = input("\t\t\t - Please enter a number >= 10 : ")
            else:
                if 10 <= result <= player.get_deposit():
                    # Create a new hand with this bet
                    player.create_hand(bet=result)
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

        j = i
        print('')

    # Add the computer to the new dict
    dealer = players_dict[keys[j + 1]]
    dealer.create_hand()
    new_players_dict[count] = dealer

    if len(players_dict) <= 1:
        end_game = True

    return end_game, new_players_dict

def deal_cards(deck, players_dict, first_deal=True, player_id=None, hand=None):
    """
       Deal the card
    """
    cards = deck.get_cards()

    if first_deal:
        # Deal one card at the time until each players have two
        for i in list(range(len(players_dict))) * 2:
            player = players_dict[i]
            player_hands = player.get_hands()

            # Since it is the first turn each player has only one hand
            # Insert each card to the hand of the player
            hand = player_hands[0]
            hand_result = hand.get_hand()

            if hand_result:
                hand.update_hand(hand_result + (cards.pop(0),))
            else:
                hand.update_hand((cards.pop(0),))
    else:
        if player_id is not None and hand is not None:
            hand.update_hand(hand.get_hand() + (cards.pop(0),))
        else:
            raise TypeError("deal_cards() missing 2 required positional argument: ('player_id', 'hand')")

def update_player_deposit(player, hand, action, reward=0):
    """
        Update player deposit
    """

    if action in ('burst', 'lost'):
        player.update_deposit(value=-hand.get_bet())
    elif action == 'win':
        player.update_deposit(value=reward)

    print(f"\t\t - Your deposit is {player.get_deposit()} \n")

def check_player_state(players_dict, full_check=True, player_id=None):
    """
       Verify a player can still play or if we have a winner
    """

    def check(player_, hand_burst_):
        player_out_ = False
        player_hands = player_.get_hands()

        for hand in player_hands:
            hand_result = hand.get_hand_result()

            if hand_result > 21:
                print(f"\t ### {player_.get_name()} -> Hand {hand.get_number()} burst")
                # Update and display player deposit
                update_player_deposit(player=player_, hand=hand, action='burst')
                # Delete the current hand
                player_.delete_hand(value=hand)
                hand_burst_.append(True)

                if len(player_.get_hands()) <= 0:
                    player_out_ = True

            elif hand_result == 21:
                hand.update_has_won(value=True)

        return player_out_

    player_out = False
    hand_burst = list()

    # Check for all the players
    if full_check:
        # Loop through all the players except the dealer
        for i in range(len(players_dict) - 1):
            player = players_dict[i]
            player_out = check(player_=player, hand_burst_=hand_burst)

            if player_out:
                del players_dict[i]
    else:
        if player_id is not None:
            player = players_dict[player_id]
            player_out = check(player_=player, hand_burst_=hand_burst)

            if player_out:
                del players_dict[player_id]
        else:
            raise TypeError("check_player_state() missing 1 required positional argument: 'player_id'")

    return player_out, hand_burst

def insert_as_value():
    """
       Ask to the player the value of the AS card
    """
    as_value = input("\t\t\t - Please choose a value for your AS card (1 or 11) : ")

    while as_value not in ('1', '11'):
        as_value = input("\t\t\t - Please choose a value for your AS card (1 or 11) : ")

    return int(as_value)

def compute_player_hand_score(player, hand, display_previous_as=False):
    """
        Compute current player hand score
    """

    # Check if the current player hand has a AS card if yes ask for value
    has_as, number = hand.has_as()

    if has_as:
        player_name = player.get_name()

        # Verify the the AS value does not already exist
        as_value_len = len(hand.get_as_values())

        if as_value_len < number:
            if player_name != 'Dealer':
                print(f"\t {player_name} you have a AS card -> Hand {hand.get_number()} -> {hand.get_hand()} : ")
                if display_previous_as:
                    print(f"\t First AS : {hand.get_as_values()}")

            for i in range(as_value_len, number):
                # If it is not the dealer ask for the value of the AS card
                if player_name != 'Dealer':
                    hand.update_as_values(insert_as_value())

                # Find it for the dealer
                else:
                    as_value = hand.get_as_values()

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

    print(f"\t {player.get_name()} : ")

    # Display player hand
    if player.get_name() != 'Dealer':
        print(f"\t\t - Hand {hand.get_number()} : {hand.get_hand()}")
        print(f"\t\t - Value : {hand.get_hand_result()}")
        print(f"\t\t - Hand Bet : {hand.get_bet()}")
        print(f"\t\t - Total Bet : {player.get_total_bet()}")
        print(f"\t\t - Deposit : {player.get_deposit()}")
    # Display dealer hand
    else:
        # Only display one card for the first round
        if first_round:
            print(f"\t\t - Hand : {hand.get_hand()[1]}")
        else:
            print(f"\t\t - Hand : {hand.get_hand()}")
            print(f"\t\t - Value : {hand.get_hand_result()}")

    print('')

def ask_for_move():
    """
       Ask for the player move and return the result
    """

    move_input = input(f"\t\t\t What is your move : \n"
                       f"\t\t\t\t 1 - Hit \n"
                       f"\t\t\t\t 2 - Stand \n"
                       f"\t\t\t\t 3 - Split \n"
                       f"\t\t\t\t 4 - Double Down ? ")

    while move_input not in '1234' or len(move_input) < 1:
        move_input = input("\t\t\t\t\t - Please choose between (1 - 4) : ")

    return move_input

def dealer_turn_play(players_dict, player_id, deck):
    """
       Function that select automatically the dealer' moves
    """
    print("\t\t Dealer Move : ")

    player = players_dict[player_id]

    hand = player.get_hands()[0]
    hand_score = hand.get_hand_result()

    while hand_score < 17:
        print("\t\t\t - Dealer Hit")
        deal_cards(deck=deck, players_dict=players_dict, first_deal=False, player_id=player_id, hand=hand)
        # Compute new score
        compute_player_hand_score(player=player, hand=hand)
        # Display the new hand
        display_hand(player=player, hand=hand)
        # Get new Score
        hand_score = hand.get_hand_result()

    if hand_score <= 21:
        print("\t\t\t - Dealer Stand \n")

def display_result(player, dealer, hand, result, blackjack=False):
    """
        Display the final result
    """

    player_name = player.get_name()
    player_hand = hand.get_hand()
    player_hand_number = hand.get_number()
    player_hand_result = hand.get_hand_result()
    player_bet = hand.get_bet()
    dealer_hand = dealer.get_hands()[0].get_hand()
    dealer_hand_result = dealer.get_hands()[0].get_hand_result()

    if result == 'draw':
        print(f"\n\t {player_name} : *** Round draw ***")
        print(f"\t\t - Hand {player_hand_number} : {player_hand} -> {player_hand_result}")
        print(f"\t\t - Dealer Hand : {dealer_hand} -> {dealer_hand_result}")
        print(f"\t\t - Deposit : {player.get_deposit()} \n")

    elif result == 'win':
        print(f"\n\t {player_name} : *** Round won ***")

        if blackjack:
            print(f"\t\t - Hand {player_hand_number} : {player_hand} -> {player_hand_result} *** Blackjacks ***")
            reward = int((player_bet * 150) / 100)
        else:
            print(f"\t\t - Hand {player_hand_number} : {player_hand} -> {player_hand_result}")
            reward = player_bet

        print(f"\t\t - Dealer Hand : {dealer_hand} -> {dealer_hand_result}")
        print(f"\t\t - Bet : {player_bet} -> Won : {reward}")

        update_player_deposit(player=player, hand=hand, action='win', reward=reward)

    elif result == 'lost':
        print(f"\n\t {player_name} : *** Round lost ***")
        print(f"\t\t - Hand {player_hand_number} : {player_hand} -> {player_hand_result}")
        print(f"\t\t - Dealer Hand : {dealer_hand} -> {dealer_hand_result}")
        print(f"\t\t - Bet : {player_bet} -> Loose : {player_bet}")

        update_player_deposit(player=player, hand=hand, action='lost', reward=player_bet)

def dealer_hand_vs_player_hand(dealer, players_dict):
    """
       Compare the hand of the dealer and player to find winner
    """
    dealer_hand = dealer.get_hands()[0]
    dealer_hand_result = dealer_hand.get_hand_result()

    if dealer_hand_result > 21:
        print("\t\t ### Dealer Burst")

        # Since we have deleted all the players that has been burst we can say that
        # all the player inside players_dict won
        for player in players_dict.values():
            if player.get_name() != 'Dealer':
                player_hands = player.get_hands()

                for hand in player_hands:
                    if hand.has_blackjack():
                        display_result(player=player, dealer=dealer, hand=hand, result='win', blackjack=True)
                    else:
                        display_result(player=player, dealer=dealer, hand=hand, result='win')
    else:
        # Loop through all the players and choose players that hand beat the dealer hand
        for player in players_dict.values():
            if player.get_name() != 'Dealer':
                player_hands = player.get_hands()

                for hand in player_hands:
                    player_hand_result = hand.get_hand_result()

                    if player_hand_result > dealer_hand_result:
                        display_result(player=player, dealer=dealer, hand=hand, result='win')
                    elif player_hand_result == dealer_hand_result:
                        # If player has blackjack and dealer not, player win
                        if hand.has_blackjack() and not dealer_hand.has_blackjack():
                            display_result(player=player, dealer=dealer, hand=hand, result='win', blackjack=True)
                        else:
                            display_result(player=player, dealer=dealer, hand=hand, result='draw')
                    else:
                        display_result(player=player, dealer=dealer, hand=hand, result='lost')

def is_bankrupt(player):
    """
        check if the player has enough found
    """
    result = False

    if player.get_deposit() < 10 and player.get_name() != 'Dealer':
        result = True
        print(f"\n\t Sorry {player.get_name()} you don't have enough money to continue \n")

    return result

def can_double_down(player, hand):
    """
        check if the player can double down and ask for the amount
    """

    result = False
    current_bet = hand.get_bet()
    deposit = player.get_deposit()
    total_bet = player.get_total_bet()
    hand_list = player.get_hands()

    if len(hand_list) == 1 and len(hand.get_hand()) == 2:
        if not hand.get_has_been_split():
            if total_bet + 10 <= deposit:
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
                                hand.update_bet(value=amount)
                                player.update_total_bet(value=amount)
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

def can_split(player, hand):
    """
        check if the player can split its card
    """
    result = False

    if len(hand.get_hand()) == 2:
        if hand.has_double():
            if player.get_total_bet() + hand.get_bet() <= player.get_deposit():
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

def loop_through_player_hands(deck, current_player_dict, i):
    """
        Does through all the current players hands and ask what move
        he will select (hit, stand, doubling down, split)
    """

    player = current_player_dict[i]
    stop = False

    # Loop through all the player hands
    for hand in player.get_hands():
        stop = False
        print('')

        # Check if the player current hand has only one card
        # This one card is the result of splitting
        if len(hand.get_hand()) == 1 and hand.get_has_been_split() is True:
            # Deal one card more
            deal_cards(deck=deck, players_dict=current_player_dict, first_deal=False, player_id=i, hand=hand)

            # Compute the new hand score
            compute_player_hand_score(player=player, hand=hand, display_previous_as=True)

            # Display the new hand
            display_hand(player=player, hand=hand)

            # Check player state
            player_out, hand_burst = check_player_state(players_dict=current_player_dict, full_check=False,
                                                        player_id=i)
            if True in hand_burst or player_out:
                stop = True
        # if the player have more than one car on a split hand it means that hand has already been played
        elif len(hand.get_hand()) > 1 and hand.get_has_been_split() is True:
            stop = True

        while not stop:
            print(f"\t\t\t - Hand {hand.get_number()} {hand.get_hand()} : Value {hand.get_hand_result()}")

            # Ask if the player want to  hit or stand
            move_input = ask_for_move()

            # Hitting
            if int(move_input) == 1:
                # Deal one card more
                deal_cards(deck=deck, players_dict=current_player_dict, first_deal=False, player_id=i, hand=hand)

                # Compute hand score
                compute_player_hand_score(player=player, hand=hand)

                # Display the new hand
                display_hand(player=player, hand=hand)

                # Check player state
                player_out, hand_burst = check_player_state(players_dict=current_player_dict, full_check=False,
                                                            player_id=i)

                if not player_out:
                    stop = loop_through_player_hands(deck=deck, current_player_dict=current_player_dict, i=i)
                else:
                    stop = True

            # Splitting
            elif int(move_input) == 3:
                result = can_split(player=player, hand=hand)

                if result:
                    stop = loop_through_player_hands(deck=deck, current_player_dict=current_player_dict, i=i)

            # Doubling down
            elif int(move_input) == 4:
                result = can_double_down(player=player, hand=hand)

                if result:
                    # Deal one card more
                    deal_cards(deck=deck, players_dict=current_player_dict, first_deal=False, player_id=i, hand=hand)

                    # Compute new bet score
                    compute_player_hand_score(player=player, hand=hand)

                    # Display the hand with the new bet score
                    display_hand(player=player, hand=hand)

                    # First check player state
                    check_player_state(players_dict=current_player_dict, full_check=False, player_id=i)

                    stop = True

            # Standing
            else:
                stop = True
                print("")

    return stop

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
        deal_cards(deck=deck, players_dict=current_player_dict)

        # Display first hands
        for player in current_player_dict.values():
            hand = player.get_hands()[0]
            # Compute player hand score
            compute_player_hand_score(player=player, hand=hand)

            # Display player hands
            display_hand(player=player, hand=hand, first_round=True)

        # First check if we have winner
        check_player_state(players_dict=current_player_dict)

        # Track dealer id
        j = 0

        # Players turn to play
        if len(current_player_dict) > 1:
            # Loop through all the players except the dealer
            for i in range(len(current_player_dict) - 1):
                player = current_player_dict[i]

                # Display this only this the current player haven't won yet
                if not player.get_hands()[0].get_has_won():
                    print(f"\t {player.get_name()} your turn")

                    # loop through each player hand and ask then what move they want
                    loop_through_player_hands(deck=deck, current_player_dict=current_player_dict, i=i)

                j = i

        # Dealer turns
        dealer_id = j + 1
        player = current_player_dict[dealer_id]
        hand = player.get_hands()[0]
        print(f"\t {player.get_name()} your turn \n")

        # Display dealer hand
        display_hand(player=player, hand=hand)

        # Do dealer move only if we still have player left
        if len(current_player_dict) > 1:
            dealer_turn_play(players_dict=current_player_dict, player_id=dealer_id, deck=deck)

            # Compare player and dealer hand and display result
            dealer_hand_vs_player_hand(dealer=player, players_dict=current_player_dict)

        players_dict_copy = players_dict.copy()

        # Check if player has enough money to continue
        for key in players_dict.keys():
            if is_bankrupt(players_dict[key]):
                del players_dict_copy[key]

        players_dict = players_dict_copy

        # Check of the game have enough players to continue
        if len(players_dict) <= 1:
            end_game = True
            print("\t Not enough player to continue")

        # Check if we have enough cards to play again
        # Check if we have enough cards to play again
        # Let assume that each player need at least 3 cards to play
        if len(deck.get_cards()) < len(players_dict) * 3:
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
