# Hackatón JusLab
## Anonimización de Resoluciones Judiciales

Prototipo desarrollado el día 12/12/2019 por:

* Ana Haydée Di Iorio (@anadiiorio)
* Guadalupe González (@guadag12)
* Bruno Constanzo (@bruno_constanzo)

Información del evento: https://consejo.jusbaires.gob.ar/agenda/evento/44.

Hackdash del desafío: https://hackdash.org/projects/5dee8cce8f5583072ba590a1.

**En el día de la fecha se dio acceso a otros archivos de prueba, distintos
a los que linkea el hackdash.** Por lo tanto el código desarrollado no coincide
con lo allí indicado. Las principales diferencias son:

* Los archivos que se entregaron durante el hackatón no habían sido
  anonimizados, sino que contaban con datos ficticios (ej: Clark Kent se vió
  involucrado en un choque automovilístico con Lois Lane). Por esta razón, el
  desarrollo se enfoca en la detección de entidades con expresiones regulares
  y luego detección de entidades, más que en la inferencia de tipo de entidades
  en base al contexto.
* El conjunto de pruebas consistía únicamente en archivos DOCX. Si bien el
  conjunto original tenía también archivos ODT, la solución hecha en el momento
  trabaja únicamente sobre DOCX y se debería agregar funciones para manejar
  adecuadamente cada uno de los formatos.

El primer commit de este repo es el código como se desarrolló en el lugar. Si
luego decidimos agregar funcionalidades, será a través de commits posteriores.

### Requerimientos:
* python-docx
* spaCy

No incluído:
* odfpy (no se trabajó en el momento la opción de cargar documentos ODF)

### Limitaciones:
El presete software solamente fue probado contra 12 casos de resoluciones dados
como conjunto de prueba en el marco del evento. Incluso en estos casos, el
desarrollo (en su forma actual) no detecta correctamente todas las entidades y
por lo tanto necesita de una etapa de revisión posterior por un operador humano
que pueda supervisar los resultados y corregirlos.

La salida del programa es, por el momento, texto en la consola con resaltado de
color para identificar rápidamente dónde se detectaron entidades. Desarrollar
funcionalidad para emitir formatos de archivo específicos quedó pendiente para
desarrollos posteriores.
