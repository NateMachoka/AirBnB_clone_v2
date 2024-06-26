#!/usr/bin/python3
""" City Module for HBNB project """

from os import getenv
from models.base_model import BaseModel

if getenv('HBNB_TYPE_STORAGE') == 'db':
    from sqlalchemy import Column, String, ForeignKey
    from models.base_model import Base

    class City(BaseModel, Base):
        """ City class """

        __tablename__ = 'cities'
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)

else:
    class City(BaseModel):
        """ City class """

        name = ''
        state_id = ''
