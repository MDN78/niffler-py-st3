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
    """Метод формирования системного окружения для отчета allure"""
    # Create list from elements in format: {key}={value}
    items = [f'{key}={value}' for key, value in settings.model_dump().items()]
    # add information about sistem
    items.append(f'os_info={platform.system()} | {platform.release()} | {platform.version()}')
    items.append(f'python_version={sys.version}')

    # Collect all elements to row
    properties = '\n'.join(items)

    # ОOpen file ./allure-results/environment.properties attribute read
    with open(settings.allure_results_dir.joinpath('environment.properties'), 'w+') as file:
        file.write(properties)
