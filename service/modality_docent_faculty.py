from typing import Optional, List
from model.modality_docent_faculty import Modality_Accrual_Docent

from service.neo4j_execute_query_service import Neo4jService

neo4j_service = Neo4jService()


class ModalityDocentFacultyService:
    async def find_modality_docent_by_faculty(self, faculty: str = None) -> Optional[List[Modality_Accrual_Docent]]:
        query = "MATCH(f:Faculty)<-[BELONGS_TO]-(p:Person)-[HAS_MODALITY]->(m:AccrualModality) RETURN m.accrual_modality_name AS Modality,p.names AS Names, p.lastnames AS LastNames, f.faculty_name AS Faculty"
        if faculty is not None:
            query = "MATCH(f:Faculty)<-[BELONGS_TO]-(p:Person)-[HAS_MODALITY]->(m:AccrualModality) WHERE f.faculty_name=$faculty RETURN m.accrual_modality_name AS Modality,p.names AS Names, p.lastnames AS LastNames, f.faculty_name AS Faculty"
        response = await neo4j_service.execute_query(
            query,
            lambda record: Modality_Accrual_Docent(
                modality=record['Modality'],
                names=record['Names'],
                lastNames=record['LastNames'],
                faculty=record['Faculty']
            ),
            faculty=faculty
        )
        return response