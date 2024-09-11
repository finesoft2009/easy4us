# easy4us  

`easy4us` - это Python-утилита для декодирования ionCube PHP файлов с использованием сайта **easytoyou.eu**. Этот инструмент автоматизирует процесс логина, загрузки и скачивания файлов с декодером easytoyou.eu.  

Структура проекта:
easy4us/  
│  
├── easy4us/  
│   ├── __init__.py  
│   ├── auth.py  
│   ├── decoder.py  
│   ├── utils.py  
│  
├── main.py  
│  
├── README.md  


## Возможности  

- Автоматический вход на сайт easytoyou.eu  
- Загрузка ionCube PHP файлов для декодирования  
- Скачивание декодированных файлов  
- Получение информации о членстве в аккаунте  

## Установка  

Клонируйте репозиторий:  

```bash  
git clone https://github.com/ваш-никнейм/easy4us.git  
cd easy4us  
Установите зависимости:

pip install -r requirements.txt  
Использование
python3 main.py -u ИМЯ_ПОЛЬЗОВАТЕЛЯ -p ПАРОЛЬ -s ИСТОЧНИК -o НАЗНАЧЕНИЕ -d ДЕКОДЕР -w --account  
Аргументы
-u, --username: имя пользователя на easytoyou.eu (обязательно)
-p, --password: пароль на easytoyou.eu (обязательно)
-s, --source: исходный каталог, содержащий PHP файлы (обязательно)
-o, --destination: каталог назначения для сохранения декодированных файлов (по умолчанию: <source>_decoded)
-d, --decoder: тип декодера (по умолчанию: ic11php72)
-w, --overwrite: перезаписывать существующие файлы
--account: получить и показать информацию о членстве в аккаунте
Пример
python3 main.py -u dj_bit -p 789852 -s /1/dec.php -o /2/dec.php -d ic11php70 -w --account
Лицензия
Этот проект лицензируется под лицензией MIT. См. файл LICENSE для получения подробной информации.
=======
# easy4us
/easy4us.git
>>>>>>> 3dccd4c975de6bfc2b992368d2e3dd4cf9b7ce90
