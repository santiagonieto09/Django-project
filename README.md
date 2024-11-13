# Proyecto Django

Este es un proyecto Django que te guía a través de los pasos básicos para ejecutar la aplicación Django.

## Requisitos previos

- Python 3.9 o superior
- Django 4.2

## Instalación 🔄

1. Navega al directorio del proyecto:
   ```
   cd ruta/al/directorio/del/proyecto
   ```

2. Instala Django:
   ```
   pip install django==4.2
   ```

3. Crea y activa un entorno virtual (opcional pero recomendado):
   ```
   python -m venv venv
   ```
   En Windows:
   ``` 
   venv\Scripts\activate  
   ```
   En Linux o macOS:
   ```
   source venv/bin/activate  
   ```
## Configuración ⚙️

1. Realiza las migraciones:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

2. Crea un superusuario (si necesitas acceder al panel de administración de Django):
   ```
   python manage.py createsuperuser
   ```

## Ejecución 🚀

1. Corre el servidor de desarrollo:
   ```
   python manage.py runserver
   ```

2. Accede a la aplicación en `http://127.0.0.1:8000/` 👈

¡Listo! Ahora puedes probar tu aplicación Django. ✔️
