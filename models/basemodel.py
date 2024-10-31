#!/usr/bin/python3
""""""
import uuid
from datetime import datetime


class BaseModel:

    def __init__(self, *args, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if key == "id":
                    value = str(uuid.uuid4())
                elif key == "created_at" or "updated_at":
                    value = datetime.now()

        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """"""

        return f"{self.__class__.__name__}: [{self.id}] ({self.created_at}, {self.updated_at})"

    def todict(self):
        """"""

        new_dict = self.__dict__.copy()
        new_dict["id"] = self.id
        new_dict["created_at"] = self.created_at
        new_dict["updated_at"] = self.updated_at
        new_dict["class"] = self.__class__.__name__
        
        return new_dict

if __name__ == '__main__':
    check = BaseModel().todict()
    print(check)
