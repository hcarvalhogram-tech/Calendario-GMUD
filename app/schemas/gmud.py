"""
Schemas de validação para GMUD
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class GMUDCreate(BaseModel):
    """Schema para criar nova GMUD"""
    data: str = Field(..., description="Data da manutenção (YYYY-MM-DD)")
    equipamento: str = Field(..., description="Nome do equipamento")
    descricao: str = Field(..., description="Descrição da manutenção")
    justificativa: str = Field(..., description="Justificativa da manutenção")
    risco: str = Field(..., description="Nível de risco (BAIXO, MÉDIO, ALTO)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "data": "2026-04-15",
                "equipamento": "Compressor A",
                "descricao": "Manutenção preventiva do compressor",
                "justificativa": "Manutenção programada regular",
                "risco": "BAIXO"
            }
        }


class GMUDUpdate(BaseModel):
    """Schema para atualizar status da GMUD"""
    status: str = Field(..., description="Novo status (AGENDADO, EM_PROGRESSO, CONCLUIDO, CANCELADO)")


class GMUDResponse(BaseModel):
    """Schema de resposta GMUD"""
    id: int
    data: str
    equipamento: str
    descricao: Optional[str] = None
    justificativa: Optional[str] = None
    risco: Optional[str] = None
    status: str
    glpi_id: Optional[str] = None
    criado_em: datetime
    atualizado_em: datetime
    
    class Config:
        from_attributes = True
