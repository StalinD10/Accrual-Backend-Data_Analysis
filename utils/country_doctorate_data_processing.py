from service.country_doctorate_service import CountryDoctorateService
import pandas as pd
from fastapi.responses import JSONResponse

country_doctorate_service = CountryDoctorateService()


class CountryDoctorateDataProcessing:

    # Obtenemos los datos del service y los tratamos:
    # eliminamos espacios vacios, los nombres los ponemos en minusculas, y eliminamos datos que contengan null
    async def convert_df(self, data_service):
        response = await data_service
        if response is None:
            return pd.DataFrame()
        data = [{
            'Country': doc.country,
            'Names': doc.names,
            'LastNames': doc.lastNames,
            'Faculty': doc.faculty
        } for doc in response]
        df = pd.DataFrame(data)
        df['Docent'] = df['Names'] + ' ' + df['LastNames']
        df['Docent'] = df['Docent'].str.strip()
        df['Docent'] = df['Docent'].str.lower().str.title()
        df = df[df['Docent'].str.strip() != '']
        return df

    # Obtenemos los datos y los enviamos al controlador en json
    async def process_data_all(self):
        df = await self.convert_df(country_doctorate_service.get_country_doctorate_faculty_all())
        json_result = df[['Country', 'Docent', 'Faculty']].to_dict(orient='records')
        return json_result

    # Obtenemos una lista de los 10 paises preferidos por los docentes para hacer su doctorado detodo el sistema o por facultad
    async def preferred_country_doctorate(self, faculty: str = None):
        df = await self.convert_df(country_doctorate_service.get_country_doctorate_faculty_all(faculty))
        country_counts = df['Country'].value_counts().reset_index()
        country_counts.columns = ['Country', 'Count']
        top_10_countries = country_counts.head(10).sort_values('Count', ascending=False)
        result = top_10_countries.to_dict(orient='records')
        return JSONResponse(content=result)
