import asyncio
import locale
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from time import sleep
import xmltodict, json
from lxml import html

import pyppeteer
from requests import session
from requests_html import HTMLSession, AsyncHTMLSession, HTML
from soupsieve import select

from customers.models import UserSearch
from job.models import RawVacancy, Vacancy
from job.utils import search_for_skills


class DjinniParser:
    base_url = 'https://djinni.co'
    detail_urls = []
    vacancy_count = None

    def prepare_vacancies_url(self, user_search: UserSearch):
        mapper = {
            'primary_keyword': user_search.programming_language,
            'salary': user_search.salary,
            'region': user_search.location,
            'employment': 'remote' if user_search.is_remote else None,
            'keywords': user_search.level_need,
            'exp_level': f'{user_search.years_need}y',
            'english_level': user_search.english_lvl,
        }
        query_params = '/jobs/rss/?'
        for key, value in mapper.items():
            if value:
                query_params += f'{key}={value}&'
        url = f'{self.base_url}{query_params}'
        return url

    @staticmethod
    def parse_detail_urls(vacancies_url):
        with HTMLSession() as session:
            response = session.get(url=vacancies_url)
            page_dict = xmltodict.parse(response.content)
            vacancies = page_dict.get('rss', {}).get('channel', {}).get('item', [])
            urls = [vac.get('link') for vac in vacancies]
        return urls

    @staticmethod
    def save_raw_vacancy(url):
        with HTMLSession() as session:
            response = session.get(url=url)
            sleep(5)
        if not RawVacancy.objects.filter(url=url).exists():
            obj = RawVacancy.objects.create(
                url=url,
                data=response.html.html,
                source='Djinni',
            )
            print(f'**** SAVE Djinni: {url}')

    def urls_generator(self):
        for url in self.detail_urls:
            yield url

    @staticmethod
    def extract_salary(table_block):
        salary_min = None
        salary_max = None
        for li in table_block:
            if '$' in li.text_content():
                salary_values = li.text_content().replace('$', '').split('-')
                if len(salary_values) == 1:
                    salary_min = salary_values[0].strip()
                    salary_max = salary_values[0].strip()
                elif len(salary_values) > 1:
                    salary_min = salary_values[0].strip()
                    salary_max = salary_values[-1].strip()
        try:
            return int(salary_min.strip()), int(salary_max.strip())
        except:
            return None, None

    @staticmethod
    def extract_location(table_block):
        location = None
        for li in table_block:
            if 'Офіс:' in li.text_content():
                location = li.text_content().replace('Офіс: ', '').replace('\n', ' ').strip()
        try:
            return location
        except:
            return None

    @staticmethod
    def extract_remote(table_block):
        remote = False
        for li in table_block:
            if 'віддалено' in li.text_content().lower():
                remote = True
        try:
            return remote
        except:
            return False

    def save_vacancy(self, raw_vacancy: RawVacancy):
        html_page = html.fromstring(raw_vacancy.data)
        try:
            description = html_page.xpath("//div[@class='col-sm-8 row-mobile-order-2']")[0].text_content()
        except Exception as e:
            description = None
        try:
            programming_language = html_page.xpath("//ul[@id='job_extra_info']/li[@class='mb-1'][1]/div[@class='row']/div[@class='col pl-2']")[0].text_content()
        except Exception as e:
            programming_language = None
        try:
            table_top_block = html_page.xpath("//strong")
            table_bot_block = html_page.xpath("//div[@class='col pl-2']")
        except Exception as e:
            table_top_block = None
            table_bot_block = None
        try:
            salary_min, salary_max = self.extract_salary(table_top_block)
        except Exception as e:
            salary_min, salary_max = None, None
        try:
            location = self.extract_location(table_bot_block)
        except Exception as e:
            location = None
        try:
            is_remote = self.extract_remote(table_top_block)
        except Exception as e:
            is_remote = None
        try:
            skills = search_for_skills(description)
        except Exception as e:
            skills = None
        try:
            Vacancy.objects.create(
                source=raw_vacancy.source,
                url=raw_vacancy.url,
                raw_data=raw_vacancy,
                description=description,
                programming_language=programming_language,
                salary_min=salary_min,
                salary_max=salary_max,
                location=location,
                is_remote=is_remote,
                skills=skills,
            )
            raw_vacancy.is_processed = True
            raw_vacancy.save()
        except Exception as e:
            print(f'Djinni Url: {raw_vacancy.url} not saving.\nError: {e}')


    def run(self, user_search: UserSearch):
        vacancies_url = self.prepare_vacancies_url(user_search)
        self.detail_urls = self.parse_detail_urls(vacancies_url)

        try:
            urls_gen = self.urls_generator()
            with ThreadPoolExecutor(max_workers=2) as executor:
                executor.map(self.save_raw_vacancy, urls_gen)
        except Exception as e:
            print(e)



class DouParser:
    base_url = 'https://jobs.dou.ua'
    detail_urls = []

    def prepare_vacancies_url(self, user_search: UserSearch):
        mapper = {
            'category': user_search.programming_language,
            'city': user_search.location,
            'remote': 'remote' if user_search.is_remote and not user_search.location else None,
            'search': user_search.level_need,
            'exp': self.conversion_years(user_search.years_need) if user_search.years_need else None,
        }
        query_params = '/vacancies/feeds/?'
        for key, value in mapper.items():
            if value:
                query_params += f'{key}={value}&'
        url = f'{self.base_url}{query_params}'
        return url

    @staticmethod
    def conversion_years(years_need):
        if years_need <= 1:
            return '0-1'
        elif years_need <= 3:
            return '1-3'
        elif years_need <= 5:
            return '3-5'
        elif years_need > 5:
            return '5plus'

    @staticmethod
    def parse_detail_urls(vacancies_url):
        with HTMLSession() as session:
            response = session.get(url=vacancies_url)
            page_dict = xmltodict.parse(response.content)
            vacancies = page_dict.get('rss', {}).get('channel', {}).get('item', [])
            urls = [vac.get('link') for vac in vacancies]
        return urls

    @staticmethod
    def extract_salary(salary_string):
        salary_min = None
        salary_max = None
        salary_values = salary_string.replace('$', '').split('-')
        if len(salary_values) == 1:
            salary_min = salary_values[0].strip()
            salary_max = salary_values[0].strip()
        elif len(salary_values) > 1:
            salary_min = salary_values[0].strip()
            salary_max = salary_values[-1].strip()
        try:
            return int(salary_min.strip()), int(salary_max.strip())
        except:
            return None, None

    @staticmethod
    def extract_created_date(raw_string):
        try:
            years_string = ['2023', '2024', '2025']
            created_date_raw = raw_string.replace('\n', '').strip()
            year_end_index = 0
            for year in years_string:
                check_index = created_date_raw.find(year)
                year_end_index = check_index + 4 if check_index >= 0 else year_end_index
            created_date = created_date_raw[0:year_end_index]
            return created_date
        except:
            return None

    @staticmethod
    def save_raw_vacancy(url):
        with HTMLSession() as session:
            response = session.get(url=url)
            sleep(5)
        if not RawVacancy.objects.filter(url=url).exists():
            obj = RawVacancy.objects.create(
                url=url,
                data=response.html.html,
                source='DOU',
            )
            print(f'**** SAVE Dou: {url}')

    def save_vacancy(self, raw_vacancy: RawVacancy):
        html_page = html.fromstring(raw_vacancy.data)
        try:
            programming_language = html_page.xpath("//li[@class='breadcrumbs']/a[2]")[0].text_content()
        except Exception as e:
            programming_language = None
        try:
            description = html_page.xpath("//div[@class='l-vacancy']/div[@class='b-typo vacancy-section']")[0].text_content()
        except Exception as e:
            description = None
        try:
            place = html_page.xpath("//li[@class='breadcrumbs']/a[3]")[0].text_content()
            location = place if place != 'віддалено' else None
            is_remote = True if place == 'віддалено' else False
        except Exception as e:
            location = None
            is_remote = None
        try:
            salary = html_page.xpath("//span[@class='salary']")[0].text_content().strip()
            salary_min, salary_max = self.extract_salary(salary)
        except Exception as e:
            salary_min, salary_max = None, None
        try:
            skills = search_for_skills(description)
        except Exception as e:
            skills = None
        try:
            created_data_raw = html_page.xpath("//div[@class='date']")[0].text_content().strip()
            created_data_string = self.extract_created_date(created_data_raw)
            locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8')
            created_data = datetime.strptime(created_data_string, "%d %B %Y").date()
        except Exception as e:
            created_data = None

        try:
            Vacancy.objects.create(
                source=raw_vacancy.source,
                url=raw_vacancy.url,
                raw_data=raw_vacancy,
                description=description,
                programming_language=programming_language,
                salary_min=salary_min,
                salary_max=salary_max,
                location=location,
                is_remote=is_remote,
                skills=skills,
                created_data=created_data,
            )
            raw_vacancy.is_processed = True
            raw_vacancy.save()
        except Exception as e:
            print(f'Dou Url: {raw_vacancy.url} not saving.\nError: {e}')

    def urls_generator(self):
        for url in self.detail_urls:
            yield url

    def run(self, user_search: UserSearch):
        vacancies_url = self.prepare_vacancies_url(user_search)
        self.detail_urls = self.parse_detail_urls(vacancies_url)

        try:
            urls_gen = self.urls_generator()
            with ThreadPoolExecutor(max_workers=2) as executor:
                executor.map(self.save_raw_vacancy, urls_gen)
        except Exception as e:
            print(e)
