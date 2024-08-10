from typing import Optional, List
from model.country_doctorate_docents_faculty import CountryDocentsFaculty
from config.neo4j_config import Neo4jConfig
from service.neo4j_execute_query_service import Neo4jService

neo4j_service = Neo4jService()


class CountryDoctorateService:
    async def get_country_doctorate_faculty_all(self, faculty: str = None) -> Optional[List[CountryDocentsFaculty]]:
        query = "MATCH(f:Faculty)<-[BELONGS_TO]-(p:Person)-[DOCTORAL_STUDY_AT_COUNTRY]->(c:Country) RETURN c.country_name AS Country,p.names AS Names, p.lastnames AS LastNames, f.faculty_name AS Faculty"
        if faculty is not None:
            query = "MATCH(f:Faculty)<-[BELONGS_TO]-(p:Person)-[DOCTORAL_STUDY_AT_COUNTRY]->(c:Country) WHERE f.faculty_name=$faculty RETURN c.country_name AS Country,p.names AS Names, p.lastnames AS LastNames, f.faculty_name AS Faculty"
        response = await neo4j_service.execute_query(
            query,
            lambda record: CountryDocentsFaculty(
                country=record['Country'],
                names=record['Names'],
                lastNames=record['LastNames'],
                faculty=record['Faculty']
            ),
            faculty=faculty
        )
        return response