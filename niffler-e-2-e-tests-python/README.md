## Niffler st3

### Предусловие

- собрать проект командой

```terminaloutput
bash docker-compose-dev.sh
```

- создать тестового пользователя и указать его данные в файле `.env`
  Пример тестового пользователя:

```dotenv
TEST_USERNAME=niffler_11St
TEST_PASSWORD=QEwdr!ss2f
```

#### Запуск тестов:

- стандартный запуск:

```commandline
pytest
```

- параллельно

```commandline
pytest --numprocesses=2
```

- в `heahed` режиме

```commandline
pytest --headed
```

#### Просмотр allure отчета

```commandline
allure serve
```
Для отображения запросов/ответов в отчетах Allure используются колоризированные шаблоны из папки `resources`
- применяется библиотека `jinja2`



Сохраненные логи прогона тестов доступны в файле `log.txt` который будет сформирован в корне проекта после завершения
тестов

### Просмотр отчетов в `Playwright Trace Viewer:`:

- скачать отчет по нужному тесту из папки проекта `/tracing`
- перейти на сайт `https://trace.playwright.dev/`
- загрузить отчет на указанный сайт

#### Notes

debug devtools

```commandline
setTimeout('debugger;', 5_000)
```

Завершить процессы postgres для освобождения порта - команда терминала:

```commandline
sudo pkill -9 postgres
```