from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from game.dto.bases import GameBase, MovementBase
from game.service.game_service import GameService

game_router = APIRouter()
game_service = Annotated[GameService, Depends(GameService)]


@game_router.post("/games", status_code=status.HTTP_201_CREATED)
async def create_game(game: GameBase, service: game_service):
    return service.create_game(game)


# according to the input given, it should be a POST method
# but according to the functionality it is a PUT method,
# and it should have the game id in the path, not in the body
@game_router.put("/games", status_code=status.HTTP_200_OK)
async def make_movement(movement: MovementBase, service: game_service):
    return service.make_movement(movement)


@game_router.get("/games", status_code=status.HTTP_200_OK)
async def get_games(finished: bool = None,
                    skip: int = 0, limit: int = None,
                    service: game_service = GameService()):
    return service.get_games(finished, skip, limit)


@game_router.get("/games/{game_id}", status_code=status.HTTP_200_OK)
async def get_game(game_id: int, service: game_service):
    return service.get_game_by_id(game_id)


@game_router.delete("/games/{game_id}", status_code=status.HTTP_200_OK)
async def delete_game(game_id: int, service: game_service):
    return service.delete_game(game_id)
