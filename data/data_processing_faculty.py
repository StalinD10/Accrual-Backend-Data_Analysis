from fastapi.responses import JSONResponse

from data.convert_df import DataFrameConverter
from data.preferred_data_general_docent import PreferredDataGeneralDocent
from data.data_statistics import DataStatistics
from service.docent_in_faculty_service import DocentInFacultyService

data_frame_converter = DataFrameConverter()
preferred_data_general_docent = PreferredDataGeneralDocent()
data_statistics = DataStatistics()
docent_service = DocentInFacultyService()


class DataProcessingFaculty:

    async def data_processing(self, service, faculty: str = None):

        data = await data_frame_converter.convert_df(service)
        for col in data.select_dtypes(include=['object']).columns:
            data[col] = data[col].str.strip()
        data.columns = [col.capitalize() for col in data.columns]
        data['Docent'] = data['Names'] + ' ' + data['Lastnames']
        data['Docent'] = data['Docent'].str.lower().str.title()
        data = data.drop(columns=['Names', 'Lastnames'])
        data = data[data['Docent'].str.strip() != '']
        if faculty is not None:
            data = data.drop(columns=['Faculty'], errors='ignore')
        return data

    # Obtenemos los datos y los enviamos al controlador en json
    async def process_data_all(self, service, faculty: str = None):
        df = await self.data_processing(service, faculty)
        columns_to_include = list(df.columns)
        if 'Faculty' in df.columns:
            columns_to_include.append('Faculty')
        json_result = df[columns_to_include].to_dict(orient='records')
        total = len(df)
        result = {
            "data": json_result,
            "total": total
        }
        return result

    # estadisticas generales del docente
    async def statistics_docent(self):
        df = await data_statistics.calculate_statistics(docent_service.find_docent_by_faculty())
        return JSONResponse(content=df)

    # Obtenemos una lista de los 10 modalidades preferidos por los docentes para hacer su devengamiento
    async def preferred_docent(self, service, column_preferred: str, faculty: str = None):
        df = await self.data_processing(service, faculty)
        if df.empty:
            return []
        top_10 = await preferred_data_general_docent.preferred_analysis(df, column_preferred, 10)
        result = top_10.to_dict(orient='records')
        return JSONResponse(content=result)

    async def count_by_faculty(self, service, column_count: str, faculty: str = None):
        df = await self.data_processing(service, faculty)
        if df.empty:
            return []
        if 'Faculty' in df.columns:
            count_df = df.groupby(['Faculty', column_count]).size().reset_index(name='Count')
        else:
            count_df = df.groupby([column_count]).size().reset_index(name='Count')
        count_df = count_df.sort_values(by='Count', ascending=False)
        json_result = count_df.to_dict(orient='records')
        return json_result

    async def count_docents_faculty(self, service, faculty: str = None):
        df = await self.data_processing(service, faculty)
        if df.empty:
            return []
        count_by_faculty = df.groupby('Faculty').size().reset_index(name='Count')
        count_df = count_by_faculty.sort_values(by='Count', ascending=False)
        json_result = count_df.to_dict(orient='records')
        return json_result
