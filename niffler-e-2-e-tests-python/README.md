## Проект автоматизированного тестирования приложения Niffler (V3).

<p style="text-align: center;">
  <code>
    <img width="65%" title="main_page" src="assets/niffler_main.png">
  </code>
</p>


### Проект реализован с использованием:

<div class="tech-icons">
  <img style="width: 45px; height: 45px;" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" alt="Python">
  <img style="width: 45px; height: 45px;" src="https://github.com/MDN78/MDN78/blob/main/assets/playwright_2.png">
  <img style="width: 45px; height: 45px;" src="https://github.com/MDN78/MDN78/blob/main/assets/pytest.png" alt="Pytest">
  <img style="width: 45px; height: 45px;" src="https://github.com/MDN78/MDN78/blob/main/assets/allure_report.png" alt="Allure Report">
  <img style="width: 45px; height: 45px;" src="https://github.com/MDN78/MDN78/blob/main/assets/github.png" alt="GitHub">
  <img style="width: 45px; height: 45px;" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/pycharm/pycharm-original.svg" alt="PyCharm">
  <img style="width: 45px; height: 45px;" src="assets/Requests_Logo.png" alt="Requests">
  <img style="width: 45px; height: 45px;" src="assets/kafka.svg" alt="Apache Kafka">
  <img style="width: 45px; height: 45px;" src="assets/Git.svg" alt="Git">
  <img style="width: 45px; height: 45px;" src="assets/PostgresSQL.svg" alt="PostgreSQL">
  <img style="width: 65px; height: 45px;" src="assets/soap.png" alt="PostgreSQL">
</div>


### Особенности проекта:

* Созданы UI тесты с использованием PageObject и ООП на фреймворке `Playwright`
* Созданы UI тесты + DB с использованием передачи данных REST API
* Созданы тесты проверяющие передачу данных REST API + DB
* Созданы Е2Е тесты проверяющие очередь событий KAFKA -> DB -> API
* Созданы SOAP тесты проверяющие тестового пользователя
* Для создания отчетов тестирования применен Allure Reports
* Для повышения читаемости отчетов тестирования используется шаблонизатор `Jinja2`
* Для валидации и трансформации данных используется библиотека `Pydantic`
* Для запуска тестов и управлением тестовыми данными созданы специальные фикстуры
* Для управления и взаимодействия с БД используется `SQLAlchemy`

### Предусловие - сборка и установка проекта

- Скопировать проект на локальную машину
- Запустить desktop версию `Docker` локально на компьютере
- Запустить `Niffler` согласно README основного проекта. 
- ВАЖНО! Установить Java версии 21. Это необходимо, т.к. проект использует синтаксис Java 21
- Настроить виртуальное окружение проекта

```commandline
python -m venv .venv
source .venv/bin/activate
```

- Установить зависимости проекта из файла при помощи `Poetry`
- В соответствии с инструкцией установить Allure [https://allurereport.org/docs/install/](https://allurereport.org/docs/install/)
- Запустить приложение `Niffler` командой через `bash` терминал:

```commandline
bash docker-compose-dev.sh
```

### Локальный запуск тестов
- Создать тестового пользователя с логином паролем, например:
```dotenv
TEST_USERNAME=niffler_11St
TEST_PASSWORD=QEwdr!ss2f
```
- Создать и заполнить `.env` в соответствии с примером, добавив созданного тестового пользователя
- Открыть в браузере приложение `Niffler`  - [http://frontend.niffler.dc/](http://frontend.niffler.dc/)
- Зарегистрировать в приложении созданного тестового пользователя
- Запустить тесты командой:

```commandline
pytest
```



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