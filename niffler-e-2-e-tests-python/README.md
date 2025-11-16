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