from data.data_processing import DataProcesing
from data.data_processing_faculty import DataProcessingFaculty
from service.docent_in_faculty_service import DocentInFacultyService
from fastapi.encoders import jsonable_encoder
import pandas as pd
import numpy as np

data_processing = DataProcesing()
data_processing_faculty = DataProcessingFaculty()
docent_service = DocentInFacultyService()


class DataStatistics():

    async def calculate_measures_central_tendency(self, service):
        df = await data_processing.data_processing(service)

        # Contar la cantidad de docentes por facultad
        faculty_counts = df['Faculty'].value_counts()

        # Calcular estadísticas sobre los conteos por facultad
        mean_value = faculty_counts.mean()
        median_value = faculty_counts.median()

        # Calcular la moda de manera segura
        mode_result = faculty_counts.mode()
        mode_value = mode_result[0] if not mode_result.empty else None

        # Convertir tipos int64 a tipos nativos de Python para evitar problemas con JSON
        mean_value = float(mean_value)
        median_value = float(median_value)
        mode_value = int(mode_value) if mode_value is not None else None
        # Devolver los resultados en formato JSON
        return {
            "mean": mean_value,
            "median": median_value,
            "mode": mode_value
        }

    async def calculate_general_dispersion_stats(self, service):
        df = await data_processing.data_processing(service)
        count_by_faculty = df.groupby('Faculty').size().reset_index(name='Count')
        count_df = count_by_faculty.sort_values(by='Count', ascending=False)

        variance = np.var(count_df['Count'], ddof=0)  # ddof=0 para varianza poblacional
        std_dev = np.std(count_df['Count'], ddof=0)  # ddof=0 para desviación estándar poblacional
        mean = np.mean(count_df['Count'])
        cv = (std_dev / mean) * 100 if mean != 0 else 0  # Coeficiente de variación

        return {
            "faculty": "Todas las facultades",
            "variance": variance,
            "standard_deviation": std_dev,
            "coefficient_of_variation": cv
        }

    async def calculate_dispersion_stats(self, service, column_group: str):
        data = await data_processing_faculty.count_by_faculty(service, "Category")
        df = pd.DataFrame(data)

        if column_group not in df.columns:
            return f"The column '{column_group}' does not exist in the data."

        dispersion_stats = df.groupby(column_group)['Count'].agg(
            variance=lambda x: np.var(x, ddof=0),
            standard_deviation=lambda x: np.std(x, ddof=0),
            mean=lambda x: np.mean(x)
        )
        dispersion_stats['coefficient_of_variation'] = dispersion_stats['standard_deviation'] / dispersion_stats['mean']

        if dispersion_stats.empty:
            return jsonable_encoder({"message": "No statistics available for the given category."})
        return jsonable_encoder(dispersion_stats.reset_index().to_dict(orient='records'))

    async def calculate_positioning_measures(self, service):

        df = await data_processing.data_processing(service)
        count_by_faculty = df.groupby('Faculty').size().reset_index(name='Count')

        counts = count_by_faculty['Count'].values
        counts = counts.astype(float)  # Convertir a float para evitar errores

        quartiles = np.percentile(counts, [25, 50, 75])
        deciles = np.percentile(counts, np.arange(10, 101, 10))
        percentiles = np.percentile(counts, np.arange(10, 100, 10))

        # Crear un diccionario con los resultados
        result = {
            "quartiles": {
                "Q1": quartiles[0],
                "Q2": quartiles[1],
                "Q3": quartiles[2],
            },
            "deciles": {
                f"D{i}": deciles[i - 1] for i in range(1, 11)
            },
            "percentiles": {
                f"P{p}": percentiles[(p // 10) - 1] for p in range(10, 100, 10)
            }
        }
        return result

    async def calculate_frequency_table(self, service):
        df = await data_processing.data_processing(service)

        count_by_faculty = df.groupby('Faculty').size().reset_index(name='Count')

        count_by_faculty['Frecuencia Absoluta'] = count_by_faculty['Count']

        total_count = count_by_faculty['Count'].sum()
        count_by_faculty['Frecuencia Relativa'] = count_by_faculty['Count'] / total_count

        count_by_faculty['Frecuencia Absoluta Acumulada'] = count_by_faculty['Frecuencia Absoluta'].cumsum()

        count_by_faculty['Frecuencia Relativa Acumulada'] = count_by_faculty['Frecuencia Relativa'].cumsum()

        count_by_faculty['Frecuencia Absoluta en Porcentajes'] = (count_by_faculty[
                                                                      'Frecuencia Absoluta'] / total_count) * 100

        count_by_faculty['Frecuencia Relativa en Porcentajes'] = count_by_faculty['Frecuencia Relativa'] * 100
        frecuencia_table = count_by_faculty[['Faculty', 'Frecuencia Absoluta', 'Frecuencia Relativa',
                                             'Frecuencia Absoluta Acumulada', 'Frecuencia Relativa Acumulada',
                                             'Frecuencia Absoluta en Porcentajes',
                                             'Frecuencia Relativa en Porcentajes']]

        return frecuencia_table.to_dict(orient='records')
