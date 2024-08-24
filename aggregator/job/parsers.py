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
from job.models import RawVacancy
from job.utils import extract_salary, search_for_skins


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
    def save_vacancy(raw_vacancy: RawVacancy):
        html_page = html.fromstring(raw_vacancy.data)
        print(type(html_page))
        source = raw_vacancy.url.split('/')[2]
        url = raw_vacancy.url
        raw_data = raw_vacancy
        description = html_page.xpath("//div[@class='col-sm-8 row-mobile-order-2']")[0].text_content()
        programming_language = html_page.xpath("//ul[@id='job_extra_info']/li[@class='mb-1'][1]/div[@class='row']/div[@class='col pl-2']")[0].text_content()
        try:
            salary_max = html_page.xpath("//div[@class='col']/h1/span[@class='public-salary-item']")[0].text_content()
            salary_max = extract_salary(salary_max)
        except:
            salary_max = None



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
        query_params = '/vacancies/feeds/?'
        for key, value in mapper.items():
            if value:
                query_params += f'{key}={value}&'
        url = f'{self.base_url}{query_params}'
        print(url)
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
    def save_vacancy(raw_vacancy: RawVacancy):
        html_page = html.fromstring(raw_vacancy.data)
        source = raw_vacancy.url.split('/')[2]
        url = raw_vacancy.url
        raw_data = raw_vacancy
        programming_language = html_page.xpath("//li[@class='breadcrumbs']/a[2]")[0].text_content()
        description = html_page.xpath("//div[@class='l-vacancy']/div[@class='b-typo vacancy-section']")[0].text_content()
        plase = html_page.xpath("//li[@class='breadcrumbs']/a[3]")[0].text_content()
        location = plase if plase !='віддалено' else None
        is_remote = True if plase == 'віддалено' else False
        skills = search_for_skins(description)
        created_data = html_page.xpath("//div[@class='date']")[0].text_content().strip()
        locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8')
        created_data = datetime.strptime(created_data, "%d %B %Y").date()

    def run(self, user_search: UserSearch):
        vacancies_url = self.prepare_vacancies_url(user_search)
        self.detail_urls = self.parse_detail_urls(vacancies_url)

        try:
            urls_gen = self.urls_generator()
            with ThreadPoolExecutor(max_workers=2) as executor:
                executor.map(self.save_raw_vacancy, urls_gen)
        except Exception as e:
            print(e)

