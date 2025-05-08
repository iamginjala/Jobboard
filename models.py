from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Jobs(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String(250))
    company: Mapped[str] = mapped_column(String(250))
    location: Mapped[str] = mapped_column(String(250))
    job_url: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    tags: Mapped[str] = mapped_column(String(250))
    posted: Mapped[str] = mapped_column(String(120))


