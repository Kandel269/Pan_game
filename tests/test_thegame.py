import pytest

from source.the_game import *
from source.objects import Card

@pytest.fixture()
def game():
    return TheGame(4)

@pytest.mark.parametrize("new_bot_hand, new_board_hand, expected_result", [ ([],[],set()), ([Card("9C",6,None)],[],set()), ([Card("9C",6,None),Card("9D",6,None),Card("9S",6,None),Card("9H",6,None)],[Card("9H",0,None)],{"6","fok6"}), ([Card("9H",0,None)],[],{"0"}) ])
def test_legal_movements(new_bot_hand,new_board_hand, expected_result):
    game = TheGame(4)
    game.bot_hand = new_bot_hand
    game.board_hand = new_board_hand
    movements = game.legal_movements(game.bot_hand, game.board_hand)
    assert movements == expected_result

@pytest.mark.parametrize("new_bot_hand, expected_value",[ ([],9999), ([Card("9C",6,None),Card("9D",6,None),Card("9S",6,None),Card("9H",6,None)],6), ([Card("XX",2,None),Card("9H",6,None)],4)  ])
def test_power_of_hand_3(new_bot_hand,expected_value):
    game = TheGame(4)
    game.bot_hand = new_bot_hand
    assert game.power_of_hand(game.bot_hand) == expected_value

def test_bot_play_cards(game):
    card = [game.bot_hand[7]]
    game.bot_play_cards(card, game.bot_hand)
    assert len(game.board_hand) == 1
    assert len(game.bot_hand) == 11

def test_bot_pull(game):
    game.bot_pull()
    assert len(game.bot_hand) == 12
    card = game.player_hand.pop(1)
    card_2 = game.player_hand.pop(5)
    game.board_hand.append(card)
    game.board_hand.append(card_2)
    game.bot_pull()
    assert len(game.bot_hand) == 13

def test_init_thegame_(game):
    assert game.max_level == 8
    assert isinstance(game.deck[0], Card)
    assert len(game.deck) == 24

def test_deal_the_cards(game):
    assert len(game.bot_hand) == 12
    assert len(game.player_hand) == 12

    turn = "player"
    for card in game.bot_hand:
        if card.card_name == "9H":
            turn = "bot"

    assert turn == game.turn

def test_new_turn_and_cards_position(game):
    assert game.player_hand[0].lock == False
    assert game.player_hand[0].y == GAME_HEIGHT - CARD_GAME_HEIGHT - 50
    assert game.player_hand[0].x != game.player_hand[1].x
    assert game.player_hand[0].y == game.player_hand[1].y

def test_check_rules_play(game):
    assert game.check_rules_play(game.player_hand) == False

    for i in range(2):
        game.player_hand[i].lock = True
    assert game.check_rules_play(game.player_hand) == False

    game.player_hand[-1].lock = True
    assert game.check_rules_play(game.player_hand) == False

def test_check_rules_pull(game):
    assert game.check_rules_pull() == False

    for i in range(3):
        card = game.player_hand.pop(i)
        game.board_hand.append(card)

    assert game.check_rules_pull() == True
    assert len(game.player_hand) == 11

def test_insert_hand(game):
    new_card = Card("AA",9,None)
    new_card_2 = Card("DD",-2,None)
    game.insert_hand(game.player_hand, new_card)
    game.insert_hand(game.player_hand, new_card_2)
    assert len(game.player_hand) == 14
    assert game.player_hand[-1].card_name == "AA"
    assert game.player_hand[0].card_name == "DD"

def test_fake_play_cards(game):
    card = game.player_hand[0]
    hand, board = game.fake_play_cards(card,game.player_hand,game.board_hand)
    assert len(hand) == 11
    assert len(board) == 1
    assert board[0] == card

def test_fake_pull(game):
    new_card = Card("AA",9,None)
    new_card_2 = Card("DD",-2,None)
    game.board_hand.append(new_card)
    game.board_hand.append(new_card_2)
    hand, board = game.fake_pull(game.player_hand,game.board_hand)
    assert len(hand) == 13
    assert len(board) == 1


