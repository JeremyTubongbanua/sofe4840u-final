from sqlalchemy import Column, Integer, ForeignKey, Table
from .base import Base

# Association table for many-to-many relationship between users (followers)
followers = Table(
    'followers',
    Base.metadata,
    Column('follower_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('followed_id', Integer, ForeignKey('users.id'), primary_key=True)
)
