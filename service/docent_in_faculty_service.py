from typing import Optional, List
from model.docent_in_faculty import DocentInFaculty
from service.neo4j_execute_query_service import Neo4jService

neo4j_service = Neo4jService()


class DocentInFacultyService:
    async def find_docent_by_faculty(self, faculty: str = None) -> Optional[List[DocentInFaculty]]:
        query = "MATCH(p:Person)-[BELONGS_TO]->(f:Faculty) RETURN p.names AS Names, p.lastnames AS LastNames, f.faculty_name AS Faculty"
        if faculty is not None:
            query = "MATCH(p:Person)-[BELONGS_TO]->(f:Faculty) WHERE f.faculty_name=$faculty RETURN p.names AS Names, p.lastnames AS LastNames, f.faculty_name AS Faculty"
        response = await neo4j_service.execute_query(
            query,
            lambda record: DocentInFaculty(
                names=record['Names'],
                lastNames=record['LastNames'],
                faculty=record['Faculty']
            ),
            faculty=faculty
        )
        return response