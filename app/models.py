from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.connection.database import Base


class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    instagram_user_id = Column(String, unique=True, index=True)
    current_follower_count = Column(Integer, default=0)
    last_checked = Column(DateTime(timezone=True), server_default=func.now())

    alerts = relationship("Alert", back_populates="profile")
    history = relationship("FollowerHistory", back_populates="profile")


class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    milestone = Column(Integer, default=1000)
    notified = Column(Integer, default=0)  # 0: not notified; 1: notified

    profile = relationship("Profile", back_populates="alerts")


class FollowerHistory(Base):
    __tablename__ = "follower_history"
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), index=True)
    count = Column(Integer)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    profile = relationship("Profile", back_populates="history")


Index("ix_follower_history_timestamp", FollowerHistory.timestamp)
