class PreferredDataGeneralDocent(object):
        async def preferred_analysis(self, data, column: str, top_n: int = 10):
            counts = data[column].value_counts().reset_index()
            counts.columns = [column.capitalize(), 'Count']
            top_n_results = counts.head(top_n).sort_values('Count', ascending=False)
            return top_n_results
