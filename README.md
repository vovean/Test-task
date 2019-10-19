# Описание
### О решении
Для API используется REST Framework.  
Чтобы упростить код многие view сделаны используя REST Framework Generic Views.  
Лонг поллинг реализован так: в момент обращения на `/api/task/<id>/change_status` в отдельном классе в 
переменную-флаг устанавливается `True`, это показывает что есть изменения, о которых нужно сообщить клиенту. Тогда, при следующем обращении клиента на `/api/listen_to_updates` вернется 
json-объект с данными об изменении, и переменная-флаг снова установится в значение `False`. Если клиент обратится 
на `/api/listen_to_updates` когда изменений нет, то откроется соединение, и сервер будет его поддерживать до того, как 
произойдут изменения, о которых нужно сообщить клиету.  
Для успешной работы с таким решением на клиенте должен быть запущен код вроде 
```js
let update = await fetch(window.location.protocol + '//' + window.location.host + '/api/listen_to_updates');
```
### Используемые технологии
 - Django 2.2.6
 - REST Framework 3.10.3

# Запуск
1) `python -m venv venv_folder`
2) `. venv_folder/bin/activate`
3) `pip install -r requirements.txt`
4) `python manage.py makemigrations`
5) `python manage.py migrate`
6) `python manage.py runserver`