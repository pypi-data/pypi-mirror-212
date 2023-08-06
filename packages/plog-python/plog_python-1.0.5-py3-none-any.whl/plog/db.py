import os
from sqlmodel import create_engine, SQLModel
from plog.models.log_model import LogModel, ObjectModel



os.makedirs("./data", exist_ok=True)


DATABASE_URL = "sqlite:///data/db.sqlite"

engine = create_engine(DATABASE_URL, echo=True)

SQLModel.metadata.create_all(engine)