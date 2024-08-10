import os
from neo4j import AsyncGraphDatabase

class Neo4jConfig:
    def __init__(self):
        self.neo4j_uri = os.environ.get("NEO4J_URI", "neo4j://localhost:7687")
        self.neo4j_username = os.getenv("NEO4J_USERNAME", "neo4j")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD", "6154277353")
        self.neo4j_database = os.getenv("NEO4J_DATABASE", "railway")

    async def get_neo4j_connection(self):
        return AsyncGraphDatabase.driver(self.neo4j_uri, auth=(self.neo4j_username, self.neo4j_password),
                                         database=self.neo4j_database)