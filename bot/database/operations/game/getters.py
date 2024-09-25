from datetime import datetime
from typing import Optional

from google.cloud.firestore_v1 import FieldFilter

from bot.database.main import firebase
from bot.database.models.game import Game, GameStatus


async def get_game(game_id: str) -> Optional[Game]:
    game_ref = firebase.db.collection(Game.COLLECTION_NAME).document(game_id)
    game = await game_ref.get()

    if game.exists:
        return Game(**game.to_dict())


async def get_count_of_games(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    status: Optional[GameStatus] = None,
) -> int:
    games_query = firebase.db.collection(Game.COLLECTION_NAME)

    if status:
        games_query = games_query.where(filter=FieldFilter('status', '==', status))
    if start_date:
        games_query = games_query.where(filter=FieldFilter('created_at', '>=', start_date))
    if end_date:
        games_query = games_query.where(filter=FieldFilter('created_at', '<=', end_date))

    games_aggregate_query = await games_query.count().get()

    return int(games_aggregate_query[0][0].value)


async def get_count_of_games_by_user_id(
    user_id: str,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> int:
    games_query = firebase.db.collection(Game.COLLECTION_NAME) \
        .where(filter=FieldFilter('user_id', '==', user_id))

    if start_date:
        games_query = games_query.where(filter=FieldFilter('created_at', '>=', start_date))
    if end_date:
        games_query = games_query.where(filter=FieldFilter('created_at', '<=', end_date))

    games_query = await games_query.count().get()

    return int(games_query[0][0].value)