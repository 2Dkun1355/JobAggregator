import asyncio
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import xmltodict, json

import pyppeteer
from requests import session
from requests_html import HTMLSession, AsyncHTMLSession
from soupsieve import select

from customers.models import UserSearch
from job.models import RawVacancy


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
        query_params = '/jobs/?'
        for key, value in mapper.items():
            if value:
                query_params += f'{key}={value}&'
        url = f'{self.base_url}{query_params}'
        return url

    # @staticmethod
    # def calculate_pages_count(vac_count):
    #     pages_count = (int(vac_count) // 15) + 1
    #     print(f'PAges count: {pages_count}')
    #     return pages_count

    @staticmethod
    def parse_detail_urls(vacancies_url):
        with HTMLSession() as session:
            response = session.get(url=vacancies_url)
            xml = xmltodict.parse(response.content)
            page_json = json.dumps(xml)
            page_dict = json.loads(page_json)
            urls = [vac.get('link') for vac in page_dict.get('rss', {}).get('channel', {}).get('item', [])]
        return urls

    @staticmethod
    def save_vacancy(url):
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
                executor.map(self.save_vacancy, urls_gen)
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
