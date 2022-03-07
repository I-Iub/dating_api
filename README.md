## Примеры запросов к API
#### Зарегистрировать нового пользователя
Отправить POST-запрос на эндпоинт `http://<domain>/api/clients/create/`.
В запросе передать:
```
{
    "avatar": "data:image/png;base64, ... ",    # картинка должна передаваться в base64
    "gender": "Male",                           # выбрать из вариантов: "Male", "Female"
    "first_name": "<first_name>",
    "last_name": "<last_name>",
    "email": "<email>",
    "password": "<password>"
}
```
#### Получить токен
Отправить POST-запрос (Content-Type: application/json) на эндпоинт `http://<domain>/api/clients/login/`.
В запросе передать:
```
{
    "email": "<email>",
    "password": "<password>"
}
```
В ответ вернётся токен:
```
{
  "token": "<token>"
}
```
#### Удалить токен
Для разлогинивания авторизованный пользователь должен передать POST-запрос на эндпоинт `http://<domain>/api/clients/logout/`.
При этом необходимо передать токен в формате `Authorization: Token <token083fd1627023118ee8f5b344850ftoken>`.
