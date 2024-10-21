import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator

cpf_regex_validator = RegexValidator(
    regex='^[0-9]*$', 
    message='O campo deve conter apenas números.'
)

cpf_min_length_validator = MinLengthValidator(11)

name_min_length_validator = MinLengthValidator(3, message='O nome deve ter mais de 3 caracteres.')

password_min_length_validator = MinLengthValidator(6, message="Senha deve ter pelo menos 5 caracteres.")

def validate_email_format(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        raise ValidationError('O email fornecido não está em um formato válido.')
