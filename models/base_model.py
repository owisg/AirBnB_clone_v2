from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
import models

Base = declarative_base()

class BaseModel:
    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        if kwargs:
            self.id = kwargs.pop("id", str(uuid.uuid4()))
            self.created_at = kwargs.pop("created_at", datetime.utcnow())
            self.updated_at = kwargs.pop("updated_at", datetime.utcnow())

            for key, value in kwargs.items():
                if key in {"created_at", "updated_at"}:
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.utcnow()

    def __str__(self):
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

    def __repr__(self):
        return self.__str__()

    def save(self):
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        my_dict = dict(self.__dict__)
        my_dict["__class__"] = type(self).__name__
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()
        my_dict.pop('_sa_instance_state', None)
        return my_dict

    def delete(self):
        models.storage.delete(self)

