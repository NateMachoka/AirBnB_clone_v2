#!/usr/bin/python3

from os import getenv
from models.base_model import BaseModel


if getenv('HBNB_TYPE_STORAGE') == 'db':
    from sqlalchemy import Column, String
    from sqlalchemy.orm import relationship
    from models.base_model import Base

    class State(BaseModel, Base):
        """ State class """

        __tablename__ = 'states'
        name = Column(
            String(length=128),
            nullable=False
        )
        cities = relationship(
            'City',
            cascade='all, delete-orphan',
            backref='state'
        )

else:
    class State(BaseModel):
        """ State class """

        name = ''

        @property
        def cities(self):
            """Gets a list of city instances related to a state"""
            from models import storage
            from models.city import City
            cities = []
            all_cities = storage.all(City)
            for city in all_cities.values():
                if city.state_id == self.id:
                    cities.append(city)
            return cities
