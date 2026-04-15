"""
Modelo GMUD no banco de dados
"""
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.database import Base


class GMUD(Base):
    """Modelo de Gestão de Manutenção de Equipamentos"""
    
    __tablename__ = "gmuds"
    
    id = Column(Integer, primary_key=True, index=True)
    data = Column(String, nullable=False, index=True)
    equipamento = Column(String, nullable=False, index=True)
    descricao = Column(Text, nullable=True)
    justificativa = Column(Text, nullable=True)
    risco = Column(String, nullable=True)
    status = Column(String, default="AGENDADO", index=True)
    glpi_id = Column(String, nullable=True, unique=True)
    criado_em = Column(DateTime, default=datetime.utcnow, index=True)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<GMUD(id={self.id}, equipamento='{self.equipamento}', status='{self.status}')>"
