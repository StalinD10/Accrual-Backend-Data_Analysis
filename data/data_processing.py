import pandas as pd

from data.convert_df import DataFrameConverter

data_frame_converter = DataFrameConverter()


class DataProcesing:
    async def data_processing(self, service):
        try:
            data = await data_frame_converter.convert_df(service)
            for col in data.select_dtypes(include=['object']).columns:
                data[col] = data[col].str.strip().str.lower().str.title()
            data.columns = [col.capitalize() for col in data.columns]
            data['Docent'] = data['Names'].str.strip().str.lower().str.title() + ' ' + data[
                'Lastnames'].str.strip().str.lower().str.title()
            data = data.drop(columns=['Names', 'Lastnames'])
            data = data.dropna()
            return data
        except Exception as e:

            print(f"Error during data processing: {e}")
            return pd.DataFrame()

    async def filter_by_column(self, json: bool, column_name: str, element: str, service):
        try:
            df = await self.data_processing(service)
            filtered_df = df[df[column_name] == element].copy()
            if json:
                response_json = filtered_df.to_dict(orient='records')
                return response_json
            else:
                return filtered_df
        except KeyError as ke:
            print(f"Column '{column_name}' not found in DataFrame: {ke}")
            return [] if json else pd.DataFrame()
        except Exception as e:
            print(f"Error during filtering: {e}")
            return [] if json else pd.DataFrame()

    async def filter_by_faculty_and_column(self, faculty_name: str, column_name: str, element: str, service):
        try:
            df = await self.data_processing(service)
            df = df[df['Faculty'] == faculty_name].copy()
            df = df.drop(columns=['Faculty'])
            df = df[df[column_name] == element]
            return df
        except KeyError as e:
            return {"error": f"Column not found: {str(e)}"}
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}
