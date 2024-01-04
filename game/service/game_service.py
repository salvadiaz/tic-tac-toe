from __future__ import annotations

from fastapi import HTTPException

from game.dto.bases import GameBase, GameOutput, PlayerBase, MovementBase, SingleGameOutput
from game.model.game import Game
from game.repo.game_repo import GameRepo

EMPTY_BOARD = [[None, None, None], [None, None, None], [None, None, None]]


def check_empty_slot(movement: MovementBase, board: list[list[str | None]]) -> bool:
    return board[movement.row][movement.column] is None


def get_player_symbol(name: str, players: list[PlayerBase]):
    player = [x for x in players if x['name'] in [name]][0]
    if not player:
        raise HTTPException(status_code=400, detail="Invalid player name")
    return player.get("symbol")


def get_next_player(players: list[PlayerBase], actual: str):
    next_player = [x for x in players if x['name'] not in [actual]][0]
    if not next_player:
        raise HTTPException(status_code=400, detail="Invalid player name")
    return next_player.get("name")


def is_current_player_the_winner(symbol: str, board: list[list[str | None]]) -> bool:
    # Three in a row
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == symbol:
            return True
        if board[0][i] == board[1][i] == board[2][i] == symbol:
            return True

    # Diagonals
    if board[0][0] == board[1][1] == board[2][2] == symbol:
        return True

    if board[0][2] == board[1][1] == board[2][0] == symbol:
        return True

    return False


def check_if_movement_is_valid(game: Game, movement: MovementBase):
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    if game.winner is not None:
        raise HTTPException(status_code=400, detail="Game already finished")

    if game.next_turn != movement.player:
        raise HTTPException(status_code=400, detail="Wrong turn")

    if not check_empty_slot(movement, game.board):
        raise HTTPException(status_code=400, detail="Slot is not empty")


class GameService:
    repo: GameRepo = GameRepo()

    def create_game(self, new_game_input: GameBase) -> GameOutput:
        game_data = new_game_input.model_dump()
        [player1, player2] = game_data.get("players")

        p1 = PlayerBase(name=player1["name"],
                        symbol="X" if player1.get("symbol") is None else player1.get("symbol"))

        p2 = PlayerBase(name=player2["name"],
                        symbol="O" if player2.get("symbol") is None else player2.get("symbol"))

        first_player = p1.name \
            if (new_game_input.starting_player is None
                or new_game_input.starting_player not in [p1.name, p2.name]) \
            else new_game_input.starting_player

        game = Game(players=[p1.model_dump(), p2.model_dump()],
                    next_turn=first_player,
                    board=EMPTY_BOARD)

        game = self.repo.save_game(game)
        return GameOutput().from_model(game)

    def make_movement(self, movement: MovementBase):
        game = self.repo.get_game_by_id(movement.game_id)
        check_if_movement_is_valid(game, movement)

        symbol = get_player_symbol(movement.player, game.players)
        game.board[movement.row][movement.column] = symbol
        game.movements_played += 1
        game.next_turn = get_next_player(game.players, movement.player)

        # check if there is a winner
        if is_current_player_the_winner(symbol, game.board):
            game.winner = movement.player

        updated_game = self.repo.save_game(game)
        return GameOutput().from_model(updated_game)

    def get_games(self, finished: bool = None, skip: int = 0, limit: int = None):
        if finished is None:
            games = self.repo.get_all_games()
        else:
            if finished is True:
                games = self.repo.get_finished_games()
            else:
                games = self.repo.get_all_games()

        if limit is not None:
            return games.offset(skip).limit(limit).all()
        return games.offset(skip).all()

    def get_game_by_id(self, game_id):
        game = self.repo.get_game_by_id(game_id)
        if game is None:
            raise HTTPException(status_code=404, detail="Game not found")

        return SingleGameOutput().from_model(game)

    def delete_game(self, game_id):
        game = self.repo.get_game_by_id(game_id)
        if game is None:
            raise HTTPException(status_code=404, detail="Game not found")

        self.repo.delete(game)
