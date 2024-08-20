from typing import Optional, List
from model.accrual_docent_in_faculty import AccrualDocentInFaculty
from service.neo4j_execute_query_service import Neo4jService

neo4j_service = Neo4jService()


class AccrualDocentInFacultyService:
    async def find_accrual_docent_by_faculty(self, faculty: str = None) -> Optional[List[AccrualDocentInFaculty]]:
        query = "MATCH (f:Faculty)<-[BELONGS_TO]-(p:Person)-[HAS_PLAN]->(k:Plan)-[HAS_ACTIVITY]->(a:Activity) RETURN DISTINCT p.names AS Names, p.lastnames AS LastNames, f.faculty_name AS Faculty"
        if faculty is not None:
            query = "MATCH (f:Faculty)<-[BELONGS_TO]-(p:Person)-[HAS_PLAN]->(k:Plan)-[HAS_ACTIVITY]->(a:Activity) WHERE f.faculty_name=$faculty RETURN DISTINCT p.names AS Names, p.lastnames AS LastNames, f.faculty_name AS Faculty"
        response = await neo4j_service.execute_query(
            query,
            lambda record: AccrualDocentInFaculty(
                names=record['Names'],
                lastNames=record['LastNames'],
                faculty=record['Faculty']
            ),
            faculty=faculty
        )
        return response