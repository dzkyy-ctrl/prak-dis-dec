from fastapi import Depends, FastAPI
from sqlalchemy import CHAR, VARCHAR, Column
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Mahasiswa(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nim: str = Field(sa_column=Column(CHAR(8), nullable=False))
    nama: str = Field(sa_column=Column(VARCHAR(50), nullable=False))
    semester: int
    aktif: bool
    ipk: float


engine = create_engine("sqlite:///kampus.db")


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()


@app.get("/mahasiswa/", response_model=list[Mahasiswa])
def read_mahasiswa(session: Session = Depends(get_session)):
    return session.exec(select(Mahasiswa)).all()
