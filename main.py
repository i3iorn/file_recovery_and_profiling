import string
from pprint import pprint

from src import EnhancedFile
from src.profile.checks import GeneralChecks

file_path = 'C:/Users/schrammelb/Downloads/2023-08-30_00000000000000052051_CaybonInternational.csv'
"""
with EnhancedFile(file_path) as f:
    for c in f.column_description:
        pprint(f.column_description[c])
"""

gc = GeneralChecks('2023-05-05')
print(gc)