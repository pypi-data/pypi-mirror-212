# -*- coding: utf-8 -*-

from babel.numbers import format_currency, format_percent
from num2words import num2words


def formato_divisa(cantidad, simbolo='€', formato=None, locale='es_ES', digitos_divisa=True, tipo_formato='standard', redondeo_decimal=True, separador_miles=True):
    """
    Convierte una cantidad en string con formato de divisa usando el simbolo y el locale pasados por parametro.

    Args:
        cantidad (float | decimal.Decimal | str): Cantidad a dar formato.
        simbolo (str): Simbolo para usar como divisa. Valor por defecto: '€'.
        formato (str | NumberPattern | None): El string de formato a usar. Valor por defecto None.
        locale (Locale | str | None): Locale a usar para la transformación. Valor por defecto: 'es_ES'.
        digitos_divisa (bool): Utiliza el número de dígitos decimales naturales de la moneda. Valor por defecto True.
        tipo_formato (Literal['name', 'standard', 'accounting']): El tipo de formato a aplicar. Valor por defecto 'standard'.
        redondeo_decimal (bool): truncar y redondear números de alta precisión al patrón de formato. Valor por defecto True.
        separador_miles (bool): activar/desactivar el separador de grupo en el formato de número de la configuración regional. Valor por defecto True.

    Returns:
        str: La cantidad con el formato indicado
    """

    return format_currency(cantidad, simbolo, formato, locale, digitos_divisa, tipo_formato, redondeo_decimal, separador_miles)


def formato_porcentaje(numero, formato=None, locale='es_ES', redondeo_decimal=True, separador_miles=True):
    """
    Convierte una cantidad en string con formato de divisa usando el simbolo y el locale pasados por parametro.

    Args:
        numero (float | decimal.Decimal | str): Cantidad a dar formato.
        formato (str | NumberPattern | None): El string de formato a usar. Valor por defecto None.
        locale (Locale | str | None): Locale a usar para la transformación. Valor por defecto: 'es_ES'.
        redondeo_decimal (bool): truncar y redondear números de alta precisión al patrón de formato. Valor por defecto True.
        separador_miles (bool): activar/desactivar el separador de grupo en el formato de número de la configuración regional. Valor por defecto True.

    Returns:
        str: La cantidad con el formato indicado
    """

    return format_percent(numero, formato, locale, redondeo_decimal, separador_miles)


def numero_a_palabras(numero, idioma='es', conversor='currency'):
    """
    Convierte un número a palabras en Español usando la librería num2words https://pypi.org/project/num2words/.

    Args:
        numero (float): Número a convertir.
        idioma (str): Idioma al cual convertir el número. Por defecto es Español.
        conversor (str): Tipo de conversion a palabras quequeremos usar. Puede tener los siguientes valores:
            cardinal
            ordinal
            ordinal_num
            year
            currency (por defecto)

    Returns:
        str: El número convertido a palabras usando el idioma y conversor indicados.
    """
    return num2words(numero, lang=idioma, to=conversor)
