import os
import random
import copy

from source.objects import *
from source.tree import *

class TheGame():
    def __init__(self, level):
        self.load_textures()
        self.deck = []

        self.max_level = level * 2

        power_counter = 0
        for symbol in ["9", "10", "J", "Q", "K", "A"]:
            power_counter += 1
            for color in ["C","D","S","H"]:
                if symbol == "9" and color == "H":
                    self.deck.append(Card(f"{symbol}{color}", 0, self.textures[f"{symbol}{color}"]))
                    continue
                self.deck.append(Card(f"{symbol}{color}",power_counter,self.textures[f"{symbol}{color}"]))

        self.player_hand = []
        self.bot_hand = []
        self.board_hand = []

        self.turn = None
        self.deal_the_cards()
        self.new_turn()

    def load_textures(self) -> None:
        current_file = os.path.dirname(__file__)
        texture_folder = os.path.join(current_file, "../img", "img_cards")
        self.textures = {}
        for img in os.listdir(texture_folder):
            texture_path = os.path.join(texture_folder, img)
            texture = pygame.image.load(texture_path)
            texture.set_colorkey((255,255,255))
            self.textures[img.replace(".png","")] = texture

    def deal_the_cards(self) -> None:
        for card in self.deck:
            if random.randint(1, 2) == 1:
                if len(self.player_hand) == 12:
                    self.bot_hand.append(card)
                    continue
                self.player_hand.append(card)
            else:
                if len(self.bot_hand) == 12:
                    self.player_hand.append(card)
                    continue
                self.bot_hand.append(card)

        self.turn = "bot"
        for card in self.player_hand:
            if card.card_name == "9H":
                self.turn = "player"
                break


    def new_turn(self) -> None:
        self.cards_position(self.player_hand, CARD_PLAYER_HEIGHT_POSITION)
        self.cards_position(self.bot_hand, CARD_BOT_HEIGHT_POSITION)
        self.cards_position(self.board_hand, CARD_BOARD_HEIGHT_POSITION)
        for card in self.player_hand:
            card.lock = False

    def cards_position(self, hand, height) -> None:
        len_hand = len(hand)
        position = ((GAME_WIDTH - 300) - CARD_GAME_WIDTH - ((len_hand-1) * OVERLAP)) / 2
        counter_cards = 0
        for card in hand:
            card.x = position + (counter_cards*OVERLAP)
            card.y = height
            counter_cards += 1

    def check_rules_play(self, hand) -> bool:
        cards_locked = []
        for card in hand:
            if card.lock:
                cards_locked.append(card)

        if len(cards_locked) not in [1,3,4]:
            return False

        elif len(cards_locked) == 1:
            if len(self.board_hand) == 0:
                if cards_locked[0].value == 0:
                    index_played_card = hand.index(cards_locked[0])
                    played_card = hand.pop(index_played_card)
                    played_card.lock = False
                    self.board_hand.append(played_card)
                    return True
            elif cards_locked[0].value >= self.board_hand[-1].value:
                index_played_card = hand.index(cards_locked[0])
                played_card = hand.pop(index_played_card)
                played_card.lock = False
                self.board_hand.append(played_card)
                return True
            return False

        else:
            if len(cards_locked) == 3:
                if len(self.board_hand) == 0:
                    return False
                if self.board_hand[-1].value != 0:
                    return False
                for card in cards_locked:
                    if card.value != 1:
                        return False
            else:
                if len(self.board_hand) == 0:
                    value_counter = 0
                    zero_card = None
                    for card in cards_locked:
                        value_counter += card.value
                        if card.value == 0:
                            zero_card = card
                    if value_counter != 3:
                        return False
                    index_played_card = hand.index(zero_card)
                    played_card = hand.pop(index_played_card)
                    played_card.lock = False
                    self.board_hand.append(played_card)
                    cards_locked.remove(zero_card)
                else:
                    value_first_card = None
                    for card in cards_locked:
                        if value_first_card == None:
                            value_first_card = card.value
                            if value_first_card <= self.board_hand[-1].value:
                                return False
                            continue
                        elif value_first_card != card.value:
                            return False

            for card in cards_locked:
                index_played_card = hand.index(card)
                played_card = hand.pop(index_played_card)
                played_card.lock = False
                self.board_hand.append(played_card)
            return True

    def check_rules_pull(self) -> bool:
        if len(self.board_hand) in [0,1]:
            return False
        else:
            how_many_cards = len(self.board_hand) - 1
            max_cards_counter = 3
            for _ in range(how_many_cards):
                if max_cards_counter == 0:
                    return True
                card = self.board_hand.pop(-1)
                self.insert_hand(self.player_hand,card)
                max_cards_counter -= 1
        return True

    def insert_hand(self,hand,new_card) -> None:
        added = False
        for card in hand:
            if new_card.value <= card.value:
                index = hand.index(card)
                hand.insert(index, new_card)
                added = True
                break

        if not added:
            hand.append(new_card)

    """
    fake
    """
    def fake_play_cards(self, cards, hand, board, literable=False) -> (list,list):
        if literable:
            for card in cards:
                index_played_card = hand.index(card)
                played_card = hand.pop(index_played_card)
                board.append(played_card)
            return hand, board
        else:
            index_played_card = hand.index(cards)
            played_card = hand.pop(index_played_card)
            board.append(played_card)
        return hand, board

    def fake_pull(self, hand, board) -> (list,list):
        how_many_cards = len(board) - 1
        max_cards_counter = 3
        for _ in range(how_many_cards):
            if max_cards_counter == 0:
                break
            card = board.pop(-1)
            self.insert_hand(hand,card)
            max_cards_counter -= 1
        return hand, board

    """
    bot mechanics
    """

    def bot_tree(self, level = 0, bot_hand = None, player_hand = None, board_hand = None, data = None) -> None:
        if level == 0:
            bot = copy.copy(self.bot_hand)
            player = copy.copy(self.player_hand)
            board = copy.copy(self.board_hand)
            self.tree = Tree(self.max_level)
            self.root = self.tree.create_node(None, None)
            if not data:
                data = self.root
        else:
            bot = copy.copy(bot_hand)
            player = copy.copy(player_hand)
            board = copy.copy(board_hand)

        """ bot """
        if level % 2 == 0:
            movements = self.legal_movements(bot,board)

            for movement in movements:
                if level == 0:
                    bot = copy.copy(self.bot_hand)
                    player = copy.copy(self.player_hand)
                    board = copy.copy(self.board_hand)

                else:
                    bot = copy.copy(bot_hand)
                    player = copy.copy(player_hand)
                    board = copy.copy(board_hand)

                if movement in ["0","1","2","3","4","5","6"]:
                    for card in bot:
                        if card.value == int(movement):
                            bot, board = self.fake_play_cards(card,bot,board)
                            break

                elif movement == "pull_cards":
                    bot, board = self.fake_pull(bot, board)

                elif movement[0:3] == "fok":
                    cards_to_play = []
                    for card in bot:
                        if card.value == int(movement[-1]):
                            cards_to_play.append(card)
                    bot, board = self.fake_play_cards(cards_to_play, bot, board, True)

                elif movement == "three1":
                    cards_to_play = []
                    for card in bot:
                        if card.value == 1:
                            cards_to_play.append(card)
                    bot, board = self.fake_play_cards(cards_to_play, bot, board, True)

                elif movement == "one_and_three":
                    cards_to_play = []
                    for card in bot:
                        if card.value == 1:
                            cards_to_play.append(card)
                        elif card.value == 0:
                            cards_to_play.insert(0, card)
                    bot, board = self.fake_play_cards(cards_to_play, bot, board, True)


                bot_power = self.power_of_hand(bot)
                player_power = self.power_of_hand(player)
                if bot_power == 9999:
                    player_power = 1
                if player_power == 9999:
                    bot_power = 1
                power = bot_power / player_power
                node = self.tree.create_node(power,data,movement)
                new_node = copy.copy(node)
                self.tree.add_node(node, level)

                if player_power == 9999 or bot_power == 9999:
                    continue
                elif not level == self.max_level - 1:
                    new_level = level + 1
                    self.bot_tree(new_level, bot, player, board, data=new_node)


            """ player """
        else:
            movements = self.legal_movements(player, board)

            for movement in movements:
                bot = copy.copy(bot_hand)
                player = copy.copy(player_hand)
                board = copy.copy(board_hand)

                if movement in ["0", "1", "2", "3", "4", "5", "6"]:
                    for card in player:
                        if card.value == int(movement):
                            player, board = self.fake_play_cards(card, player, board)
                            break

                elif movement == "pull_cards":
                    player, board = self.fake_pull(player, board)

                elif movement[0:3] == "fok":
                    cards_to_play = []
                    for card in player:
                        if card.value == int(movement[-1]):
                            cards_to_play.append(card)
                    player, board = self.fake_play_cards(cards_to_play, player, board, True)

                elif movement == "three1":
                    cards_to_play = []
                    for card in player:
                        if card.value == 1:
                            cards_to_play.append(card)
                    player, board = self.fake_play_cards(cards_to_play, player, board, True)

                elif movement == "one_and_three":
                    cards_to_play = []
                    for card in player:
                        if card.value == 1:
                            cards_to_play.append(card)
                        elif card.value == 0:
                            cards_to_play.insert(0, card)
                    player, board = self.fake_play_cards(cards_to_play, player, board, True)



                bot_power = self.power_of_hand(bot)
                player_power = self.power_of_hand(player)
                if bot_power == 9999:
                    player_power = 1
                if player_power == 9999:
                    bot_power = 1
                power = bot_power / player_power
                node = self.tree.create_node(power,data)
                new_node = copy.copy(node)
                self.tree.add_node(node, level)

                if player_power == 9999 or bot_power == 9999:
                    continue
                elif not level == self.max_level - 1:
                    new_level = level + 1
                    self.bot_tree(new_level, bot, player, board, data=new_node)


    def bot_play_best(self, movement) -> None:
        card_counter = 0
        play_cards = []
        value = None
        if movement in ["0","1","2","3","4","5","6"]:
            card_counter = 1
            value = int(movement)
        elif movement == "pull_cards":
            self.bot_pull()
            return
        elif movement[0:3] == "fok":
            value = int(movement[-1])
            card_counter = 4
        elif movement == "three1":
            value = 1
            card_counter = 3
        elif movement == "one_and_three":
            value = 1
            card_counter = 3
            for card in self.bot_hand:
                if card.value == 0:
                    play_cards.append(card)
                    break

        for card in self.bot_hand:
            if card.value == value:
                play_cards.append(card)
                card_counter -= 1
                if card_counter == 0:
                    break

        self.bot_play_cards(play_cards, self.bot_hand)

    def bot_pull(self) -> None:
        how_many_cards = len(self.board_hand) - 1
        max_cards_counter = 3
        for _ in range(how_many_cards):
            if max_cards_counter == 0:
                break
            card = self.board_hand.pop(-1)
            self.insert_hand(self.bot_hand, card)
            max_cards_counter -= 1

    def bot_play_cards(self, cards, hand) -> None:
        for card in cards:
            index_played_card = hand.index(card)
            played_card = hand.pop(index_played_card)
            self.board_hand.append(played_card)


    def best_bot_move(self) -> str:
        for level in range(self.max_level):
            new_level = (self.max_level - 1) - level
            if new_level % 2 == 0:
                if new_level == 0:
                    self.tree.add_sons(new_level, min, True)
                else:
                    self.tree.add_sons(new_level, min)
            else:
                if new_level == self.max_level - 1:
                    self.tree.add_sons(new_level)
                else:
                    self.tree.add_sons(new_level, max)
        best_power = -100
        best_node = None
        if not isinstance(self.root.list_of_sons[0],Node):
            nodes = self.tree.levels_of_tree[0]
            for node in nodes:
                if (not best_node) and node.bot_move in ["0","1","2","3","4","5","6"]:
                    best_node = node
                elif node.bot_move[0:3] == "fok" or node.bot_move ==  "one_and_three" or node.bot_move == "three1":
                    best_node = node
        else:
            """ Program wysypywał się na końcówkach i takie coś jest potrzebne"""
            for node in self.root.list_of_sons:
                if not isinstance(node, Node):
                    continue
                elif node.power > best_power:
                    best_power = node.power
                    best_node = node

        movement = best_node.bot_move
        return movement

    def legal_movements(self, hand, board) -> set:
        movements = set()
        counter_set_cards = 0
        if len(board) == 0:
            counter_one_value = 0
            counter_zero_value = 0
            for card in hand:
                if card.value == 0:
                    movements.add(str(card.value))
                    counter_zero_value += 1
                elif card.value == 1:
                    counter_one_value += 1

            if counter_zero_value == 1 and counter_one_value == 3:
                movements.add("one_and_three")

        else:
            last_value = -1
            last_board_card = board[-1].value

            for card in hand:
                if card.value < last_board_card:
                    counter_set_cards = 0
                    last_value = card.value
                    continue
                elif card.value == last_value:
                    counter_set_cards += 1
                else:
                    counter_set_cards = 1
                    last_value = card.value
                movements.add(str(card.value))
                if counter_set_cards == 4:
                    movements.add(f"fok{card.value}")  # fok - four of a kind / poker terminology
                if last_value == 1 and counter_set_cards == 3:
                    movements.add(f"three{card.value}")

            if ("0" in movements) and "three1" in movements:
                movements.add("one_and_three")
            if len(board) > 1:
                movements.add("pull_cards")

        return movements

    def power_of_hand(self, hand) -> int:
        if len(hand) == 0:
            return 9999
        power = 0
        for card in hand:
            power += card.value
        average_of_cards = power/len(hand)
        return average_of_cards


