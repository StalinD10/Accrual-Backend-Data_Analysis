from data.data_processing import DataProcesing
import pandas as pd
from scipy import stats

data_processing = DataProcesing()


class DataStatistics():

    async def calculate_statistics(self, service):
        # Convertir los datos en un DataFrame (simulación)
        df = await data_processing.data_processing(service)
        # Contar la cantidad de docentes por facultad
        faculty_counts = df['Faculty'].value_counts()

        # Calcular estadísticas sobre los conteos por facultad
        mean_value = faculty_counts.mean()
        median_value = faculty_counts.median()

        # Calcular la moda de manera segura
        mode_result = faculty_counts.mode()
        mode_value = mode_result[0] if not mode_result.empty else None

        # Calcular cuartiles
        quartiles = faculty_counts.quantile([0.25, 0.5, 0.75]).to_dict()

        # Generar tabla de frecuencia
        frequency_table = faculty_counts.to_dict()

        # Convertir tipos int64 a tipos nativos de Python para evitar problemas con JSON
        mean_value = float(mean_value)
        median_value = float(median_value)
        mode_value = int(mode_value) if mode_value is not None else None
        quartiles = {key: float(value) for key, value in quartiles.items()}
        frequency_table = {key: int(value) for key, value in frequency_table.items()}

        # Devolver los resultados en formato JSON
        return {
            "mean": mean_value,
            "median": median_value,
            "mode": mode_value,
            "quartiles": quartiles,
            "frequency_table": frequency_table
        }