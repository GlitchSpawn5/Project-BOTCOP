import random
import time
import json
import uuid
from datetime import datetime

class LogGenerator:
    def __init__(self):
        self.users = ["admin", "dev_user", "hr_manager", "finance_exec", "sales_rep"]
        self.ips = ["192.168.1.50", "10.0.5.12", "172.16.0.4", "192.168.1.100"]
        self.services = ["auth-service", "data-api", "k8s-master", "llm-gateway"]

    def generate_iam_log(self, user=None, status=None):
        user = user or random.choice(self.users)
        status = status or random.choice(["SUCCESS", "FAILURE", "MFA_REQUIRED"])
        return {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "type": "IAM_LOGIN",
            "actor": user,
            "source_ip": random.choice(self.ips),
            "status": status,
            "geo": {
                "city": random.choice(["San Francisco", "London", "Tokyo", "Berlin", "Dubai"]),
                "country": "US",
                "lat": random.uniform(20, 50),
                "lon": random.uniform(-120, 130)
            },
            "biometrics": {
                "typing_speed": random.randint(40, 80),
                "error_rate": random.random() * 0.05
            },
            "details": f"Login attempt for user {user}"
        }

    def generate_api_log(self):
        return {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "type": "API_CALL",
            "actor": random.choice(self.users),
            "service": random.choice(self.services),
            "method": random.choice(["GET", "POST", "DELETE"]),
            "endpoint": f"/api/v1/{random.choice(['data', 'user', 'config'])}",
            "status_code": random.choice([200, 201, 403, 500])
        }

    def generate_network_log(self):
        return {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "type": "NETWORK_FLOW",
            "src": random.choice(self.ips),
            "dst": "10.0.0.1",
            "port": random.choice([80, 443, 22, 3306]),
            "bytes": random.randint(100, 10000)
        }

    def generate_llm_log(self, prompt=None):
        prompt = prompt or "Analyze these logs for me"
        return {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "type": "LLM_USAGE",
            "actor": random.choice(self.users),
            "prompt": prompt,
            "injection_score": random.random() * 0.1 # Baseline low
        }

    def generate_email_log(self):
        return {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "type": "EMAIL_METADATA",
            "sender": f"{random.choice(self.users)}@enterprise.com",
            "recipient": "external@gmail.com",
            "subject": "Q4 Financial Report",
            "has_attachment": random.choice([True, False])
        }

if __name__ == "__main__":
    generator = LogGenerator()
    while True:
        log_type = random.choice(["IAM", "API", "NETWORK", "LLM", "EMAIL"])
        if log_type == "IAM": log = generator.generate_iam_log()
        elif log_type == "API": log = generator.generate_api_log()
        elif log_type == "NETWORK": log = generator.generate_network_log()
        elif log_type == "LLM": log = generator.generate_llm_log()
        else: log = generator.generate_email_log()
        
        print(json.dumps(log))
        time.sleep(1)
