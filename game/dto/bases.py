from __future__ import annotations

from typing import Union

from pydantic import BaseModel, field_validator

from game.model.game import Game


class PlayerBase(BaseModel):
    name: str
    symbol: str

    @field_validator("symbol")
    @classmethod
    def validate_symbol(cls, value: str):
        if value is not None and value not in ["X", "O"]:
            raise ValueError("Symbol must be X or O")
        return value


class GameBase(BaseModel):
    players: list[dict] = []
    starting_player: str = None


class GameOutput(BaseModel):
    game_id: int
    movements_played: int
    next_turn: str
    board: list[list[Union[str, None]]]
    winner: str
    players: list[PlayerBase]

    def from_model(self, game: Game) -> GameOutput:
        self.movements_played = game.movements_played
        self.next_turn = game.next_turn
        self.board = game.board
        self.winner = game.winner
        self.game_id = game.id
        self.players = game.players

        return self


class SingleGameOutput(BaseModel):
    game_id: int = None
    movements_played: int = None
    players: list[PlayerBase] = []

    def from_model(self, game: Game) -> SingleGameOutput:
        self.movements_played = game.movements_played
        self.game_id = game.id
        self.players = game.players

        return self


def validate_field(field: str, value: int):
    if value is None:
        raise ValueError(f"Missing {field}")
    if value < 0 or value > 2:
        raise ValueError(f"{field} value must be between 0 and 2")
    return value


class MovementBase(BaseModel):
    game_id: int
    player: str
    row: int
    column: int

    # @field_validator("id")
    # @classmethod
    # def validate_game_id(cls, value: int):
    #     if not value:
    #         raise ValueError("Must provide game id")
    #     return value
    #
    # @field_validator("player")
    # @classmethod
    # def validate_player(cls, value: str):
    #     if not value:
    #         raise ValueError("Must provide a player")
    #     return value

    @field_validator("row")
    @classmethod
    def validate_row(cls, value: int):
        return validate_field("row", value)


    @field_validator("column")
    @classmethod
    def validate_column(cls, value: int):
        return validate_field("column", value)
