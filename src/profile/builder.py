import re

from src.profile import profile_decorator


class Profiler:
    CHECKS = {
        'decimal': {'type': 'general', 'value': 1},
        'numeric': {'type': 'general', 'value': 2},
        'alpha': {'type': 'general', 'value': 4},
        'alnum': {'type': 'general', 'value': 8},
        'lower': {'type': 'general', 'value': 16},
        'upper': {'type': 'general', 'value': 32},
        'whitespace': {'type': 'general', 'value': 64},
        'title': {'type': 'general', 'value': 128},
        'ascii': {'type': 'general', 'value': 256},
        'country_code': {'type': 'specific'},
        'language_code': {'type': 'specific'},
        'phrase': {'type': 'general', 'value': 512},
        'name': {'type': 'specific'},
        'ssn': {'type': 'specific'},
        'orgnr': {'type': 'specific'},
        'duns': {'type': 'specific'},
        'email': {'type': 'specific'},
        'url': {'type': 'complex'},
        'phone': {'type': 'complex'},
        'ipv4': {'type': 'rare'},
        'ipv6': {'type': 'rare'},
        'blank': {'type': 'general', 'value': 1024},
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
        profile = {
            'general': {},
            'specific': {},
            'complex': {},
            'rare': {}
        }
        for check, properties in self.CHECKS.items():
            func_name = f"is_{check}"
            profile[properties.get('type')][check] = getattr(self, func_name)()

        result = {
            'string': self.__string,
            'general': sum([
                self.CHECKS.get(k).get('value')
                for k, v in profile.get('general').items()
                if v and self.CHECKS.get(k).get('type') == 'general'
            ]),
            'specific': [k for k, v in profile.get('specific').items() if v],
        }
        return result

    """ GENERAL CHECKS """
    @profile_decorator
    def is_decimal(self):
        return self.__string.isdecimal() and ('.' in self.__string or ',' in self.__string)

    @profile_decorator
    def is_numeric(self):
        return self.__string.isnumeric()

    @profile_decorator
    def is_alpha(self):
        return self.__string.isalpha()

    @profile_decorator
    def is_alnum(self):
        if self.is_numeric() or self.is_alpha():
            return False
        return self.__string.isalnum()

    @profile_decorator
    def is_lower(self):
        return self.__string.islower()

    @profile_decorator
    def is_upper(self):
        return self.__string.isupper()

    @profile_decorator
    def is_whitespace(self):
        return self.__string.isspace()

    @profile_decorator
    def is_title(self):
        return self.__string.istitle()

    @profile_decorator
    def is_ascii(self):
        return self.__string.isascii()

    @profile_decorator
    def is_blank(self):
        return self.__string == ''

    """ SPECIFIC CHECKS """
    @profile_decorator
    def is_country_code(self):
        return self.__string.isupper() and len(self.__string) == 2

    @profile_decorator
    def is_language_code(self):
        return self.__string.islower() and len(self.__string) == 2

    @profile_decorator
    def is_phrase(self):
        if len(self.__string) > 20 and len(self.__string.split(' ')) > 2:
            if len(re.findall(r'\w', self.__string)) < len(self.__string) / 1.5:
                return True
        return False

    @profile_decorator
    def is_ssn(self):
        return False

    @profile_decorator
    def is_orgnr(self):
        return False

    @profile_decorator
    def is_duns(self):
        return False

    @profile_decorator
    def is_email(self):
        return False

    """ COMPLEX CHECKS """
    @profile_decorator
    def is_url(self):
        return False

    @profile_decorator
    def is_name(self):
        for word in self.__string.split(' '):
            if not word.istitle() and len(word) > 3:
                return False
        return True

    @profile_decorator
    def is_phone(self):
        return False


    """ RARE CHECKS """
    @profile_decorator
    def is_ipv4(self):
        return False

    @profile_decorator
    def is_ipv6(self):
        return False

    @profile_decorator
    def is_mac(self):
        return False

    @profile_decorator
    def is_credit_card(self):
        return False

    @profile_decorator
    def is_credit_card_secure(self):
        return False

    @profile_decorator
    def is_iban(self):
        return False

    @profile_decorator
    def is_bic(self):
        return False

    @profile_decorator
    def is_isbn(self):
        return False

    @profile_decorator
    def is_isrc(self):
        return False

    @profile_decorator
    def is_issn(self):
        return False

    @profile_decorator
    def is_imei(self):
        return False

    @profile_decorator
    def is_imei_sv(self):
        return False

    @profile_decorator
    def is_upc(self):
        return False

    @profile_decorator
    def is_ean(self):
        return False

    @profile_decorator
    def is_ean13(self):
        return False

    @profile_decorator
    def is_ean8(self):
        return False

    @profile_decorator
    def is_local_phone_number(self):
        return False

    @profile_decorator
    def is_mime_type(self):
        return False
