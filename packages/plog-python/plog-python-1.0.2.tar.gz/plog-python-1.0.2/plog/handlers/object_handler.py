from typing import List, Optional
from sqlmodel import Session, select
from plog.db.engine import engine
from plog.models import ObjectModel

class ObjectHandler:
    def create_object(self, obj: ObjectModel) -> ObjectModel:
        with Session(engine) as session:
            session.add(obj)
            session.commit()
            session.refresh(obj)
        return obj

    def get_object(self, obj_id: int) -> Optional[ObjectModel]:
        with Session(engine) as session:
            statement = select(ObjectModel).where(ObjectModel.id == obj_id)
            result = session.exec(statement)
            obj = result.first()
        return obj

    def update_object(self, obj: ObjectModel) -> ObjectModel:
        with Session(engine) as session:
            session.add(obj)
            session.commit()
            session.refresh(obj)
        return obj

    def delete_object(self, obj_id: int) -> bool:
        with Session(engine) as session:
            statement = select(ObjectModel).where(ObjectModel.id == obj_id)
            result = session.exec(statement)
            obj = result.first()
            if obj:
                session.delete(obj)
                session.commit()
                return True
            return False

    def get_objects_by_log_id(self, log_id: int) -> List[ObjectModel]:
        with Session(engine) as session:
            statement = select(ObjectModel).where(ObjectModel.log_id == log_id)
            objects = session.exec(statement).all()
        return objects