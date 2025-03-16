import asyncio
from sqlalchemy.orm import Session
from app.connection.database import SessionLocal
from app import crud, models
from app.utils.instagram_client import get_instagram_followers
from app.utils.telegram_bot import send_telegram_message


async def monitor_profiles():
    while True:
        db: Session = SessionLocal()
        profiles = db.query(models.Profile).all()
        for profile in profiles:
            followers = get_instagram_followers(profile.instagram_user_id)
            if followers is not None:
                profile.current_follower_count = followers
                db.commit()
                crud.create_follower_history(db, profile.id, followers)
                alerts = crud.get_alerts_for_profile(db, profile.id)
                for alert in alerts:
                    if followers >= alert.milestone and not alert.notified:
                        message = f"{profile.username} has {followers} followers"
                        send_telegram_message(message)
                        alert.notified = 1
                        db.commit()
        db.close()
        await asyncio.sleep(60)
