import asyncio
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import xmltodict, json
from lxml import html

import pyppeteer
from requests import session
from requests_html import HTMLSession, AsyncHTMLSession, HTML
from soupsieve import select

from customers.models import UserSearch
from job.models import RawVacancy
from job.utils import extract_salary


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
            'exp_level': user_search.years_need,
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
            )

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
            print(li.text_content().lower())
            if 'віддалено' in li.text_content().lower():
                remote = True
        try:
            return remote
        except:
            return False

    def save_vacancy(self, raw_vacancy: RawVacancy):
        html_page = html.fromstring(raw_vacancy.data)
        source = raw_vacancy.url.split('/')[2]
        url = raw_vacancy.url
        raw_data = raw_vacancy
        description = html_page.xpath("//div[@class='col-sm-8 row-mobile-order-2']")[0].text_content()
        programming_language = html_page.xpath("//ul[@id='job_extra_info']/li[@class='mb-1'][1]/div[@class='row']/div[@class='col pl-2']")[0].text_content()
        table_top_block = html_page.xpath("//strong")
        table_bot_block = html_page.xpath("//div[@class='col pl-2']")
        salary_min, salary_max = self.extract_salary(table_top_block)
        location = self.extract_location(table_bot_block)
        is_remote = self.extract_remote(table_top_block)
        print(is_remote)




    def run(self, user_search: UserSearch):
        vacancies_url = self.prepare_vacancies_url(user_search)
        self.detail_urls = self.parse_detail_urls(vacancies_url)

        try:
            urls_gen = self.urls_generator()
            with ThreadPoolExecutor(max_workers=2) as executor:
                executor.map(self.save_raw_vacancy, urls_gen)
        except Exception as e:
            print(e)

    # async def render_html(self, vacancies_url):
    #     new_loop = asyncio.new_event_loop()
    #     asyncio.set_event_loop(new_loop)
    #     asession = AsyncHTMLSession()
    #     browser = await pyppeteer.launch({
    #         'ignoreHTTPSErrors': True,
    #         'headless': True,
    #         'handleSIGINT': False,
    #         'handleSIGTERM': False,
    #         'handleSIGHUP': False
    #     })
    #     asession._browser = browser
    #     response = await asession.get(vacancies_url)
    #     await response.html.arender(scrolldown=2, sleep=2)
    #     return response


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
        query_params = '/vacancies/?'
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

    def parse_detail_urls(self, vacancies_url):
        with HTMLSession() as session:
            response = session.get(url=vacancies_url)
        urls = response.html.xpath("//div[@class='title']/a[@class='vt']/@href")
        return urls

    def save_raw_vacancy(self, url):
        with HTMLSession() as session:
            response = session.get(url=url)
            sleep(5)
        if not RawVacancy.objects.filter(url=url).exists():
            obj = RawVacancy.objects.create(
                url=url,
                data=response.html.html,
            )

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
