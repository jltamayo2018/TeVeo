# ENTREGA CONVOCATORIA JUNIO

# ENTREGA DE PRÁCTICA

## Datos

* Nombre: Jose Luis Tamayo Díez
* Titulación: Ingeniería Telemática
* Cuenta en laboratorios: jltamayo
* Cuenta URJC: jl.tamayo.2018
* Video básico (url): https://youtu.be/B5K6URiHbZ8
* Video parte opcional (url): https://youtu.be/L3Lg55wVsQg
* Despliegue (url): https://joseluistamayo.pythonanywhere.com
* Contraseñas: Como e indica en la práctica, NO hay autenticación de usuarios, por lo que NO hay contraseñas
* Cuenta Admin Site: admin/admin

## Resumen parte obligatoria

### Página de cada recurso

- En la **página principal** se muestra un listado de comentarios, donde se indica:
	- el nombre de la cámara (enlace a dicha cámara)
	- el comentario
	- autor
	- fecha del comentario
	- imagen de la cámara en el momento en que se puso el comentario

- En la **página de cámaras** se muestra:
	- listado de fuentes de datos, de donde se obtienen las cámaras
	- listado de cámaras (con una imagen aleatoria de una de ellas al principio), se muestra su:
		- id
		- nombre
		- enlace a la cámara estática
		- enlace a la cámara dinámica
		- número de comentarios

- En la **página estática de cada cámara** se muestra:
	- detalles de la cámara
	- enlace a la cámara dinámica
	- enlace a la cámara JSON
	- imagen actual de la cámara
	- enlace para dejar comentario
	- comentarios que hay para dicha cámara

- En la **página dinámica** se muestra:
	- lo mismo que en la página estática...
	- con la diferencia de que la imagen se actualiza cada 30 segundos

- En la página **JSON de cada cámara** se muestra:
	- los detalles de cada cámara en formato *JSON*

- En la **página de comentario**(que solicita query string) se muestra:
	- Detalles de la cámara sobre la que se hace el comentario
	- imagen de la cámara
	- fecha y hora actual
	- formulario para añadir el comentario

- En la **página de configuración** se muestra:
	- formulario para cambiar el nombre del comentador
	- formulario para cambiar el tamaño y título de la fuente
	- un botón para generar un enlace de autenticación (poniendo dicho enlace en la barra de búsqueda podrás iniciar sesión como estabas registrado)

- En la **página de ayuda** se muestra información sobre el funcionamiento de la aplicación web.

### Elementos generales de todas las páginas HTML

Todas las páginas tienen:

- Una **cabecera** con el título *TeVeO* y el nombre del comentador

- Un **menú** desde el que puedes acceder a las distintas páginas (no aparece la página en la que ya te encuentras)

- Un **pie** que muestra el número de cámaras y comentarios que hay

### Aspecto visual de las páginas

- Se emplea *marcado HTML*

- Se utiliza una hoja de estilo *CSS* para la apariencia del sitio

- Se usa *Bootstrap* para la maquetación de las páginas

### Tests

- **De extremo a extremo** para cada recurso de la práctica

## Lista partes opcionales

- Inclusión de *favicon*
- Inclusión de la imagen del Sitio a la Cabecera
- Permitir "terminar la sesión"
- "Terminar la sesión" pide confirmación adicional
- Permitir votar las cámaras. Mediante *likes*
