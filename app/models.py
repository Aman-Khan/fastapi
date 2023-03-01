from sqlalchemy import Column, INTEGER, VARCHAR, BOOLEAN, TIMESTAMP, TEXT, ForeignKey, text
from .database import Base, engine

class userCred(Base):
    __tablename__ = 'user_cred'
    email = Column(VARCHAR(100), unique=True, nullable=False)
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    pwd = Column(VARCHAR(100), nullable=False)
    acs = Column(BOOLEAN, nullable=False, server_default=text('0'))
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('NOW()'))

class posts(Base):
    __tablename__ = 'posts'
    pid = Column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
    id = Column(INTEGER, ForeignKey('user_cred.id', ondelete='CASCADE'), nullable=False)
    post = Column(TEXT, nullable=False)
    context = Column(VARCHAR(200), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('NOW()'))

class votes(Base):
    __tablename__ = 'votes'
    pid = Column(INTEGER,  ForeignKey('posts.pid', ondelete='CASCADE'), primary_key=True)
    id = Column(INTEGER,  ForeignKey('user_cred.id', ondelete='CASCADE'), primary_key=True)
    
Base.metadata.create_all(bind=engine)