from sqlalchemy import BigInteger, ForeignKey 
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from config import SQLALCHEMY_URL

engine = create_async_engine(SQLALCHEMY_URL, echo = True)


async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id : Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column()


class Subject(Base):
    __tablename__ = 'subjects'
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column()
    items = relationship('Item',back_populates='subject')

class Item(Base):
    __tablename__ = 'items'
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column()
    rule : Mapped[str] = mapped_column()
    subject_id : Mapped[int] = mapped_column(ForeignKey('subjects.id'))
    subject = relationship('Subject', back_populates='items')

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)