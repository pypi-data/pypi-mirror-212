from typing import List, Optional
from sqlmodel import Session, select
from plog.db import engine
from plog.models.log_model import LogModel, ObjectModel


class LogHandler:
    def create_log(self, log: LogModel) -> LogModel:
        with Session(engine) as session:
            session.add(log)
            session.commit()
            session.refresh(log)
        return log

    def get_log(self, log_id: str) -> Optional[LogModel]:
        with Session(engine) as session:
            statement = select(LogModel).where(LogModel.id == log_id)
            result = session.exec(statement)
            log = result.first()
        return log

    def update_log(self, log: LogModel) -> LogModel:
        with Session(engine) as session:
            session.add(log)
            session.commit()
            session.refresh(log)
        return log

    def delete_log(self, log_id: str) -> bool:
        with Session(engine) as session:
            statement = select(LogModel).where(LogModel.id == log_id)
            result = session.exec(statement)
            log = result.first()
            if log:
                session.delete(log)
                session.commit()
                return True
            return False

    def get_logs_sorted_by_time(
        self, filters: Optional[dict[str, str]] = None
    ) -> List[LogModel]:
        with Session(engine) as session:
            statement = select(LogModel)
            if filters:
                for field, value in filters.items():
                    statement = statement.where(getattr(LogModel, field) == value)
            statement = statement.order_by(LogModel.time)
            logs = session.exec(statement).all()
        return logs