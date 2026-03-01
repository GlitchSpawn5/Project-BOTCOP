import asyncio
import httpx
import time
import random
import json
from simulator.log_generator import LogGenerator
from simulator.threat_engine import ThreatEngine

async def run_simulators():
    gen = LogGenerator()
    threats = ThreatEngine(gen)
    
    async with httpx.AsyncClient() as client:
        print("Simulator Runner started. Streaming logs to BOTCOP Backend...")
        while True:
            # 90% chance of normal log, 10% chance of attack
            if random.random() > 0.1:
                log_type = random.choice(["IAM", "API", "NETWORK", "LLM", "EMAIL"])
                if log_type == "IAM": log = gen.generate_iam_log()
                elif log_type == "API": log = gen.generate_api_log()
                elif log_type == "NETWORK": log = gen.generate_network_log()
                elif log_type == "LLM": log = gen.generate_llm_log()
                else: log = gen.generate_email_log()
                logs = [log]
            else:
                print(">>> SHIELD ALERT: Threat simulation sequence triggered!")
                logs = threats.run_random_attack()

            for log in logs:
                try:
                    await client.post("http://localhost:8000/api/v1/events/ingest", json=log)
                except Exception as e:
                    print(f"Ingestion Error: {e}")
            
            await asyncio.sleep(random.uniform(0.5, 2.0))

if __name__ == "__main__":
    asyncio.run(run_simulators())
