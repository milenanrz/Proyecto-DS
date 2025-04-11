from sqlalchemy import Column, Float, ForeignKey, Table, String, Integer, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Photographers(Base):
    __tablename__ = "photographers"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    state: Mapped[bool] = mapped_column(Boolean, nullable=False)

class Styles(Base):
    __tablename__ = "photograficStyles"
    id: Mapped[int] = mapped_column(foreign_key=Photographers.id, primary_key=True, autoincrement=True)
    styleName: Mapped[str] = mapped_column(String(20), nullable=False)
