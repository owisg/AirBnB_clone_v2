import json
import shlex
from models.base_model import BaseModel

class FileStorage:
    """This class serializes instances to a JSON file and
    deserializes JSON file to instances
    Attributes:
        __file_path: path to the JSON file
        __objects: objects will be stored
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """returns a dictionary"""
        if cls:
            return {key: obj for key, obj in self.__objects.items() if type(obj) == cls}
        return self.__objects

    def new(self, obj):
        """sets __object to given obj"""
        if obj:
            key = f"{type(obj).__name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self):
        """serialize the file path to JSON file path"""
        my_dict = {key: obj.to_dict() for key, obj in self.__objects.items()}
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(my_dict, f)

    def reload(self):
        """deserialize the file path to JSON file path"""
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                for key, value in json.load(f).items():
                    value = eval(value["__class__"])(**value)
                    self.__objects[key] = value
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """delete an existing element"""
        if obj:
            key = f"{type(obj).__name__}.{obj.id}"
            del self.__objects[key]

    def close(self):
        """calls reload()"""
        self.reload()

