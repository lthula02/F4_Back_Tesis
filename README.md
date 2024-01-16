# Backend - Trabajo de Grado

- **Universidad Metropolitana**
- Título: Subsistema para el análisis de variabilidad como mecanismo para el diseño de arquitecturas de referencia
- Autores: [Christian Behrens](https://github.com/cbehrensunimet) y [Nicolás Briceño](https://github.com/nicoabb)

## Cómo comenzar

- `pipenv shell`
- `pipenv install (solo la primera vez)`
- `python manage.py runserver`

Se pueden encontrar problemas en la versión de Python, *este trabajo fue realizado con Python 3.9*. El archivo `pipfile` fue generado a partir del `requirements.txt`, este último permanece como backup de los requerimientos del sistema.

**Nota: se debe estar corriendo backend y frontend para que funcione el proyecto, ya que la información se guarda en la cuenta de Google enlazada**

#### [Repositorio del Frontend](https://github.com/nicoabb/F4_Front_Tesis)

## Contexto de la aplicación desarrollada

La investigación *Estudio de la ingeniería inversa en el contexto de generación de arquitecturas referenciales*, busca diseñar una metodología para la generación de arquitecturas de referencia, a partir de la aplicación de procedimientos propios de la ingeniería inversa (Guillén et al., 2020). Esta investigación se desarrolla en tres etapas: la primera etapa implica un estudio exhaustivo del estado del arte; la segunda etapa se centra en el diseño y construcción de un prototipo de herramienta; y la tercera y última etapa se dedica a la validación del método propuesto.

La presente investigación corresponde a la segunda etapa, que se divide en cuatro actividades. Esta es la cuarta y última actividad. El trabajo previo incluyó, en primer lugar, la construcción de la arquitectura global del prototipo y la generación de un grafo como resultado del análisis del código fuente del sistema a analizar (Cafarelli y Mariña, 2021). En segundo lugar, se desarrolló un subsistema para la identificación de componentes conceptuales mediante la aplicación de métricas (D’Lacoste y Perez, 2022). Finalmente, como tercera actividad, se desarrolló un subsistema para la reconstrucción de la arquitectura de un sistema (González y Rodríguez, 2023). Tomando como entrada las arquitecturas generadas en la tercera actividad, **este trabajo realiza el análisis de variabilidad para generar una arquitectura de referencia**, cerrando así, la etapa de diseño y construcción del prototipo de software.

## Pasos para utilizar la aplicación

1. Descarga e instala la herramienta Doxygen en tu computadora
2. Descarga los archivos que deseas procesar y conviértelos en archivos XML utilizando Doxygen*
3. Agrega la nueva arquitectura a la aplicación (los archivos de interés). Ya sea en un nuevo proyecto o en uno ya existente
4. Haz clic en la esquina inferior derecha (tres barras), saldrá una tabla de **Nodos, Relaciones y Componentes Compuestos**
5. En la tabla *Relaciones* define las métricas específicas para calcular las relaciones entre nodos y la agrupación de componentes. **Se recomienda utilizar las predeterminadas**:
   - Peso DMS: 5
   - Peso Mapeo de Paquete: 60
   - Peso Semejanza de Nombre: 35
   - Umbral Semejanza: 40
   - Umbral Acoplamiento: 50
   - Umbral Q: -0.1
6. En la misma pestaña, haga clic en **Calcular Metricas** y posteriormente **Unir Componentes**. Este proceso no debe tardar más de 5 minutos
7. En la tabla *Componentes Compuestos* haga clic en **Calcular Interfaces**

Una vez realizado estos pasos podrá visualizar el grafo de la arquitectura. A continuación para la visualización de los diagramas debe:

8. Documentar la funcionalidad de cada Nodo en la tabla *Nodos*
9. Dar un nombre de aspecto a cada Componente Compuesto (opcional), el programa tomará el ID como predeterminado, el aspecto debe indicar la función general del componente, de forma que ayude en la comprensión de la arquitectura
10. Haga clic en los 3 puntos dentro del recuadro blanco de su proyecto (a la izquierda de la página), y seleccione cualquiera de las siguientes opciones:
    - Diagrama UML de la Arquitectura: descarga el UML de la arquitectura seleccionada, *no se descargará si no está visualizando ninguna de sus arquitecturas en el proyecto*
    - Mostrar variabilidad: descarga el diagrama de variabilidad del proyecto completo. Indica la funcionalidad de cada nodo dentro de los aspectos en el dominio y cómo cambian de enfoque entre arquitecturas.
    - Diagrama de componentes: descarga el diagrama de componentes del proyecto. Muestra la relación entre los aspectos (dependencias) y la frecuencia con la que aparece cada uno en las arquitecturas estudiadas

**La eficacia de los resultados obtenidos dependerá en gran medida de la competencia del usuario y el conocimiento que posea acerca de las arquitecturas estudiadas**

**NOTA: Este trabajo optó por archivos .php de código abierto, y se enfocó únicamente en aquellos que comenzaron con el carácter "_" como, por ejemplo, “_db_message_source_8php.xml”.*