"""
This module defines custom validators for user-related fields.
"""
import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator


cpf_regex_validator = RegexValidator(
    regex=r'^[0-9]*$',
    message='O campo deve conter apenas números.'
)

cpf_min_length_validator = MinLengthValidator(11, message='O CPF deve ter 11 dígitos.') # Adicionando mensagem para clareza

name_min_length_validator = MinLengthValidator(3, message='O nome deve ter mais de 3 caracteres.')

# A mensagem indica "pelo menos 5 caracteres", mas o valor é 6. Ajustei a mensagem.
password_min_length_validator = MinLengthValidator(6, message="A senha deve ter pelo menos 6 caracteres.")


def validate_email_format(email):
    """
    Validates the format of an email address.
    Raises ValidationError if the email is not in a valid format.
    """
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        raise ValidationError('O email fornecido não está em um formato válido.')
