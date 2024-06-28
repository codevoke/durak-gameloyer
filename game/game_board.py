from __future__ import annotations

from functools import reduce
import json

from card import Card


class GameBoard:
    SLOTS_COUNT = 6
    
    def __init__(self):
        self.slots = [None] * self.SLOTS_COUNT

    def add_card(self, card: Card, slot: int) -> bool:
        if self.slots[slot] is None:
            self.slots[slot] = [card]
            return True
        else:
            return False

    def beat_card(self, beat_card: Card, slot: int) -> bool:
        if not self.slots[slot]:
            return False

        if beat_card > self.slots[slot][0]:
            self.slots[slot].append(beat_card)
            return True
        
        return False
    
    def take_all(self) -> list[Card]:
        card_list = reduce(lambda x, y: [*x, *y], self.slots)
        self.slots = []
        return card_list

    def __str__(self) -> str:
        return "<GameBoard 0x%x: %s>" % (
            id(self), 
            "; ".join([
                "[%s]" % ", ".join([str(card) for card in slot_cards])
                for slot_cards in self.slots
            ])
        )

    def serialize(self) -> str:
        return json.dumps(
            [
                [
                    card.serialize() 
                    for card in slot
                ] 
                for slot in self.slots
            ]
        )
    
    @staticmethod
    def deserialize(raw_data) -> GameBoard:
        slots = json.loads(raw_data)
        new_game_board = GameBoard()  
        new_game_board.slots = [
            [
                Card.deserialize(card) 
                for card in slot
            ] 
            for slot in slots
        ]
        return new_game_board
