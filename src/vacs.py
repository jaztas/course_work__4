class VacanciesHH:
    """Класс для создания и работы с объектами вакансиями"""
    all = []

    def __init__(self, name: str, salary: dict, area: str,
                 snippet_req: str,
                 schedule: str,
                 url: str):
        self.name = name
        self.salary = salary
        self.area = area
        self.snippet_req = snippet_req
        self.schedule = schedule
        self.url = url
        self.all.append(self)

    @classmethod
    def init_from_jsonfile(cls, data_vacancies: list):
        """Класс-метод для создания объектов из полученной БД вакансий"""
        cls.all.clear()
        for vacancy in data_vacancies:
            vacancies_list = list(vacancy.values())
            name, salary, area, requirement, schedule, url = vacancies_list
            cls(name, salary, area, requirement, schedule,
                url)

    @staticmethod
    def currency_rate(notruscost: int, currency: str):
        """Статметод для перевода валюты в рубли """
        rate = {"AZN": 0.027728, "BYR": 0.042685, "EUR": 0.015982, "GEL": 0.0344, "KGS": 1.356611, "KZT": 7.809145,
                "RUR": 1, "UAH": 0.596833, "USD": 0.016311, "UZS": 177.916948}
        rus_cost = notruscost / rate[currency]
        return int(rus_cost)

    def conversion_norus_salary(self):
        """Пересчет зарплаты в иностранной валюте в рубли """
        if self.salary:
            if self.salary["currency"] != "RUR":
                if self.salary["from"] and self.salary["to"]:
                    self.salary["from"] = int(
                        self.currency_rate(self.salary["from"], self.salary["currency"]))
                    self.salary["to"] = int(
                        self.currency_rate(self.salary["to"], self.salary["currency"]))
                elif self.salary["from"] is None and self.salary["to"]:
                    self.salary["to"] = int(
                        self.currency_rate(self.salary["to"], self.salary["currency"]))
                elif self.salary["from"] and self.salary["to"] is None:
                    self.salary["from"] = int(
                        self.currency_rate(self.salary["from"], self.salary["currency"]))
            self.salary["currency"] = "RUR"

    def __str__(self):
        """Вывод данных о вакансии в удобном для чтения формате"""
        salary_cost = ""
        if self.salary is None or (self.salary["from"] is None and self.salary["to"] is None):
            salary_cost = "не указана"
        elif self.salary["from"] and self.salary["to"] and self.salary["from"] != self.salary["to"]:
            salary_cost = f'от {self.salary["from"]} до {self.salary["to"]}'
        elif self.salary["from"] and self.salary["to"] is None:
            salary_cost = f'от {self.salary["from"]}'
        elif (self.salary["from"] is None and self.salary["to"]) or self.salary["from"] == self.salary["to"]:
            salary_cost = f'до {self.salary["to"]}'
        return (
            f'Название вакансии: {self.name}, город: {self.area}, режим работы: {self.schedule}, \n'
            f'требования: {self.snippet_req}, \n'
            f'cсылка на вакансию: {self.url}\n'
            f'зарплата: {salary_cost} {self.salary["currency"]}\n******************************')

    def __repr__(self):
        """Информация об объекте класса в режиме отладки"""
        return f"{self.__class__.__name__}: {self.name}, {self.url}"

    def uniform_salary(self):
        """Приведение данных о зарплате к удобному виду для сортировки и фильтрации"""
        if self.salary["from"] is None and self.salary["to"]:
            self.salary["from"] = int(self.salary["to"])
        if self.salary["from"] and self.salary["to"] is None:
            self.salary["to"] = int(self.salary["from"])

    def __len__(self):
        """Применение функции len к объектам класса"""
        return len(self.all)
