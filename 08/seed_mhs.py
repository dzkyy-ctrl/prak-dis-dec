from sqlmodel import Session, SQLModel, select

from service_mhs import Mahasiswa, engine

data = [
    Mahasiswa(nim="23000001", nama="Andi Pratama", semester=5, aktif=True, ipk=3.45),
    Mahasiswa(nim="23000002", nama="Budi Santoso", semester=5, aktif=True, ipk=3.20),
    Mahasiswa(nim="23000003", nama="Citra Lestari", semester=3, aktif=True, ipk=3.80),
    Mahasiswa(nim="23000004", nama="Dewi Anggraini", semester=7, aktif=False, ipk=2.95),
    Mahasiswa(nim="23000005", nama="Eko Wibowo", semester=1, aktif=True, ipk=3.60),
]

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    if session.exec(select(Mahasiswa)).first():
        print("Data sudah ada, tidak ditambahkan lagi.")
    else:
        session.add_all(data)
        session.commit()
        print(f"{len(data)} data berhasil ditambahkan.")
