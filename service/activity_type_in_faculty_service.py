from typing import Optional, List
from model.activity_type_docent_in_faculty import ActivityTypeDocent
from service.neo4j_execute_query_service import Neo4jService

neo4j_service = Neo4jService()


class ActivityTypeInFacultyService:
    async def find_activity_type_by_faculty(self) -> Optional[List[ActivityTypeDocent]]:
        query = "MATCH (p:Person)-[HAS_PLAN]->(k:Plan)-[HAS_ACTIVITY]->(a:Activity)-[BELONGS_TO]-(s:ActivityType), (a)-[PERFORMED_AT]->(f:Faculty), (k)-[per:BELONGS_TO]->(d:Period) RETURN  DISTINCT p.names AS Names, p.lastnames AS LastNames, s.activity_type_name AS TypeActivity, f.faculty_name AS Faculty, d.period_value AS  Period  ORDER BY f.faculty_name"
        response = await neo4j_service.execute_query(
            query,
            lambda record: ActivityTypeDocent(
                names=record['Names'],
                lastNames=record['LastNames'],
                typeActivity=record['TypeActivity'],
                faculty=record['Faculty'],
                period=record['Period']
            )
        )
        return response
