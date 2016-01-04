# audiowebpagedog
Набор скриптов позволяющий автоматически загружать новые аудио файлы с указанной web-страницы.

Информация о новых загруженных аудиофайлах появляется в области уведомлений.

Настройки программы хранятся в файле базы данных SQLite: **$HOME/.config/audiowebpagedog/audiowebpagedog.db**

## Зависимости
* python3
* python3-notify2

## Использование
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
    page edit <page_url> <subdir>   -- change the page directory
    page remove <page_url>          -- remove the page
    page list                       -- show the page list
```

* сначала проинициализируйте базу данных:
```bash
$ audiowebpagedog_ctl.py init
```

* затем вам необходимо задать путь к каталогу, в который будут сохраняться скачанные аудиофайлы:
```bash
$ audiowebpagedog_ctl.py set download_directory /home/username/your_download_directory
```

* после этого вы можете добавлять страницы, с которых вы хотите загружать аудиофайлы: 
```bash
$ audiowebpagedog_ctl.py page add http://some-web.page/something.rss some-channel-directory
```

**Примечание: аудиофалы будут сохраняться в "/home/username/your_download_directory/some-channel-directory"**

Для запуска процесса загрузки аудиофайлов используйте:
```bash
$ audiowebpagedog_execute.py
```

Для удобства скрипт можно запускать автоматически. Для этого
отредактируйте crontab(crontab -e) приблизительно следующим образом:
```bash
# проверять наличие новых подкастов каждый час
00 * * * * ~/bin/run_script_with_lock-dbus_in_crontab.sh ~/bin/audiowebpagedog/audiowebpagedog_execute.py
# проверить наличие новых подкастов через 600 секунд после включения компьютера
@reboot sleep 600 ; ~/bin/run_script_with_lock-dbus_in_crontab.sh ~/bin/audiowebpagedog/audiowebpagedog_execute.py
```

**run_script_with_lock-dbus_in_crontab.sh решает проблему с отображением уведомлений
на рабочий стол при запуске скрипта из cron. (Подробнее об этом 
можно прочитать по ссылке http://alekseydurachenko.github.io/2015/03/12/python-notify2-crontab.html
а сам скрипт находится по адресу https://gist.github.com/AlekseyDurachenko/2027114608e4863eb038)**
