import pytest

from src.vacs_api import HeadHunterAPI

hh_api = HeadHunterAPI()


def test_get_areas():
    assert hh_api.get_areas("Москва") == "1"


def test_get_vacancies():
    assert hh_api.get_vacancies("", False, None)
    assert hh_api.get_vacancies("Python, разработчик", True, "1")
