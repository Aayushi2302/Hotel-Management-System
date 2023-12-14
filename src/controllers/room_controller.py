from config.query import QueryConfig
from models.database import Database

class RoomController:
    def __init__(self, db: Database) -> None:
        self.db = db

    def save_room_details(self, room_data: tuple) -> int | None:
        last_row_id =   self.db.save_data_to_database(
                            QueryConfig.SAVE_ROOM_DATA,
                            room_data
                        )
        return last_row_id

    def get_room_data(self) -> list:
        data =  self.db.fetch_data_from_database(
                    QueryConfig.FETCH_ROOM_DATA
                )
        return data

    