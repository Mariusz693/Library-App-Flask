from datetime import date
from wtforms.validators import ValidationError


class PasswordValidator:

    def __call__(self, form, field):
        password = field.data

        if len(password) < 8:
            raise ValidationError('Hasło musi mieć minimalnie 8 znaków!')

        if len(password) > 64:
            raise ValidationError('Hasło może mieć maksymalnie 64 znaki!')

        contains_lower_char = False
        contains_upper_char = False
        
        for char in password:
            if char.islower():
                contains_lower_char = True
                break
        for char in password:
            if char.isupper():
                contains_upper_char = True
                break
        
        if (contains_lower_char is False) or (contains_upper_char is False):
            raise ValidationError('Hasło musi zawierać małe i duże litery!')

        if not any([char.isdigit() for char in password]):
            raise ValidationError('Hasło musi zawierać minimum jedną cyfrę!')

        special_char = """!@#$%^&*()_+-={}[]|\:";'<>?,./"""
        contains_special_char = False
        
        for char in special_char:
            if char in password:
                contains_special_char = True
                break
        
        if contains_special_char is False:
            raise ValidationError(f'Hasło musi zawierać znak specjalny {special_char}!')
        
        return


class DateRangeValidator:

    def __init__(self):
        self.max = date.today()
        self.field_flags = {}
        if self.max is not None:
            self.field_flags['max'] = self.max
        
    def __call__(self, form, field):
        data = field.data
        
        if data > self.max:

            raise ValidationError('Data nie może być większa niż dziś')

        return


class EqualDateToValidator:

    def __init__(self, field_name):
        self.field_name = field_name

    def __call__(self, form, field):
        
        try:
            other = form[self.field_name]
        except KeyError:

            raise ValidationError('Błąd nazwy pola')
        
        if field.data <= other.data:

            raise ValidationError('Data musi być większa niż urodzenia')
        
        return