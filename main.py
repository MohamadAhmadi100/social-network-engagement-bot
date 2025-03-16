from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from app.connection.database import SessionLocal, engine, Base
from app import schemas, crud
from app.config import settings
from app.background_tasks import monitor_profiles
import asyncio

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Social Network Engagement Bot")
security = HTTPBasic()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = settings.basic_auth_username
    correct_password = settings.basic_auth_password
    if not (credentials.username == correct_username and credentials.password == correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="wrong username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(monitor_profiles())


@app.post("/profiles/", response_model=schemas.ProfileOut, dependencies=[Depends(basic_auth)])
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    db_profile = crud.get_profile_by_username(db, profile.username)
    # profile_id = crud.get_profile(db, int(profile.instagram_user_id))
    # print(profile_id)
    if db_profile:
        raise HTTPException(status_code=400, detail="Profile already registered")
    return crud.create_profile(db, profile)


@app.put("/profiles/{profile_id}", response_model=schemas.ProfileOut, dependencies=[Depends(basic_auth)])
def update_profile(profile_id: int, profile_update: schemas.ProfileUpdate, db: Session = Depends(get_db)):
    db_profile = crud.update_profile(db, profile_id, profile_update)
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


@app.get("/profiles/{profile_id}", response_model=schemas.ProfileOut, dependencies=[Depends(basic_auth)])
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    db_profile = crud.get_profile(db, profile_id)
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


@app.post("/alerts/", response_model=schemas.AlertOut, dependencies=[Depends(basic_auth)])
def create_alert(alert: schemas.AlertCreate, db: Session = Depends(get_db)):
    return crud.create_alert(db, alert)


@app.get("/alerts/{profile_id}", response_model=list[schemas.AlertOut], dependencies=[Depends(basic_auth)])
def get_alerts(profile_id: int, db: Session = Depends(get_db)):
    return crud.get_alerts_for_profile(db, profile_id)


@app.get("/follower-history/{profile_id}", response_model=list[schemas.FollowerHistoryOut],
         dependencies=[Depends(basic_auth)])
def get_history(profile_id: int, db: Session = Depends(get_db)):
    return crud.get_follower_history(db, profile_id)


@app.get("/insights/", dependencies=[Depends(basic_auth)])
def get_top_insights(db: Session = Depends(get_db)):
    insights = crud.get_top_follower_insights(db)
    return insights
