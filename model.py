from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation
from sqlalchemy.sql import func

Base = declarative_base()

class Organization(Base):
    __tablename__ = "organization"
    id = Column(Integer, primary_key=True)
    name = Column(String(64))

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    FirstName = Column(String(64))
    LastName = Column(String(64))
    NRC = Column(String(64))
    DOB = Column(String(64))
    nationality = Column(String(64))
    location = Column(String(64))
    organization = relation('Organization', backref='user')
    Organization_id = Column(Integer, ForeignKey('organization.id'))

class Client(Base):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True)
    name = Column(String(64))
    location = Column(String(64))
    number_cameras = Column(Integer)
    user = relation('User', backref='client')
    user_id = Column(Integer, ForeignKey('user.id'))
    organization = relation('Organization', backref='client')
    Organization_id = Column(Integer, ForeignKey('organization.id'))

class Cameras(Base):
    __tablename__ = 'camera'
    id = Column(Integer, primary_key=True)
    Location = Column(String(64))
    Model = Column(String(64))
    Date_installed = Column(DateTime, server_default=func.now())
    Client_id = Column(Integer, ForeignKey('client.id'))
    client = relation('Client', backref='camera')