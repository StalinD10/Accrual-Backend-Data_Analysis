from service.activity_subtype_in_faculty_service import ActivitySubtypeInFacultyService
from data.data_processing import DataProcesing

activity_subtype_in_faculty_service = ActivitySubtypeInFacultyService()
data_processing = DataProcesing()


class DataProcessingSubtypeActivity:

    async def find_subtype_by_faculty(self, faculty_name: str):
        df = await data_processing.filter_by_column(True, "Faculty", faculty_name,
                                                    activity_subtype_in_faculty_service.find_activity_subtype_by_faculty())
        total = len(df)
        result = {
            "data": df,
            "total": total
        }
        return result

    async def find_subtype_by_faculty_all(self):
        df = await data_processing.data_processing(
            activity_subtype_in_faculty_service.find_activity_subtype_by_faculty())
        response_json = df.to_dict(orient='records')
        total = len(df)
        result = {
            "data": response_json,
            "total": total
        }
        return result

    async def find_by_faculty_and_column(self, faculty_name: str, column_name: str, element: str, ):
        df = await data_processing.filter_by_faculty_and_column(faculty_name, column_name, element,
                                                                activity_subtype_in_faculty_service.find_activity_subtype_by_faculty())
        response_json = df.to_dict(orient='records')
        total = len(df)
        result = {
            "data": response_json,
            "total": total
        }
        return result

    async def frequent_subtype(self, faculty_name: str):
        if faculty_name:
            df = await data_processing.filter_by_column(False, "Faculty", faculty_name,
                                                        activity_subtype_in_faculty_service.find_activity_subtype_by_faculty())
        else:
            df = await data_processing.data_processing(
                activity_subtype_in_faculty_service.find_activity_subtype_by_faculty())
        activity_frequency = df['Subtype'].value_counts().reset_index()
        activity_frequency.columns = ['Subtype', 'Frequency']
        response_json = activity_frequency.to_dict(orient='records')
        total = len(df)
        result = {
            "data": response_json,
            "total": total
        }
        return result
