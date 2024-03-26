from src.vacs import VacanciesHH
from src.vacs_api import HeadHunterAPI
from src.vacs_data import DataVacanciesJson


def user_interaction():
	"""Метод для работы с пользователем"""
	print("Здравствуйте! Добро пожаловать в сервис поиска вакансий на сайте hh.ru")
	print("Укажите параметры фильтрации для поиска вакансий")
	print("Если фильтрация не требуется нажимайте Enter без заполнения")

	"""Сбор данных для фильтрации при поиске вакансий на сайте hh.ru"""
	params_vacancy = str(input(
		f"Перечислите через запятую ключевые слова по вакансии: \n"
		f"(например: разработчик, тестирование, python; "
		f"поиск по ключевым словам выполняется в названии, описании вакансии и в требованиях к вакансии)\n"))

	select_area = input(
		f"По какому городу выполнить поиск? \n"
		f"(поиск можно выполнить по городам России, Белоруссии, Азербайджана, "
		f"Казахстана, Киргизии, Грузии, Узбекистана, Украины): \n")

	only_with_salary = input("Искать вакансии только с указанием зарплаты? (да/нет или y/n): \n")
	print("******************************")
	if only_with_salary.lower() == "y" or only_with_salary.lower() == "да":
		only_with_salary = True
	elif only_with_salary.lower() == "n" or only_with_salary.lower() == "нет" or only_with_salary == "":
		only_with_salary = False

	"""Создание экземпляра класса для работы с API сайта hh.ru"""
	hh_api = HeadHunterAPI()
	"""Получение id региона с hh.ru в формате JSON"""
	id_area = hh_api.get_areas(select_area.capitalize())
	"""Получение вакансий с hh.ru в формате JSON"""
	hh_vacancies = hh_api.get_vacancies(params_vacancy, only_with_salary, id_area)
	"""Создание экземпляра класса для работы с БД вакансий в виде json-файла"""
	data_vacancies = DataVacanciesJson()
	"""Сохранение данных, полученных с сайта hh.ru в json-файл"""
	data_vacancies.save_vacancies(hh_vacancies)
	"""Чтение данных из json-файла"""
	data_from_file = data_vacancies.read_from_json()
	"""Выборка набора данных по вакансиям, полученных из json-файла"""
	select_vacancies = data_vacancies.selection_vacancies(data_from_file)
	"""Преобразование набора данных из JSON в список объектов"""
	VacanciesHH.init_from_jsonfile(select_vacancies)
	print(f'С сайта получено {len(VacanciesHH.all)} вакансий')

	if only_with_salary:
		print("Хотите получить ТОП самых высокооплачиваемых вакансий по выбранным параметрам?")
		print(
			f"******************************\n"
			f"Внимание! При формировании ТОП самых высокооплачиваемых вакансий "
			f"зарплата будет пересчитана в рубли по текущему курсу\n"
			f"******************************")
		if len(VacanciesHH.all) >= 20:
			in_top = 20
		else:
			in_top = len(VacanciesHH.all)
		top_vacancies = input(f"Укажите количество - не более {in_top} или пропустите заполнение: \n")
		print("******************************")
		"""Вывод ТОП вакансий"""
		if top_vacancies:
			top_vacancies = int(top_vacancies)
			if len(VacanciesHH.all) == 1:
				print(f"Найдена всего одна вакансия: \n{str(VacanciesHH.all[0])}")
			elif int(top_vacancies) > 1 and int(top_vacancies) <= 20 and int(top_vacancies) <= len(VacanciesHH.all):
				for i in range(int(top_vacancies)):
					for vac in VacanciesHH.all:
						"""Унифицированный вид и перевод в рубли"""
						VacanciesHH.uniform_salary(vac)
						VacanciesHH.conversion_norus_salary(vac)
					VacanciesHH.all.sort(key=lambda x: x.salary["to"], reverse=True)
					print(str(VacanciesHH.all[i]))
		else:
			for vac in VacanciesHH.all:
				print(str(vac))
	elif not only_with_salary:
		currency_salary = input("Пересчитывать зарплату в рубли, если указана в другой валюте? (да/нет или y/n): ")
		print("******************************")
		if currency_salary.lower() == "y" or currency_salary.lower() == "да":
			for vac in VacanciesHH.all:
				"""Перевод в рубли"""
				VacanciesHH.conversion_norus_salary(vac)
				print(str(vac))
		elif currency_salary.lower() == "n" or currency_salary.lower() == "нет" or currency_salary == "":
			for vac in VacanciesHH.all:
				print(str(vac))
	print("Выполнено!")

	"""Очищение файла"""
	data_vacancies.delete_vacancies()
