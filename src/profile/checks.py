import re
import string as s
from datetime import datetime


def profile_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


class IChecks:
    IS = NotImplementedError
    HAS = NotImplementedError

    DATE_FORMATS = [
        '%Y-%m-%d',
        '%d-%m-%Y',
        '%d.%m.%Y',
        '%d/%m/%Y',
        '%Y%m%d',
        '%d%m%Y',
        '%d%m%y',
    ]

    def __init__(self, string):
        self.__string = string
        self.__is_profile: str = self.__generate_profile('is')
        self.__has_profile: str = self.__generate_profile('has')
        self.__profile = self.__is_profile + self.__has_profile

    def __repr__(self):
        return self.__profile

    def __generate_profile(self, check_type: str):
        profile = ''
        for check in self.IS:
            func_name = f"{check.lower()}"
            profile += '1' if self.__run_check(func_name, check_type) else '0'
        return profile

    def __run_check(self, check, check_type: str):
        if check_type == 'is':
            return getattr(self, check)(self.__string)
        elif check_type == 'has':
            for c in self.__string:
                if getattr(self, check)(c):
                    return True


class GeneralChecks(IChecks):
    IS = [
        'decimal',
        'numeric',
        'alpha',
        'alnum',
        'lower',
        'upper',
        'whitespace',
        'title',
        'ascii',
        'blank',
        'punctuation',
        'hexadecimal',
        'phrase',
        'special'
    ]
    HAS = [
        'alpha',
        'digit',
        'lower',
        'upper',
        'whitespace',
        'blank',
        'punctuation',
        'special',
    ]

    """ GENERAL CHECKS """
    @staticmethod
    @profile_decorator
    def decimal(string:str):
        return string.isdecimal()

    @staticmethod
    @profile_decorator
    def numeric(string: str):
        return string.isnumeric()

    @staticmethod
    @profile_decorator
    def alpha(string: str):
        return string.isalpha()

    @staticmethod
    @profile_decorator
    def alnum(string: str):
        return string.isalnum()

    @staticmethod
    @profile_decorator
    def lower(string: str):
        return string.islower()

    @staticmethod
    @profile_decorator
    def upper(string: str):
        return string.isupper()

    @staticmethod
    @profile_decorator
    def whitespace(string: str):
        return string.isspace()

    @staticmethod
    @profile_decorator
    def title(string: str):
        return string.istitle()

    @staticmethod
    @profile_decorator
    def ascii(string: str):
        return string.isascii()

    @staticmethod
    @profile_decorator
    def blank(string: str):
        return string == ''

    @staticmethod
    @profile_decorator
    def punctuation(string: str):
        return string in s.punctuation

    @staticmethod
    @profile_decorator
    def hexadecimal(string: str):
        return string in s.hexdigits

    @staticmethod
    @profile_decorator
    def phrase(check_type: str):
        return False

    @staticmethod
    @profile_decorator
    def special(check_type: str):
        return False


class SpecificChecks(IChecks):
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


class ComplexChecks(IChecks):
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

    @profile_decorator
    def is_date(self):
        for date_format in self.DATE_FORMATS:
            try:
                datetime.strptime(self.__string, date_format)
                return True
            except ValueError:
                pass


class RareChecks(IChecks):
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
