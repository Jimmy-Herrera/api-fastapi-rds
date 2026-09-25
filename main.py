from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from database import init_db, get_session
from models import Usuario, UsuarioCreate, Libro, LibroCreate

app = FastAPI(title="API CRUD FastAPI + RDS")

@app.on_event("startup")
def on_startup():
    init_db()

# --- CRUD USUARIOS ---
@app.post("/usuarios/", response_model=Usuario)
def crear_usuario(usuario: UsuarioCreate, session: Session = Depends(get_session)):
    db_user = Usuario.from_orm(usuario)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@app.get("/usuarios/", response_model=List[Usuario])
def listar_usuarios(session: Session = Depends(get_session)):
    return session.exec(select(Usuario)).all()

@app.get("/usuarios/{usuario_id}", response_model=Usuario)
def obtener_usuario(usuario_id: int, session: Session = Depends(get_session)):
    user = session.get(Usuario, usuario_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int, session: Session = Depends(get_session)):
    user = session.get(Usuario, usuario_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    session.delete(user)
    session.commit()
    return {"ok": True, "mensaje": "Usuario eliminado"}

# --- CRUD LIBROS ---
@app.post("/libros/", response_model=Libro)
def crear_libro(libro: LibroCreate, session: Session = Depends(get_session)):
    db_libro = Libro.from_orm(libro)
    session.add(db_libro)
    session.commit()
    session.refresh(db_libro)
    return db_libro

@app.get("/libros/", response_model=List[Libro])
def listar_libros(session: Session = Depends(get_session)):
    return session.exec(select(Libro)).all()