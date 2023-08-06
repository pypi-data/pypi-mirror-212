import os
from sqlmodel import create_engine, SQLModel
from plog.models.log_model import LogModel, ObjectModel



os.makedirs("./plog-data", exist_ok=True)


DATABASE_URL = "sqlite:///plog-data/db.sqlite"

engine = create_engine(DATABASE_URL, echo=False)

SQLModel.metadata.create_all(engine)