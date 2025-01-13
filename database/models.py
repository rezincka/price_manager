from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, UniqueConstraint
from sqlalchemy.dialects.sqlite import JSON



class Base(DeclarativeBase):
    ...

class TrackList(Base):
    __tablename__ = 'tracklist'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # primary key is necessary
    user_id: Mapped[int] = mapped_column(Integer,)
    tag: Mapped[str] = mapped_column(String(20), nullable=False)
    src: Mapped[str] = mapped_column(String(40), nullable=False)
    price : Mapped[list[float]] = mapped_column(JSON, nullable=False)

    __table_args__ = (
        UniqueConstraint('user_id', 'tag', name='uix_user_tag'),
    )