from pydantic import BaseModel


class Health(BaseModel):
    database_connected: bool
