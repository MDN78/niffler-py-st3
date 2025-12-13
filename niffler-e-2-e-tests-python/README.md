## Niffler st3

### Предусловие

- собрать проект командой

```terminaloutput
bash docker-compose-dev.sh
```

- создать тестового пользователя и указать его данные в файле `.env`
Пример тестовго пользователя:
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