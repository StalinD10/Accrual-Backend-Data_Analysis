import pandas as pd

class DataFrameConverter:
    @staticmethod
    async def convert_df(data_service):
        response = await data_service
        if response is None:
            return pd.DataFrame()
        data = [doc.__dict__ for doc in response]
        df = pd.DataFrame(data)
        return df
