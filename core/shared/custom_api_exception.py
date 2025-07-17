"""
This module defines a custom API exception for consistent error handling.
"""
from rest_framework.exceptions import APIException
from rest_framework import status


class CustomAPIException(APIException):
    """
    Custom API Exception class.

    This exception allows for custom detail messages and HTTP status codes
    to be returned in API responses.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "A server error occurred."
    default_code = 'error'

    def __init__(self, detail=None, status_code=None):
        """
        Initializes a new instance of CustomAPIException.

        Args:
            detail (str, optional): A custom error message. Defaults to None.
            status_code (int, optional): A custom HTTP status code. Defaults to None.
        """
        if detail is not None:
            # Converte o detalhe em um dicionário para consistência com o formato de erro do DRF
            self.detail = {'error': detail}
        else:
            # Se nenhum detalhe for fornecido, usa o default_detail da classe base
            self.detail = {'error': self.default_detail}

        if status_code is not None:
            self.status_code = status_code
        # Se nenhum status_code for fornecido, usa o status_code padrão da classe
