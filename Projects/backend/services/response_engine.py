from typing import Dict
import logging

class ResponseEngine:
    def __init__(self, mode: str = "B"): # Default to Analyst Approval
        self.mode = mode
        self.actions = {
            "DISABLE_ACCOUNT": self._disable_account,
            "ISOLATE_CONTAINER": self._isolate_container,
            "DEPLOY_DECOY": self._deploy_decoy,
            "APPLY_FIREWALL": self._apply_firewall
        }

    def set_mode(self, mode: str):
        if mode in ["A", "B"]:
            self.mode = mode

    async def execute_mitigation(self, threat_data: Dict):
        recommendation = threat_data.get("mitigation")
        risk_score = threat_data.get("risk_score", 0)
        
        print(f"Executing mitigation logic for {threat_data.get('threat_category')}")
        
        if self.mode == "A" or (self.mode == "B" and risk_score > 90):
            # Automated execution for high risk or Mode A
            action = self._map_mitigation_to_action(recommendation)
            if action:
                return await self.actions[action](threat_data)
        
        return {"status": "PENDING_APPROVAL", "message": "Manual review required for risk score < 90"}

    def _map_mitigation_to_action(self, recommendation: str):
        if "Block User" in recommendation or "Revoke" in recommendation:
            return "DISABLE_ACCOUNT"
        if "Isolate" in recommendation:
            return "ISOLATE_CONTAINER"
        if "Sanitize" in recommendation:
            return "APPLY_FIREWALL"
        return "DEPLOY_DECOY"

    async def _disable_account(self, data):
        print(f"ACTION: Disabling account {data.get('actor')}")
        return {"status": "SUCCESS", "action": "DISABLE_ACCOUNT"}

    async def _isolate_container(self, data):
        print(f"ACTION: Isolating service {data.get('service')}")
        return {"status": "SUCCESS", "action": "ISOLATE_CONTAINER"}

    async def _deploy_decoy(self, data):
        print(f"ACTION: Deploying decoy credentials for {data.get('actor')}")
        return {"status": "SUCCESS", "action": "DEPLOY_DECOY"}

    async def _apply_firewall(self, data):
        print(f"ACTION: Applying firewall rule for {data.get('source_ip')}")
        return {"status": "SUCCESS", "action": "APPLY_FIREWALL"}

response_engine = ResponseEngine()
