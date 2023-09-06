import time
from pprint import pprint

from src import EnhancedFile

file_path = 'C:/Users/schrammelb/Downloads/CaybonInternational_OUT_20230831_iq_matched.csv'


with EnhancedFile(file_path) as f:
    for c in f.column_description:
        pprint(f.column_description[c])