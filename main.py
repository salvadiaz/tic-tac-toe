from fastapi import FastAPI
from db.database import engine, Base
from game.routes.routes import game_router

app = FastAPI()
Base.metadata.create_all(bind=engine)
# game_service = Annotated[GameService, Depends(GameService)]

app.include_router(game_router)

# @app.post("/games", status_code=status.HTTP_201_CREATED)
# async def create_game(game: GameBase, service: game_service):
#     return service.create_game(game)


# according to the input given, it should be a POST method
# but according to the functionality it is a PUT method,
# and it should have the game id in the path, not in the body
# @app.put("/games", status_code=status.HTTP_200_OK)
# async def make_movement(movement: MovementBase, service: game_service):
#     return service.make_movement(movement)
