# main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime, timedelta
from pydantic import BaseModel
import requests
import zipfile
import io
from docx import Document
import os

# Database
DATABASE_URL = "sqlite:///./gmuds.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Models
class GMUD(Base):
    __tablename__ = "gmuds"
    id = Column(Integer, primary_key=True)
    data = Column(String)
    equipamento = Column(String)
    status = Column(String, default="AGENDADO")
    glpi_id = Column(String, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# Schemas
class GMUDCreate(BaseModel):
    data: str
    equipamento: str
    descricao: str
    justificativa: str
    risco: str

class GMUDUpdate(BaseModel):
    status: str

# FastAPI
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# GLPI Config
GLPI_URL = os.getenv("GLPI_URL", "http://localhost/glpi")
GLPI_APP_TOKEN = os.getenv("GLPI_APP_TOKEN", "")
GLPI_USER_TOKEN = os.getenv("GLPI_USER_TOKEN", "")

def criar_chamado_glpi(data, equipamento):
    headers = {"App-Token": GLPI_APP_TOKEN, "User-Token": GLPI_USER_TOKEN}
    payload = {
        "name": f"GMUD - {equipamento} - {data}",
        "content": f"Manutenção programada para {equipamento}",
        "type": 1,
        "status": 2
    }
    try:
        response = requests.post(f"{GLPI_URL}/apirest.php/Ticket", json=payload, headers=headers)
        return response.json().get("id")
    except:
        return None

@app.post("/agendar")
def agendar_gmud(gmud: GMUDCreate, db: Session = SessionLocal()):
    existe = db.query(GMUD).filter(GMUD.data == gmud.data, GMUD.equipamento == gmud.equipamento).first()
    if existe:
        raise HTTPException(status_code=400, detail="GMUD já existe para este equipamento nesta data")
    
    glpi_id = criar_chamado_glpi(gmud.data, gmud.equipamento)
    novo = GMUD(data=gmud.data, equipamento=gmud.equipamento, glpi_id=glpi_id)
    db.add(novo)
    db.commit()
    return {"id": novo.id, "glpi_id": glpi_id}

@app.get("/gmuds")
def listar_gmuds(db: Session = SessionLocal()):
    return db.query(GMUD).all()

@app.put("/gmuds/{gmud_id}")
def atualizar_gmud(gmud_id: int, update: GMUDUpdate, db: Session = SessionLocal()):
    gmud = db.query(GMUD).filter(GMUD.id == gmud_id).first()
    if not gmud:
        raise HTTPException(status_code=404)
    gmud.status = update.status
    db.commit()
    return gmud

@app.delete("/gmuds/{gmud_id}")
def deletar_gmud(gmud_id: int, db: Session = SessionLocal()):
    gmud = db.query(GMUD).filter(GMUD.id == gmud_id).first()
    if not gmud:
        raise HTTPException(status_code=404)
    db.delete(gmud)
    db.commit()
    return {"deleted": True}

@app.post("/gerar")
def gerar_gmud(ids: list, db: Session = SessionLocal()):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for gmud_id in ids:
            gmud = db.query(GMUD).filter(GMUD.id == gmud_id).first()
            if gmud:
                doc = Document("GMUD_PADRAO.docx")
                for paragraph in doc.paragraphs:
                    if "{{DATA}}" in paragraph.text:
                        paragraph.text = paragraph.text.replace("{{DATA}}", gmud.data)
                    if "{{EQUIPAMENTO}}" in paragraph.text:
                        paragraph.text = paragraph.text.replace("{{EQUIPAMENTO}}", gmud.equipamento)
                
                buffer = io.BytesIO()
                doc.save(buffer)
                zip_file.writestr(f"GMUD_{gmud.id}.docx", buffer.getvalue())
    
    zip_buffer.seek(0)
    return FileResponse(zip_buffer, filename="gmuds.zip")

@app.get("/dashboard")
def dashboard(db: Session = SessionLocal()):
    total = db.query(GMUD).count()
    concluidas = db.query(GMUD).filter(GMUD.status == "CONCLUIDO").count()
    pendentes = total - concluidas
    return {
        "total": total,
        "concluidas": concluidas,
        "pendentes": pendentes,
        "taxa": (concluidas / total * 100) if total > 0 else 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)