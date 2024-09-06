# FastAPI6

FastAPI Tutorial 6 dars

# Serializers va Pydantic Modellar

Bu darsda Pydantic modellar va serializersdan foydalanib, ma'lumotlarni validatsiya qilish va ularni tashqi ko'rinishda
ko'rsatishni o'rganamiz. Shuningdek, kichik bir resume sayt yozamiz, unda foydalanuvchining umumiy ma'lumotlari va
tajribasi kiritiladi.

### Pydantic — bu FastAPI da ma'lumotlarni validatsiya qilish va serialize/deserializatsiya qilish uchun ishlatiladigan asosiy kutubxona. Pydantic modellarini yaratish orqali kiruvchi va chiquvchi ma'lumotlar tuzilishini nazorat qilish mumkin.

* Validation: Kiruvchi ma'lumotlarni Pydantic modeliga muvofiq tekshirish.
* Serialization: Pythondagi obyektlarni JSON formatga aylantirish.
* Deserialization: JSON formatdan Pythondagi obyektlarga aylantirish.

Pydantic Modellar
Pydantic modellar klasslarni ifodalaydi, unda maydonlar turi va default qiymatlari belgilanadi. Ma'lumotlar ushbu
modellar orqali validatsiya qilinadi.


-----------------------------------------------------------------------------------------

# Resume Sayti

Bu misolda, oddiy resume saytini yaratamiz, unda quyidagi ma'lumotlar bo'ladi:

* About - Umumiy ma'lumotlar (ism, biografiya).
* Experience - Ish tajribasi (lavozim, kompaniya, vaqti).
* Education - Ta'lim ma'lumotlari (muassasa nomi, daraja, vaqti).

### Step 1: database.py faylini yaratish

Ma'lumotlar bazasi bilan aloqani o'rnatish uchun database.py faylini yaratamiz.

````python
# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
````

### Step 2: models.py faylini yaratish

models.py faylida SQLAlchemy yordamida ma'lumotlar bazasi modellarini yaratamiz:

```python
# models.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class About(Base):
    __tablename__ = "about"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    bio = Column(Text, index=True)


class Experience(Base):
    __tablename__ = "experience"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String, index=True)
    start_date = Column(String)
    end_date = Column(String)
    about_id = Column(Integer, ForeignKey("about.id"))

    about = relationship("About", back_populates="experiences")


class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)
    institution = Column(String, index=True)
    degree = Column(String, index=True)
    start_date = Column(String)
    end_date = Column(String)
    about_id = Column(Integer, ForeignKey("about.id"))

    about = relationship("About", back_populates="educations")


About.experiences = relationship("Experience", order_by=Experience.id, back_populates="about")
About.educations = relationship("Education", order_by=Education.id, back_populates="about")
```

### Step 2: schemas.py faylini yaratish

schemas.py faylida Pydantic modellarini yaratamiz, ular ma'lumotlarni validatsiya qilish va serialize/deserializatsiya
qilish uchun ishlatiladi.

```python
# schemas.py

from pydantic import BaseModel
from typing import List, Optional


class ExperienceBase(BaseModel):
    title: str
    company: str
    start_date: str
    end_date: str


class ExperienceCreate(ExperienceBase):
    pass


class Experience(ExperienceBase):
    id: int

    class Config:
        orm_mode = True


class EducationBase(BaseModel):
    institution: str
    degree: str
    start_date: str
    end_date: str


class EducationCreate(EducationBase):
    pass


class Education(EducationBase):
    id: int

    class Config:
        orm_mode = True


class AboutBase(BaseModel):
    name: str
    bio: str


class AboutCreate(AboutBase):
    pass


class About(AboutBase):
    id: int
    experiences: List[Experience] = []
    educations: List[Education] = []

    class Config:
        orm_mode = True

```

### Step 4: main.py faylini yaratish

main.py faylida FastAPI ilovasini va CRUD endpointlarini yaratamiz:

```python
# main.py

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal, engine
import models
import schemas

# Ma'lumotlar bazasini yaratish
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CRUD uchun About endpointlari
@app.post("/about/", response_model=schemas.About)
def create_about(about: schemas.AboutCreate, db: Session = Depends(get_db)):
    db_about = models.About(name=about.name, bio=about.bio)
    db.add(db_about)
    db.commit()
    db.refresh(db_about)
    return db_about


@app.get("/about/", response_model=List[schemas.About])
def read_about(db: Session = Depends(get_db)):
    return db.query(models.About).all()


# CRUD uchun Experience endpointlari
@app.post("/experience/", response_model=schemas.Experience)
def create_experience(experience: schemas.ExperienceCreate, db: Session = Depends(get_db)):
    db_experience = models.Experience(
        title=experience.title,
        company=experience.company,
        start_date=experience.start_date,
        end_date=experience.end_date,
        about_id=experience.about_id
    )
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)
    return db_experience


@app.get("/experience/", response_model=List[schemas.Experience])
def read_experience(db: Session = Depends(get_db)):
    return db.query(models.Experience).all()


# CRUD uchun Education endpointlari
@app.post("/education/", response_model=schemas.Education)
def create_education(education: schemas.EducationCreate, db: Session = Depends(get_db)):
    db_education = models.Education(
        institution=education.institution,
        degree=education.degree,
        start_date=education.start_date,
        end_date=education.end_date,
        about_id=education.about_id
    )
    db.add(db_education)
    db.commit()
    db.refresh(db_education)
    return db_education


@app.get("/education/", response_model=List[schemas.Education])
def read_education(db: Session = Depends(get_db)):
    return db.query(models.Education).all()

```

### Tushuntirish

1. Modellar (models.py): About, Experience, va Education modellar ma'lumotlar bazasidagi tegishli jadvallarni
   ifodalaydi. Experience va Education modellari About modeli bilan bog'langan (ForeignKey) va ular relationship()
   yordamida bog'langan.

2. Schemas (schemas.py): Pydantic modellar kiruvchi va chiquvchi ma'lumotlarni validatsiya qilish uchun ishlatiladi.
   Experience, Education, va About uchun alohida schema yaratilgan. orm_mode=True orqali SQLAlchemy ob'ektlari bilan
   moslashuvchan bo'lish uchun ishlatiladi.

3. main.py Fayli: FastAPI ilovasi bu yerda yaratilib, CRUD endpointlar aniqlangan. Har bir endpoint ma'lumotlarni
   yaratish va olish uchun ishlatiladi.

4. Database Configuration (database.py): sqlite ma'lumotlar bazasidan foydalaniladi va SessionLocal orqali sessiyalar
   boshqariladi.

## Xulosa

Bu misolda, Pydantic modellar orqali validatsiya va serializatsiya qanday ishlatilishini ko'rsatdik. Shuningdek, kichik
resume saytni yaratdik, unda foydalanuvchining umumiy ma'lumotlari va tajribasi kiritiladi. Ushbu amaliyot sizga haqiqiy
dunyo loyihalarida FastAPI va Pydanticni samarali foydalanishga yordam beradi.