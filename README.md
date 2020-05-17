# Создание файлов трек-логов для каждого маршрута из базы данных

- Python 2.7 (Python >= 3 не поддерживается СУБД)
- СУБД: Advantage Database Sever 11
- Сервер мониторинга передвижения транспорта: PCN 8 (Ritm)

## Запуск
`python.exe main.py --date=20200517 --offset=0 --save=..\tracks --type=plt --tspsw=password --dbpsw=password --update=y`

* `--date=20200517`   - дата (по умолчанию текущая дата)
* `--offset=0 `       - смещение дней (по умолчанию 0)
* `--save=..\tracks`  - папка для сохранения треков (по умолчанию в ..\tmp\tracks)
* `--type=plt`        - тип трека (plt/json, plt - по умолчанию)
* `--tspsw=password`  - пароль доступа к серверу треков
* `--dbpsw=password`  - пароль доступа к БД 
* `--update=y`        - установить отметку в БД о том, что для маршрута сформирован файл трек-лога (`y` - обновлять, если не указать, то обновляться не будет)