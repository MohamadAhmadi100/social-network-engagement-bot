from sqlalchemy.orm import Session
from app import models, schemas


def get_profile(db: Session, profile_id: int):
    return db.query(models.Profile).filter(models.Profile.id == profile_id).first()


def get_profile_by_username(db: Session, username: str):
    return db.query(models.Profile).filter(models.Profile.username == username).first()


def create_profile(db: Session, profile: schemas.ProfileCreate):
    db_profile = models.Profile(username=profile.username, instagram_user_id=profile.instagram_user_id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def update_profile(db: Session, profile_id: int, profile_update: schemas.ProfileUpdate):
    db_profile = get_profile(db, profile_id)
    if not db_profile:
        return None
    if profile_update.username:
        db_profile.username = profile_update.username
    if profile_update.instagram_user_id:
        db_profile.instagram_user_id = profile_update.instagram_user_id
    db.commit()
    db.refresh(db_profile)
    return db_profile


def create_alert(db: Session, alert: schemas.AlertCreate):
    db_alert = models.Alert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert


def get_alerts_for_profile(db: Session, profile_id: int):
    return db.query(models.Alert).filter(models.Alert.profile_id == profile_id).all()


def create_follower_history(db: Session, profile_id: int, count: int):
    db_history = models.FollowerHistory(profile_id=profile_id, count=count)
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history


def get_follower_history(db: Session, profile_id: int):
    return db.query(models.FollowerHistory).filter(models.FollowerHistory.profile_id == profile_id).all()


def get_top_follower_insights(db: Session):
    from datetime import datetime, timedelta
    cutoff = datetime.utcnow() - timedelta(hours=24)
    profiles = db.query(models.Profile).all()
    insights = []
    for profile in profiles:
        history = db.query(models.FollowerHistory).filter(
            models.FollowerHistory.profile_id == profile.id,
            models.FollowerHistory.timestamp >= cutoff
        ).order_by(models.FollowerHistory.timestamp).all()
        if history and len(history) > 1:
            diff = history[-1].count - history[0].count
            insights.append({
                "profile_id": profile.id,
                "username": profile.username,
                "follower_change": diff
            })
    insights.sort(key=lambda x: abs(x["follower_change"]), reverse=True)
    return insights
