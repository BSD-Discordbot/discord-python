from db.database import SessionLocal
from sqlalchemy.orm import Session
from db import crud

session = SessionLocal()

def get_db():
    return session
    # db.close()

def get_player(db: Session, player_id: str):
    player = crud.get_player(db, player_id)
    if(player == None):
        player = crud.create_player(db, player_id)
    return player
