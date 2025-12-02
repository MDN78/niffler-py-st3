
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import DirectoryPath
from typing import Self
import platform
import sys



class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra='allow')
    allure_results_dir: DirectoryPath

    @classmethod
    def initialize(cls) -> Self:
        allure_results_dir = DirectoryPath("./allure-results")
        allure_results_dir.mkdir(exist_ok=True)

        return Settings(allure_results_dir=allure_results_dir)

settings = Settings.initialize()


def create_allure_environment_file():
    # Создаем список из элементов в формате {key}={value}
    items = [f'{key}={value}' for key, value in settings.model_dump().items()]
    # add information about sistem
    items.append(f'os_info={platform.system()} | {platform.release()} | {platform.version()}')
    items.append(f'python_version={sys.version}')

    # Собираем все элементы в единую строку с переносами
    properties = '\n'.join(items)

    # Открываем файл ./allure-results/environment.properties на чтение
    with open(settings.allure_results_dir.joinpath('environment.properties'), 'w+') as file:
        file.write(properties)  # Записываем переменные в файл