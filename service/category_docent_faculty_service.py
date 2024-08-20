from typing import Optional, List
from model.category_docent_faculty import CategoryDocentFaculty
from service.neo4j_execute_query_service import Neo4jService

neo4j_service = Neo4jService()


class CategoryDocentFacultyService:
    async def find_category_docent_faculty(self, faculty: str = None) -> Optional[List[CategoryDocentFaculty]]:
        query = "MATCH(f:Faculty)<-[BELONGS_TO]-(p:Person)-[HAS_CATREGORY]->(c:DocentCategory)  RETURN c.docent_category_name AS Category,p.names AS Names, p.lastnames AS LastNames, f.faculty_name AS Faculty"
        if faculty is not None:
            query = "MATCH(f:Faculty)<-[BELONGS_TO]-(p:Person)-[HAS_CATREGORY]->(c:DocentCategory) WHERE f.faculty_name=$faculty RETURN c.docent_category_name AS Category,p.names AS Names, p.lastnames AS LastNames, f.faculty_name AS Faculty"
        response = await neo4j_service.execute_query(
            query,
            lambda record: CategoryDocentFaculty(
                category=record['Category'],
                names=record['Names'],
                lastNames=record['LastNames'],
                faculty=record['Faculty']
            ),
            faculty=faculty
        )
        return response
