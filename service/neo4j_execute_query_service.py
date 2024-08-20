from pydantic import BaseModel
from typing import Type, TypeVar, Callable, Optional, List
from config.neo4j_config import Neo4jConfig

T = TypeVar('T', bound=BaseModel)


class Neo4jService:
    def __init__(self):
        self.neo4j = Neo4jConfig()
    async def execute_query(self, query: str, map_record: Callable[[dict], T], **parameters) -> Optional[List[T]]:
        driver = await self.neo4j.get_neo4j_connection()
        session = driver.session()
        results = []
        try:
            result = await session.run(query,**parameters)
            async for record in result:
                results.append(map_record(record))
        except Exception as error:
            print(f"Error: {error}")
        finally:
            await session.close()
            await driver.close()
        return results if results else None

