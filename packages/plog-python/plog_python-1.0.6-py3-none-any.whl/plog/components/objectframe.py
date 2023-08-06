import io
from typing import Any
import pandas as pd
from plog.models import ObjectModel
from plog.handlers import ObjectHandler


class ObjectFrame:
    def __init__(self, df: pd.DataFrame, title: str, type: str = ".pkl") -> None:
        self.df = df
        self.model = ObjectModel(title=title, type=type, object=None)

    def build_bytes_from_df(self):
        df_bytes = io.BytesIO()
        self.df.to_pickle(df_bytes)
        df_bytes.seek(0)

        return df_bytes.getvalue()

    def set_handler(self):
        try:
            self.handler = ObjectHandler()

            return True
        except:
            return False

    def __call__(self) -> ObjectModel:
        self.set_handler()
        self.model.object = self.build_bytes_from_df()
        obj = self.handler.create_object(self.model)

        return {"id": obj.id, "title": obj.title, "type": obj.type}
