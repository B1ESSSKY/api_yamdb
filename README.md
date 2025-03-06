# API YaMDb
## Запуск проекта
1. Клонируем репозиторий  
```  
git clone git@github.com:TheQChan/api_final_yatube.git  
```
2. Переходим в папку, создаем и активируем виртуальное окружение
```  
python -m venv venv
```
```  
source venv/Scripts/activate
```
3. Обновляем pip и устанавливаем зависимости
```  
python -m pip install --upgrade pip
```
```  
pip install -r requirements.txt
```
4. Выполнение миграций
```  
python manage.py migrate
```
5. Запуск проекта
```  
python manage.py runserver
```