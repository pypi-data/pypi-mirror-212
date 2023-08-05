from jinja2 import Environment, FileSystemLoader, BaseLoader
from arrendatools.plantillas.filters.fechas import dias_del_año, formato_fecha, aplicar_timedelta, trimestre
from arrendatools.plantillas.filters.numeros import formato_divisa, formato_porcentaje, numero_a_palabras


custom_functions = {
    "aplicar_timedelta": aplicar_timedelta,
    "numero_a_palabras": numero_a_palabras,
    "formato_divisa": formato_divisa,
    "formato_porcentaje": formato_porcentaje,
    "formato_fecha": formato_fecha,
    "dias_del_año": dias_del_año,
    "trimestre": trimestre
}

custom_filters = {**custom_functions}


def aplicar_plantilla(directorio_plantillas, plantilla, datos):
    environment = Environment(loader=FileSystemLoader(directorio_plantillas))
    environment.filters.update(custom_filters)
    environment.globals.update(custom_functions)
    template = environment.get_template(plantilla)
    return template.render(datos)


def aplicar_plantilla_texto(texto_plantilla, datos):
    try:
        environment = Environment(loader=BaseLoader)
        environment.filters.update(custom_filters)
        environment.globals.update(custom_functions)
        template = environment.from_string(texto_plantilla)
        return template.render(datos)
    except Exception as e:
        return str(e)
