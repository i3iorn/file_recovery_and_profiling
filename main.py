import string
from pprint import pprint

from src import EnhancedFile

file_path = 'C:/Users/bjosch/Downloads/Kortkonto-12010408292-20230821.csv'

with EnhancedFile(file_path) as f:
    for c in f.column_description:
        pprint(f.column_description[c])
