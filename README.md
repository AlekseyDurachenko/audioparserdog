# audiowebpagedog
Инструмент для автоматической загрузки свежих аудиозаписей с указанной веб страницы

Установка и запуск
------------------
Для работы с утилитой вам потребуется установить python3 а так же 
модуль python3-nofity2. Установка в дистрибутивах debian/ubuntu
будет выглядеть следующим образом:

```bash
sudo apt-get install python3 python3-notify2
```

Как пользоваться?
-----------------
```bash
$ audiowebpagedog_ctl.py
=== audio web page control v.0.1.0 ===
Usage:
    audiowebpagedog_ctl.py <command> <arg1> ... <argN>
Command details:
    init                            -- init the database
    set download_directory <path>   -- set the download directory
    get download_directory          -- show the download directory
    page add <page_url> <subdir>    -- add the page
    page edit <page_url> <subdir>   -- add the page
    page remove <page_url>          -- remove the page
    page list                       -- show the page list
```

Перед началом работы вам необходимо задать путь к каталогу, в который будут
сохраняться скаченные аудиофайлы. Для этого выполните следующую команду:
```bash
$ audiowebpagedog_ctl.py set download_directory /home/username/your_download_directory
```

После этого вам потребуется добавить стринцы, которые вы хотите автоматически загружать,
следующей командой: 
```bash
$ audiowebpagedog_ctl.py page add http://some-web.page/something.rss some-channel-directory
```

В результате все аудиофайлы с данной страницы будут загружены в
/home/username/your_download_directory/some-directory

Файл настроек представляет из себя файл базы данных SQLite, который располагается по
адресу ~/.config/audiowebpagedog/audiowebpagedog.db

Для запуска загрузки новых аудиофайлов необходимо запустить скрипт 
audiowebpagedog_execute.pyбез параметров.

Так же этот скрипт можно запускать по расписанию с помощью cron. Для этого выполните
команду 
```bash
$ crontab -e
```

И пропишите приблизительно следующее:
```bash
00 * * * * ~/bin/run_script_with_lock-dbus_in_crontab.sh ~/bin/audiowebpagedog/audiowebpagedog_execute.py
@reboot sleep 600 ; ~/bin/run_script_with_lock-dbus_in_crontab.sh ~/bin/audiowebpagedog/audiowebpagedog_execute.py
```
Согласно этим правилам проверка свежих аудиофайлов будет производиться 
каждый час, а так же через 10 минут после включения компьютера.

run_script_with_lock-dbus_in_crontab.sh решает проблему с отображением уведомлений
на рабочий стол при запуске скрипта из cron. Подробнее об этом 
можно прочитать по ссылке http://alekseydurachenko.github.io/2015/03/12/python-notify2-crontab.html
а сам скрипт находится по адресу https://gist.github.com/AlekseyDurachenko/2027114608e4863eb038
