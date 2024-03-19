#!/usr/bin/python3
"""New class for SQLAlchemy"""
from os import getenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity

class DBStorage:
    """Create tables in environmental"""
    __engine = None
    __Session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary"""
        session = self.__Session()
        dic = {}
        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
            query = session.query(cls)
            dic = {"{}.{}".format(type(obj).__name__, obj.id): obj for obj in query}
        else:
            classes = [State, City, User, Place, Review, Amenity]
            for cls in classes:
                query = session.query(cls)
                dic.update({"{}.{}".format(type(obj).__name__, obj.id): obj for obj in query})
        session.close()
        return dic

    def new(self, obj):
        """Add a new element in the table"""
        self.__Session.add(obj)

    def save(self):
        """Save changes"""
        self.__Session.commit()

    def delete(self, obj=None):
        """Delete an element in the table"""
        if obj:
            self.__Session.delete(obj)

    def reload(self):
        """Configuration"""
        Base.metadata.create_all(self.__engine)
        self.__Session = sessionmaker(bind=self.__engine)

    def close(self):
        """Closes the current session"""
        if self.__Session:
            self.__Session.close()

