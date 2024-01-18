# 02-DigiCore

## Integrantes

Este es el repositorio de ***DigiCore***, compuesto por:

<ins>**Scrum Master**</ins>

- Rodrigo Ramírez, 202004579-8

<ins>**Product Owner**</ins>

- Sebastián Salgado, 201951563-2

<ins>**Desarrolladores**</ins>

- Diego Acevedo, 202073532-8
- Martín Moraga, 202004599-2
- Florencia Ramírez, 202073522-0
- Francisca Romero, 202004511-9

## Task Board
Con el siguiente enlace puede ingresar a la organización del equipo [enlace](https://trello.com/invite/b/5YLIHOAE/ATTI59ebeb755591266b79c444cdbb7308e15C014D55/digicore)
## Wiki

Se puede acceder a la Wiki con el siguiente [enlace](https://github.com/INF225-2023-2-P201/02-digicore/wiki)

## Hitos

- [Hito 1](https://github.com/INF225-2023-2-P201/02-digicore/wiki#hito-1)
- [Hito 2](https://github.com/INF225-2023-2-P201/02-digicore/wiki#hito-2)
- [Hito 3](https://github.com/INF225-2023-2-P201/02-digicore/wiki#hito-3)
- [Hito 4](https://github.com/INF225-2023-2-P201/02-digicore/wiki#hito-4)
- [Hito 5](https://github.com/INF225-2023-2-P201/02-digicore/wiki#hito-5)
- [Hito 6](https://github.com/INF225-2023-2-P201/02-digicore/wiki#hito-6)
- [Hito 7](https://github.com/INF225-2023-2-P201/02-digicore/wiki#hito-7)

## Forma de ejecutar

Se recomiendan las siguientes versiones:
- Python: 3.11
- Xampp: 8.2.4
- Node: 16 o superior

En la Carpeta donde almacene la app, debe dirigirse a una terminal cmd, debe ejecutar el comando: 
    
```
pip install virtualenv
```

Debe tener previamente instalado el pip.

Luego en debe crear un entorno virtual con el siguiente comando:

```
virtualenv env
```

Se creará una carpeta env, luego debe ejecutar el siguiente archivo para activar el entorno:

```
.\env\Scripts\activate
```

Debería aparterecer un "(env)" antes de la dirección de su terminal, eso significa que vamos bien, luego debe dirigirse a la carpeta DigiCore_API y ejecutar el siguiente comando:

```
pip install -r requirements.txt
```

Se instalará todos los módulos necesarios. En paralelo debemos abrir Xampp Control y levantar MySql y Apache, abrir phpMyAdmin en el navedagor y crear una nueva base de datos con el nombre digicore_db.

Luego debe migrar el contenido de manage.py con el siguiente comando:

```
python manage.py migrate
```

Luego debemos crear un super usario, con el siguiente comando:

```
python manage.py createsuperuser 
```

Deberá ingresar un nombre de usuario, una direccion de correo electronico y su contraseña.

Con el super usuario creado, debe levantar el servidor con el siguiente comando:

```
python manage.py runserver
```

Ya estaría listo nuestro Backend.

Ahora nos podemos dirigir a la siguiente dirección http://127.0.0.1:8000/admin/, donde nos pediran nuestro super usuario creado previamente, aquí en el apartado API, nos dirigimos a Settings logs, luego en settingsLog object y aquí es donde podemos agregar más input y output a nuestra base de datos.

Dentro de phpMyAdmin, en la base de datos digicore_db, en la tabla "api_settingslog" se encuentran los inputs y outputs correspondientes.
