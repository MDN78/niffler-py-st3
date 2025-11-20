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



#### Notes
debug devtools

```commandline
setTimeout('debugger;', 5_000)
```