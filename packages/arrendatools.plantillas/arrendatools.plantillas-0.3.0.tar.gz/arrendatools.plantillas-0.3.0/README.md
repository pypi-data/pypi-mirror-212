# ArrendaTools Plantillas
![License](https://img.shields.io/github/license/hokus15/ArrendaToolsPlantillas)
[![Build Status](https://github.com/hokus15/ArrendaToolsPlantillas/actions/workflows/main.yml/badge.svg)](https://github.com/hokus15/ArrendaToolsPlantillas/actions)
![GitHub last commit](https://img.shields.io/github/last-commit/hokus15/ArrendaToolsPlantillas?logo=github)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/hokus15/ArrendaToolsPlantillas?logo=github)

Módulo de Python que aplica plantillas jinja. Además inlcuye filtros que pueden ser útiles a los arrendadores para la generación de recibos de alquiler, facturas, generar informes,....

## Requisitos

Este módulo requiere Python 3.7 o superior.

## Uso

A continuación se muestra un ejemplo de cómo usar el módulo:

```python
from arrendatools.plantillas.plantilla import aplicar_plantilla
import json

plantilla = "prueba.html"
fichero_datos = 'prueba.json'

with open(fichero_datos, encoding='utf-8') as json_file:
    data = json.load(json_file)

doc = aplicar_plantilla("./", plantilla, data)

with open('prueba-rendered.html', "wb") as archivo:
    archivo.write(doc.encode('utf-8'))

```
