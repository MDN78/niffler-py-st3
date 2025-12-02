## Niffler st3

### Предусловие
- собрать проект командой 
```terminaloutput
bash docker-compose-dev.sh
```
- создать тестового пользователя и указать его данные в файле `.env`

Запуск тестов  параллельно 
```commandline
pytest --numprocesses=2
```

### Просмотре отчетов в `Playwright Trace Viewer:`:
- перейти на сайт `https://trace.playwright.dev/`
- скачать отчет по нужному тесту из папки проекта `/tracing`
- загрузить отчет на указанный сайт



#### Notes
debug devtools

```commandline
setTimeout('debugger;', 5_000)
```