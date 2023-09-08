from src.file import EnhancedFile

file_path = 'C:/Users/schrammelb/Downloads/2023-08-30_00000000000000052051_CaybonInternational.csv'

with EnhancedFile(file_path) as f:
    print(f.unique_columns)

