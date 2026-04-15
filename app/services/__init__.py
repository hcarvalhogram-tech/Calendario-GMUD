"""Serviços da aplicação"""
from .glpi import GLPIService
from .document import GMUDDocumentService

__all__ = ["GLPIService", "GMUDDocumentService"]
