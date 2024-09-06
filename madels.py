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
