# Pasos para correr la API djangorestframework
1. Clonar el repositorio
```git clone https://github.com/ferjovel06/api-unan.git```
```cd api-unan```
2. Crear un entorno virtual
```python -m venv env``` \
En Windows\
```env\Scripts\activate``` \
En Linux \
```source env/bin/activate```
3. Instalar las dependencias
```pip install -r requirements.txt```
4. Correr el servidor
```python manage.py runserver```
5. Probar la API
```http://localhost:8000/api/```

## Documentación de la API
```http://localhost:8000/swagger/```

### Pasos para autenticarse en swagger
1. Crear un superusuario
```python manage.py createsuperuser```
2. Correr el servidor
```python manage.py runserver```
3. Ingresar a la URL
```http://localhost:8000/swagger/```
4. En el endpoint "Token" dar click en "Try it out"
5. Ingresar las credenciales del superusuario
6. Copiar el token generado
7. En la parte superior derecha dar click en "Authorize"
8. En la sección "Bearer" pegar el token copiado con el prefijo "Bearer"\
    Ejemplo:
```Bearer <token>```
9. Dar click en "Authorize"