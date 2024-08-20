from typing import Optional, List
from model.institution_doctorate_docent_faculty import InstitutionDoctorateDocentFaculty

from service.neo4j_execute_query_service import Neo4jService

neo4j_service = Neo4jService()


class InstitutionDocentFacultyService:
    async def find_institution_docent_by_faculty(self, faculty: str = None) -> Optional[List[InstitutionDoctorateDocentFaculty]]:
        query = "MATCH (a:Institution)<-[DOCTORAL_STUDY_AT_INSTITUTION]-(p:Person)-[BELONGS_TO]->(f:Faculty) RETURN a.institution_name as Institution, p.names AS Names, p.lastnames AS LastNames, f.faculty_name AS Faculty"
        if faculty is not None:
            query = "MATCH (a:Institution)<-[DOCTORAL_STUDY_AT_INSTITUTION]-(p:Person)-[BELONGS_TO]->(f:Faculty) WHERE f.faculty_name=$faculty RETURN a.institution_name as Institution, p.names AS Names, p.lastnames AS LastNames, f.faculty_name AS Faculty"
        response = await neo4j_service.execute_query(
            query,
            lambda record: InstitutionDoctorateDocentFaculty(
                institution=record['Institution'],
                names=record['Names'],
                lastNames=record['LastNames'],
                faculty=record['Faculty']
            ),
            faculty=faculty
        )
        return response
