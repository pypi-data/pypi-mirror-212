from datetime import datetime
from typing import Dict, List, Optional, Union
from uuid import uuid4
from plog.models.log_model import LogModel
from plog.handlers.log_db_handler import LogHandler
from plog.handlers.disk_handler import DiskHandler


def create_log(
    task: str,
    description: str,
    type: str,
    session_id: Optional[str] = None,
    data: str = None,
    files: str = None,
    time: datetime = datetime.now(),
    id: str = str(uuid4())
) -> LogModel:
    log = LogModel(
        id=id,
        task=task,
        description=description,
        type=type,
        session_id=session_id,
        data=data,
        files=files,
        time=time,
    )
    log_handler = LogHandler()
    created_log = log_handler.create_log(log)
    return created_log


def get_log(log_id: str) -> Optional[LogModel]:
    log_handler = LogHandler()
    log = log_handler.get_log(log_id)
    return log


def update_log(log_id: str, **kwargs: Union[str, datetime]) -> Optional[LogModel]:
    log_handler = LogHandler()
    log = log_handler.get_log(log_id)
    if log:
        for field, value in kwargs.items():
            setattr(log, field, value)
        updated_log = log_handler.update_log(log)
        return updated_log
    return None


def delete_log(log_id: str) -> bool:
    log_handler = LogHandler()
    deleted = log_handler.delete_log(log_id)
    return deleted


def get_logs_sorted_by_time(
    filters: Optional[Dict[str, Union[str, datetime]]] = None
) -> List[LogModel]:
    log_handler = LogHandler()
    logs = log_handler.get_logs_sorted_by_time(filters)
    return logs

def upload_metafile(session_id: str, file_bytes: bytes, file_type: str):
    disk_handler = DiskHandler()
    disk_handler.save_file(
        session_id=id,
        file_bytes=file_bytes,
        file_type=file_type
    )
    