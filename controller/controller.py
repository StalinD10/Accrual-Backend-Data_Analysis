from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import HTTPException, status

from service.country_doctorate_service import CountryDoctorateService
from utils.country_doctorate_data_processing import CountryDoctorateDataProcessing

router = APIRouter(prefix="/apiAnalytics")
country_doctorate_service = CountryDoctorateService()
country_doctorate_data_processing = CountryDoctorateDataProcessing()


@router.get("/findCountryDoctorateDocentsAll")
async def getCountryDoctorateDocentsAll():
    results = await country_doctorate_data_processing.process_data_all()
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")
    return results


@router.get("/findCountryDoctorateDocentsFaculty/{faculty}")
async def get_country_doctorate_docents_faculty(faculty: str):
    results = await country_doctorate_service.get_country_doctorate_faculty_all(faculty)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")
    return results


@router.get("/findPreferredCountryDoctorate")
async def findPreferred_country_doctorate(faculty: str = None):
    results = await country_doctorate_data_processing.preferred_country_doctorate(faculty)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No results found")
    return results
