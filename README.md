# Tutor Virtual Unicaribe

Tutor virtual para el area de matemáticas.

Alumnos:

* Joan de Jesus Mendez Pool - 160300102@ucaribe.edu.mx -  [Github](https://github.com/JJWizardMP)
* Saulo Jesus Sanchez Dzul - 160300150@ucaribe.edu.mx -  [Github](https://github.com/SauloSanchez)
* Noe Vazquez Pompa - 160300153@ucaribe.edu.mx -  [Github](https://github.com/Famvazpom)

Asesor:

* Fernando Gomez Garcia

### Nota importante

Para que se ejecute correctamente el proyecto, es necesario hacer un cambio a la libreria chatterbot, para ello es necesario ir al archivo " envs\[Nombre del enviroment]\lib\python3.7\site-packages\chatterbot\languages.py" y cambiar la linea 1940.

La linea se vera como la siguiente:

```
    ISO_639_1 = 'es'
```

Debe quedar de la siguiente forma

```
    ISO_639_1 = 'es_core_news_sm'
```

De igual forma en el archivo " envs\[Nombre del enviroment]\lib\python3.7\site-packages\chatterbot\storage\storage_adapter.py" modificar la linea 21, la cual se vera como la siguiente:

```
            'tagger_language', languages.ENG
```

Debe cambiarse de la siguiente forma:

```
            'tagger_language', languages.SPA
```

Posteriormente, hay que descargar los modelos referentes al idioma español:

```
python -m spacy download es_core_news_sm
```

Cabe mencionar que estos pasos pueden replicarse a cualquier idioma soportado por Spacy.

Estos pasos especificos son para ejecutar chatterbot con spacy 3.0 o superior con el idioma español.
