import uuid
import random

class DeceptionMesh:
    def __init__(self):
        self.active_decoys = []
        self.honeypot_endpoints = ["/api/v1/admin/config", "/api/v1/internal/secrets"]

    def generate_decoy_credential(self, user_context: str):
        decoy = {
            "id": str(uuid.uuid4()),
            "type": "PASSWORD",
            "username": f"adm_{user_context}_{random.randint(100,999)}",
            "password": f"Pass_{uuid.uuid4().hex[:8]}",
            "service": "production-db"
        }
        self.active_decoys.append(decoy)
        return decoy

    def check_honeypot_access(self, endpoint: str, ip: str):
        if endpoint in self.honeypot_endpoints:
            return {
                "triggered": True,
                "threat_type": "HONEYPOT_TOUCH",
                "ip": ip,
                "severity": "HIGH"
            }
        return {"triggered": False}

deception_mesh = DeceptionMesh()
