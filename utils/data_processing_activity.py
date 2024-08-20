from fastapi.responses import JSONResponse

from utils.convert_df import DataFrameConverter

data_frame_converter = DataFrameConverter()


class DataProcessingActivity:
    async def data_processing_activity(self, service):
        data = await data_frame_converter.convert_df(service)
        for col in data.select_dtypes(include=['object']).columns:
            data[col] = data[col].str.strip()
        data.columns = [col.capitalize() for col in data.columns]
        data['Docent'] = data['Names'] + ' ' + data['Lastnames']
        data['Docent'] = data['Docent'].str.lower().str.title()
        data = data.drop(columns=['Names', 'Lastnames'])
        return data

    async def filter_by_faculty(self, service, faculty_name: str):
        df = await data_frame_converter.convert_df(service)
        filtered_df = df[df['Faculty'] == faculty_name].copy()
        response_json = filtered_df.drop(columns=['Faculty']).to_dict(orient='records')
        return response_json

    async def filter_by_subtype(self, service, subtype_name: str):
        df = await data_frame_converter.convert_df(service)
        filtered_df = df[df['Subtype'] == subtype_name].copy()
        response_json = filtered_df.to_dict(orient='records')
        return response_json