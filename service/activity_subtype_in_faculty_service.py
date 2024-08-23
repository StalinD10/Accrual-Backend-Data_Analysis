from typing import Optional, List
from model.activity_subtype_docent_in_faculty import ActivitySubtypeDocent
from service.neo4j_execute_query_service import Neo4jService

neo4j_service = Neo4jService()


class ActivitySubtypeInFacultyService:
    async def find_activity_subtype_by_faculty(self) -> Optional[List[ActivitySubtypeDocent]]:
        query = "MATCH (p:Person)-[:BELONGS_TO]->(f:Faculty)<-[:PERFORMED_AT]-(a:Activity)-[:BELONGS_TO]->(s:ActivitySubtype) RETURN DISTINCT p.names as Names, p.lastnames as LastNames, s.activity_subtype_name AS Subtype, f.faculty_name AS Faculty"
        response = await neo4j_service.execute_query(
            query,
            lambda record: ActivitySubtypeDocent(
                names=record['Names'],
                lastNames=record['LastNames'],
                subtype=record['Subtype'],
                faculty=record['Faculty']
            )
        )
        return response
