import json
import random
from collections import Counter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src import EnhancedLine


def profile_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


class ColumnProfiler:
    def __init__(self, lines: list['EnhancedLine']):
        self.__lines = lines
        with open('src/profiles.json', 'r') as json_file:
            self.__profile_details = json.load(json_file)
        self.__profile = self.__calculate_profile()

    def __repr__(self):
        return f"ColumnProfiler(profile={self.__profile})"

    def __str__(self):
        return self.__profile.__str__()

    def __dict__(self):
        return self.__profile

    def __iter__(self):
        return self.__profile.__iter__()

    def __getitem__(self, item: int):
        return self.__profile.get(item)

    def __calculate_general_profile(self):
        pass

    def __calculate_profile(self):
        """
        Loop through all rows and all fields for each row and count the different profile strings. The most common
        profile string is the profile for that column.
        """
        g_prof = {}
        s_prof = {}
        c_prof = {}
        for line in self.__lines:
            for i, field in enumerate(line.fields):
                if i not in g_prof:
                    g_prof[i] = []
                    s_prof[i] = []
                    c_prof[i] = []
                if field.profile.general != 1024:
                    g_prof[i].append(field.profile.general)
                    s_prof[i].append(field.profile.specific)
                    c_prof[i].append(field.profile.complex)

        result = {}
        for i, profile_list in g_prof.items():
            p = Counter(profile_list).most_common(1)[0][0]
            result[i] = {
                'value': f"{p}",
                'example': f"{random.choice(self.__lines).fields[i]}",
                'probable_type': self.__profile_details.get(str(p), {'name': 'Unknown'}).get('name'),
            }

        for i, profile_list in s_prof.items():
            p = Counter(profile_list).most_common(1)[0][0]
            result[i]['spcific'] = self.__profile_details.get(str(p), {'name': 'Unknown'}).get('name')

        for i, profile_list in c_prof.items():
            p = Counter(profile_list).most_common(1)[0][0]
            result[i]['complex'] = self.__profile_details.get(str(p), {'name': 'Unknown'}).get('name')

        return result
