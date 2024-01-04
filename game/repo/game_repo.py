from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified

from db.database import SessionLocal
from game.model.game import Game


class GameRepo:
    db: Session = SessionLocal()

    def save_game(self, game: Game):
        # flag_modified needs to be specified when a json field is being updated
        flag_modified(game, "board")
        self.db.add(game)
        self.db.commit()
        self.db.refresh(game)

        return game

    def get_game_by_id(self, game_id: int) -> Game:
        return self.db.query(Game).filter(game_id == Game.id).first()

    def get_all_games(self) -> list[Game]:
        return self.db.query(Game)

    def get_finished_games(self):
        return self.db.query(Game).where(Game.winner != None)

    def get_non_finished_games(self):
        return self.db.query(Game).where(Game.winner == None)

    def delete(self, game: Game):
        self.db.delete(game)
        self.db.commit()
