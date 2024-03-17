import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import shlex

class FileStorage:
    """This class serializes instances to a JSON file and
    deserializes JSON file to instances
    Attributes:
        __file_path: path to the JSON file
        __objects: objects will be stored
    """
    __file_path = "file.json"
    __classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }
    
    def all(self, cls=None):
        """Returns a dictionary of objects"""
        if cls:
            return {key: obj for key, obj in self.__objects.items() if isinstance(obj, cls)}
        return self.__objects
    
    def new(self, obj):
        """Adds a new object to the storage"""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj
    
    def save(self):
        """Saves the objects to a JSON file"""
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump({key: obj.to_dict() for key, obj in self.__objects.items()}, f)
    
    def reload(self):
        """Loads objects from JSON file"""
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                data = json.load(f)
                self.__objects = {key: self.__classes[obj['__class__']](**obj) for key, obj in data.items()}
        except FileNotFoundError:
            pass
    
    def delete(self, obj=None):
        """Deletes an object from storage"""
        if obj:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            del self.__objects[key]
    
    def close(self):
        """Calls reload to synchronize data"""
        self.reload()

