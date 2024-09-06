from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Session_Local, engine
from typing import List
import madels
import schema

madels.Base.metadata.create_all(bind=engine)

app = FastAPI(title='resume API', description='API for resume')


def get_db():
    db = Session_Local()
    try:
        yield db
    finally:
        db.close()


@app.post('/about/', response_model=schema.About)
async def create_about(data: schema.AboutCreate, db: Session = Depends(get_db)):
    info = madels.About(**data.dict())
    db.add(info)
    db.commit()
    db.refresh(info)
    return info


@app.get('/about-get/', response_model=List[schema.About])
async def get_about(db: Session = Depends(get_db)):
    return db.query(madels.About).all()


@app.post('/experience/', response_model=schema.Experience)
async def create_experience(experience: schema.ExperienceCreate, db: Session = Depends(get_db)):
    exp = madels.Experience(**experience.dict())
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp


@app.get('/experience-get/', response_model=List[schema.Experience])
async def get_experience(db: Session = Depends(get_db)):
    return db.query(madels.Experience).all()


@app.post('/education/', response_model=schema.Education)
async def create_education(edu: schema.EducationCreate, db: Session = Depends(get_db)):
    exp = madels.Education(**edu.dict())
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp


@app.get('/education-get/', response_model=List[schema.Education])
async def education_get(db: Session = Depends(get_db)):
    return db.query(madels.Education).all()
