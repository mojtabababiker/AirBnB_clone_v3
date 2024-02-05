#!/usr/bin/python3
"""
Contains the class DBStorage"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB),
                                      pool_pre_ping=True)
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session
        new_dict = {}
        for _class in classes:
            if cls is None or cls is classes[_class] or cls is _class:
                objs = self.__session.query(classes[_class]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        """
        new_dict = {}
        if not cls:
            for _class in classes.values():
                objs = self.__session.query(_class).all()
                for obj in objs:
                    key = _class.__name__ + '.' + obj.id
                    new_dict[key] = obj
        else:
            if type(cls) is str:
                cls = classes.get(cls)
                if not cls:
                    return {}
            try:
                objs = self.__session.query(cls).all()
                for obj in objs:
                    key = cls.__name__ + '.' + obj.id
                    new_dict[key] = obj
            except Exception:
                return {}
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session()

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """A method to retrieve one object from the dataabse with
        the class cls and id id
        """
        try:
            cls_objs = self.all(cls).values()
            for obj in cls_objs:
                if obj.id == id:
                    return obj
            return None
        except Exception as e:
            return None

    def count(self, cls=None):
        """method to count the number of objects in storage
        or instance of the class cls"""
        all_obj = self.all(cls)
        if cls in classes.values():
            all_obj = self.all(cls)
        return len(all_obj)
