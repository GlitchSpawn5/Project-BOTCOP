from neo4j import GraphDatabase
from backend.core.config import settings

class GraphEngine:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            settings.NEO4J_URI, 
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
        )

    def close(self):
        self.driver.close()

    def process_log(self, log: dict):
        with self.driver.session() as session:
            if log["type"] == "IAM_LOGIN":
                session.execute_write(self._create_login_relation, log)
            elif log["type"] == "API_CALL":
                session.execute_write(self._create_api_relation, log)
            # Add other log types...

    @staticmethod
    def _create_login_relation(tx, log):
        query = (
            "MERGE (u:User {name: $actor}) "
            "MERGE (ip:IP {address: $source_ip}) "
            "CREATE (u)-[:LOGGED_IN {timestamp: $timestamp, status: $status}]->(ip)"
        )
        tx.run(query, actor=log["actor"], source_ip=log["source_ip"], 
               timestamp=log["timestamp"], status=log["status"])

    @staticmethod
    def _create_api_relation(tx, log):
        query = (
            "MERGE (u:User {name: $actor}) "
            "MERGE (s:Service {name: $service}) "
            "CREATE (u)-[:ACCESSED {timestamp: $timestamp, method: $method, status: $status_code}]->(s)"
        )
        tx.run(query, actor=log["actor"], service=log["service"], 
               timestamp=log["timestamp"], method=log["method"], status=log["status_code"])

    def get_graph_data(self):
        """Fetch nodes and edges for D3.js visualization."""
        with self.driver.session() as session:
            result = session.run("MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 100")
            nodes = []
            links = []
            node_ids = set()
            
            for record in result:
                n = record["n"]
                m = record["m"]
                r = record["r"]
                
                for node in [n, m]:
                    if node.id not in node_ids:
                        nodes.append({
                            "id": node.id,
                            "label": list(node.labels)[0],
                            "properties": dict(node)
                        })
                        node_ids.add(node.id)
                
                links.append({
                    "source": n.id,
                    "target": m.id,
                    "type": r.type,
                    "properties": dict(r)
                })
            
            return {"nodes": nodes, "links": links}

graph_engine = GraphEngine()
