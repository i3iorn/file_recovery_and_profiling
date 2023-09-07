import re
import string
from datetime import datetime

from src.profile.checks import profile_decorator


class Profiler:
    CHECKS = {
        'country_code': {'type': 'specific', 'value': 'A'},
        'language_code': {'type': 'specific', 'value': 'B'},
        'name': {'type': 'specific', 'value': 'D'},
        'ssn': {'type': 'specific', 'value': 'E'},
        'orgnr': {'type': 'specific', 'value': 'F'},
        'duns': {'type': 'specific', 'value': 'G'},
        'email': {'type': 'specific', 'value': 'H'},
        'url': {'type': 'complex', 'value': 'I'},
        'phone': {'type': 'complex', 'value': 'J'},
        'ipv4': {'type': 'rare', 'value': 'K'},
        'ipv6': {'type': 'rare', 'value': 'L'},
        'date': {'type': 'complex', 'value': 'P'},
    }

    def __init__(self, string: str):
        self.__string = string
        self.profile = self.__get_profile()

    def __repr__(self):
        return self.profile

    @property
    def general(self):
        return self.profile.get('general')

    @property
    def specific(self):
        return self.profile.get('specific')

    @property
    def complex(self):
        return self.profile.get('complex')

    @property
    def rare(self):
        return self.profile.get('rare')

    def __get_profile(self):
        profile = {}
        profile['general'] = self.__generate_profile('general')
        profile['specific'] = self.__generate_profile('specific')
        profile['complex'] = self.__generate_profile('complex')
        profile['rare'] = self.__generate_profile('rare')
        return profile
