from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import HTTPException, status

from service.country_doctorate_service import CountryDoctorateService
from utils.data_processing_faculty import DataProcessingFaculty
from service.modality_docent_faculty import ModalityDocentFacultyService
from service.category_docent_faculty_service import CategoryDocentFacultyService
from service.institution_docent_faculty_service import InstitutionDocentFacultyService
from service.docent_in_faculty_service import DocentInFacultyService
from service.accrual_docent_in_faculty_service import AccrualDocentInFacultyService
router = APIRouter(prefix="/apiAnalytics")
country_doctorate_service = CountryDoctorateService()
data_processing = DataProcessingFaculty()
modality_doctorate_service = ModalityDocentFacultyService()
category_doctorate_service = CategoryDocentFacultyService()
institution_doctorate_service = InstitutionDocentFacultyService()
docent_in_faculty_service = DocentInFacultyService()
accrual_doctorate_service = AccrualDocentInFacultyService()

# Country
@router.get("/findCountryDoctorateDocentsAll")
async def find_country_doctorate_docents_all():
    results = await data_processing.process_data_all(country_doctorate_service.get_country_doctorate_faculty_all())
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")
    return results

@router.get("/findCountryDoctorateDocentsFaculty/{faculty}")
async def find_country_doctorate_docents_faculty(faculty: str):
    results = await data_processing.process_data_all(
        country_doctorate_service.get_country_doctorate_faculty_all(faculty))
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")
    return results

@router.get("/findPreferredCountryDoctorate")
async def find_preferred_country_doctorate(faculty: str = None):
    results = await data_processing.preferred_docent(
        country_doctorate_service.get_country_doctorate_faculty_all(faculty), "Country", faculty)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")
    return results

@router.get("/countCountryFaculty")
async def count_country_faculty(faculty: str = None):
    results = await data_processing.count_by_faculty(
        country_doctorate_service.get_country_doctorate_faculty_all(faculty), "Country", faculty)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")
    return results

# Modality
@router.get("/findModalityDocentAll")
async def find_modality_docents_faculty_all():
    results = await data_processing.process_data_all(
        modality_doctorate_service.find_modality_docent_by_faculty())
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")
    return results

@router.get("/findModalityDocent/{faculty}")
async def find_modality_docent_faculty(faculty: str):
    results = await data_processing.process_data_all(
        modality_doctorate_service.find_modality_docent_by_faculty(faculty))
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")
    return results

@router.get("/findPreferredModalityDocent")
async def find_preferred_modality_docent(faculty: str = None):
    results = await data_processing.preferred_docent(
        modality_doctorate_service.find_modality_docent_by_faculty(faculty), "Modality", faculty)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")
    return results

@router.get("/countModalityFaculty")
async def count_modality_faculty(faculty: str = None):
    results = await data_processing.count_by_faculty(
        modality_doctorate_service.find_modality_docent_by_faculty(faculty), "Modality", faculty)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")
    return results

#Category
@router.get("/findCategoryDocentAll")
async def find_category_docents_faculty_all():
    results = await data_processing.process_data_all(
        category_doctorate_service.find_category_docent_faculty())
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")
    return results

@router.get("/findCategoryDocent/{faculty}")
async def find_category_docent_faculty(faculty: str):
    results = await data_processing.process_data_all(
        category_doctorate_service.find_category_docent_faculty(faculty))
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")
    return results

@router.get("/findPreferredCategoryDocent")
async def find_preferred_category_docent(faculty: str = None):
    results = await data_processing.preferred_docent(
        category_doctorate_service.find_category_docent_faculty(faculty), "Category", faculty)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")
    return results

@router.get("/countCategoryFaculty")
async def count_modality_faculty(faculty: str = None):
    results = await data_processing.count_by_faculty(
        category_doctorate_service.find_category_docent_faculty(faculty), "Category", faculty)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")
    return results

#Institution
@router.get("/findInstitutionDocentAll")
async def find_institution_docents_faculty_all():
    results = await data_processing.process_data_all(
        institution_doctorate_service.find_institution_docent_by_faculty())
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")
    return results

@router.get("/findInstitutionDocent/{faculty}")
async def find_institution_docent_faculty(faculty: str):
    results = await data_processing.process_data_all(
        institution_doctorate_service.find_institution_docent_by_faculty(faculty))
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")
    return results

@router.get("/findPreferredInstitutionDocent")
async def find_preferred_institution_docent(faculty: str = None):
    results = await data_processing.preferred_docent(
        institution_doctorate_service.find_institution_docent_by_faculty(faculty), "Institution", faculty)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")
    return results

@router.get("/countInstitutionFaculty")
async def count_institution_faculty(faculty: str = None):
    results = await data_processing.count_by_faculty(
        institution_doctorate_service.find_institution_docent_by_faculty(faculty), "Institution", faculty)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")
    return results

#Docents in Faculty
@router.get("/findDocentAll")
async def find_docents_faculty_all():
    results = await data_processing.process_data_all(
        docent_in_faculty_service.find_docent_by_faculty())
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")
    return results

@router.get("/findDocent/{faculty}")
async def find_docent_faculty(faculty: str):
    results = await data_processing.process_data_all(
        docent_in_faculty_service.find_docent_by_faculty(faculty))
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")
    return results

@router.get("/countDocentFaculty")
async def count_docent_faculty(faculty: str = None):
    results = await data_processing.count_docents_faculty(
        docent_in_faculty_service.find_docent_by_faculty(faculty))
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")
    return results

#Accrual docents in Faculty
@router.get("/findAccrualDocentAll")
async def find_accrual_docents_faculty_all():
    results = await data_processing.process_data_all(
        accrual_doctorate_service.find_accrual_docent_by_faculty())
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")
    return results

@router.get("/findAccrualDocent/{faculty}")
async def find_accrual_docent_faculty(faculty: str):
    results = await data_processing.process_data_all(
        accrual_doctorate_service.find_accrual_docent_by_faculty(faculty))
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")
    return results

@router.get("/countAccrualDocentFaculty")
async def count_accrual_docent_faculty(faculty: str = None):
    results = await data_processing.count_docents_faculty(
        accrual_doctorate_service.find_accrual_docent_by_faculty(faculty))
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")
    return results