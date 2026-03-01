import asyncio
import httpx
import time
import random
from simulator.log_generator import LogGenerator

async def send_logs(count: int):
    gen = LogGenerator()
    async with httpx.AsyncClient() as client:
        for i in range(count):
            log_type = random.choice(["IAM", "API", "NETWORK", "LLM", "EMAIL"])
            if log_type == "IAM": log = gen.generate_iam_log()
            elif log_type == "API": log = gen.generate_api_log()
            elif log_type == "NETWORK": log = gen.generate_network_log()
            elif log_type == "LLM": log = gen.generate_llm_log()
            else: log = gen.generate_email_log()
            
            try:
                await client.post("http://localhost:8000/api/v1/events/ingest", json=log)
                if i % 100 == 0:
                    print(f"Sent {i} logs...")
            except Exception as e:
                print(f"Error sending log: {e}")
            
            # Simulate high-load with slight delay
            await asyncio.sleep(0.01)

if __name__ == "__main__":
    print("Starting load test: Sending 1000 logs to BOTCOP...")
    start = time.time()
    asyncio.run(send_logs(1000))
    end = time.time()
    print(f"Load test complete in {end - start:.2f} seconds.")
