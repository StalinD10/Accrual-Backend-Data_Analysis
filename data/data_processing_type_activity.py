from service.activity_type_in_faculty_service import ActivityTypeInFacultyService
from data.data_processing import DataProcesing

activity_type_in_faculty_service = ActivityTypeInFacultyService()
data_processing = DataProcesing()


class DataProcessingTypeActivity:
    async def find_type_by_faculty(self, faculty_name: str):
        df = await data_processing.filter_by_column(True, "Faculty", faculty_name,
                                                    activity_type_in_faculty_service.find_activity_type_by_faculty())
        total = len(df)
        result = {
            "data": df,
            "total": total
        }
        return result

    async def find_type_by_faculty_all(self):
        df = await data_processing.data_processing(
            activity_type_in_faculty_service.find_activity_type_by_faculty())
        response_json = df.to_dict(orient='records')
        total = len(df)
        result = {
            "data": response_json,
            "total": total
        }
        return result

    async def find_type_by_period(self, period: str):
        df = await data_processing.filter_by_column(True, "Period", period,
                                                    activity_type_in_faculty_service.find_activity_type_by_faculty())
        total = len(df)
        result = {
            "data": df,
            "total": total
        }
        return result

    async def find_by_faculty_and_column(self, faculty_name: str, column_name: str, element: str):
        df = await data_processing.filter_by_faculty_and_column(faculty_name, column_name, element,
                                                                activity_type_in_faculty_service.find_activity_type_by_faculty())
        response_json = df.to_dict(orient='records')
        total = len(df)
        result = {
            "data": response_json,
            "total": total
        }
        return result

    async def frequent_type(self, faculty_name: str):
        if faculty_name:
            df = await data_processing.filter_by_column(False, "Faculty", faculty_name,
                                                        activity_type_in_faculty_service.find_activity_type_by_faculty())
        else:
            df = await data_processing.data_processing(activity_type_in_faculty_service.find_activity_type_by_faculty())
        activity_frequency = df['Typeactivity'].value_counts().reset_index()
        activity_frequency.columns = ['Typeactivity', 'Frequency']
        response_json = activity_frequency.to_dict(orient='records')
        total = len(df)
        result = {
            "data": response_json,
            "total": total
        }
        return result

    async def activity_type_trends(self):
        df = await data_processing.data_processing(
            activity_type_in_faculty_service.find_activity_type_by_faculty())
        required_columns = ['Typeactivity', 'Period']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("The DataFrame must contains columns 'Typeactivity' y 'Period'")
        activity_counts = df.groupby(['Period', 'Typeactivity']).size().unstack(fill_value=0)
        activity_counts.reset_index(inplace=True)
        response_json = activity_counts.to_dict(orient='records')
        total = len(df)
        result = {
            "data": response_json,
            "total": total
        }
        return result

    async def identify_most_active_docents(self, top_n=None):
        df = await data_processing.data_processing(
            activity_type_in_faculty_service.find_activity_type_by_faculty())
        if not {'Docent', 'Typeactivity'}.issubset(df.columns):
            raise ValueError("The DataFrame must contain columns 'Docent' and 'Typeactivity'")
        activity_counts = df.groupby('Docent').size().reset_index(name='ActivityCount')
        ranked_docents = activity_counts.sort_values(by='ActivityCount', ascending=False)
        if top_n is not None:
            ranked_docents = ranked_docents.head(top_n)
        response_json = ranked_docents.to_dict(orient='records')
        total = len(ranked_docents)
        result = {
            "data": response_json,
            "total": total
        }

        return result
