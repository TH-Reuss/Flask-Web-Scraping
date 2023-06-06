## Consideraciones

Se limitó la cantidad de productos que se pueden obtener desde Falabella. Tiene un máximo de 600 productos

### Implementacion

Integración continua
Asincronismo en las funciones para reducir los tiempos de carga

### Funciones a implementar

1.- Proximamente se debe implementar una funcion que permita recibir una lista de busqueda, de tal forma de aumentar la escalabilidad del proyecto
2.- Transformar las clases en modulos de python instalables desde pip
3.-Utilizar async with en lugar de requests para hacer solicitudes síncronas: Como el código utiliza aiohttp para realizar solicitudes asíncronas, es recomendable utilizar también aiohttp para las solicitudes síncronas, en lugar de requests.
4.- Agregar más tiendas en las cuales buscar productos
5.- Crea una clase padre de Scraping y subclases para cada tienda
6.- Que indique cuando no se encontraron productos
7.- Crear mantenedor de usuarios para generar alertas de seguimiento

### Errores

1.- Al buscar los productos "cama" y "tv" arroja un error, se cree que es debido a que el template que renderiza falabella es distinto para estos productos

### AWS

El proyecto fue montado en una instancia ec2 a través de AWS Elastic Beanstalk. Para actualizarlo estoy utilizando la herramienta de integracion continua de AWS CodePipeline donde se canaliza mi repositorio en github
