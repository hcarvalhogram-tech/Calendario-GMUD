"""
Serviço de integração com GLPI
"""
import requests
import logging
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class GLPIService:
    """Serviço para integração com GLPI"""
    
    def __init__(self):
        self.base_url = settings.GLPI_URL
        self.headers = {
            "App-Token": settings.GLPI_APP_TOKEN,
            "User-Token": settings.GLPI_USER_TOKEN
        }
    
    def criar_chamado(self, equipamento: str, data: str, descricao: str) -> dict:
        """
        Cria um chamado no GLPI
        
        Args:
            equipamento: Nome do equipamento
            data: Data da manutenção
            descricao: Descrição da manutenção
            
        Returns:
            dict com ID do chamado ou None em caso de erro
        """
        if not self.base_url or not self.headers["App-Token"]:
            logger.warning("GLPI não configurado, chamado não será criado")
            return None
        
        payload = {
            "name": f"GMUD - {equipamento} - {data}",
            "content": descricao,
            "type": 1,
            "status": 2
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/apirest.php/Ticket",
                json=payload,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            ticket_id = response.json().get("id")
            logger.info(f"Chamado GLPI criado: {ticket_id}")
            return {"success": True, "glpi_id": ticket_id}
            
        except requests.RequestException as e:
            logger.error(f"Erro ao criar chamado GLPI: {str(e)}")
            return {"success": False, "error": str(e)}
