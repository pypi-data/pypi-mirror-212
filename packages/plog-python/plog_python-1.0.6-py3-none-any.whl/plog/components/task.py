from typing import List
from plog.models import LogModel
from plog.handlers import LogHandler
from plog.components import ObjectFrame


class Task:
    def __init__(
        self,
        task: str,
        session_id: str = None,
        description: str = None,
        type: str = None,
        data: dict = None,
        objects: List[ObjectFrame] = None,
    ) -> None:
        self.task = task
        self.session_id = session_id
        self.description = description
        self.type = type
        self.data = self.get_data(data)
        self.objects = self.get_objects(objects)

        self.__insert__()
        self.__destroy__()

    def get_data(self, data: dict):
        return str(data)

    def get_objects(self, objects: List[ObjectFrame]):
        return str([str(obj()) for obj in objects])

    def set_handler(self):
        try:
            self.handler = LogHandler()

            return True
        except:
            return False

    def __insert__(self):
        self.set_handler()
        self.handler.create_log(
            LogModel(
                task=self.task,
                session_id=self.session_id,
                description=self.description,
                type=self.type,
                data=self.data,
                objects=self.objects
            )
        )
    
    def __destroy__(self):
        del self
