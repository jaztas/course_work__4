import json
from abc import ABC, abstractmethod


class DataVacancies(ABC):
    """Абстрактный класс для работы с БД вакансий"""

    @abstractmethod
    def save_vacancies(self, *args, **kwargs):
        """Сохранение данных"""
        pass

    @abstractmethod
    def selection_vacancies(self, *args, **kwargs):
        """Выборка данных"""
        pass

    @abstractmethod
    def delete_vacancies(self, *args, **kwargs):
        """Удаление данных"""
        pass


class DataVacanciesJson(DataVacancies):
    """Класс для работы с файлами json, наследуется от абстрактного класса DataVacancies"""
    json_file = "../data/vacancies_hh.json"

    def save_vacancies(self, data_json):
        """ Сохранение данных в файл json"""
        with open(self.json_file, 'w+', encoding='utf-8') as file:
            json.dump(data_json, file, ensure_ascii=False)

    def read_from_json(self):
        """Чтение данных из файла json"""
        try:
            open(self.json_file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {self.json_file} не найден")
        else:
            with open(self.json_file, "r+", encoding='utf-8') as file:
                return json.load(file)

    def selection_vacancies(self, data_from_file):
        """Выборка данных из файла json"""
        selection_vacancies_list = []
        for vacancy in data_from_file:
            name = vacancy["name"]
            area = vacancy["area"]["name"]
            url = vacancy["url"]
            snippet_req = vacancy["snippet"]["requirement"]
            schedule = vacancy["schedule"]["name"]
            salary = vacancy["salary"]
            vacancy_info = {
                "name": name,
                "salary": salary,
                "area": area,
                "snippet_req": snippet_req,
                "schedule": schedule,
                "url": url
            }
            selection_vacancies_list.append(vacancy_info)
        return selection_vacancies_list

    def delete_vacancies(self):
        """Удаление данных из файла json"""
        try:
            open(self.json_file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {self.json_file} не найден")
        else:
            open(self.json_file, "w").close()
