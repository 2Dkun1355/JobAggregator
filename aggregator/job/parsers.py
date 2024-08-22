import asyncio
from concurrent.futures import ThreadPoolExecutor
from time import sleep

import pyppeteer
from requests import session
from requests_html import HTMLSession, AsyncHTMLSession
from soupsieve import select

from customers.models import UserSearch
from job.models import RawVacancy


class DjinniParser:
    base_url = 'https://djinni.co'
    detail_urls = []

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

    def parse_detail_urls(self, vacancies_url):
        vacancies_url = 'https://djinni.co/jobs/?primary_keyword=Python&salary=1000&employment=remote&english_level=intermediate'
        with HTMLSession() as session:
            response = session.get(url=vacancies_url)

        # last_page = response.html.xpath("//a[@class='page-link']")
        links = response.html.xpath("//a[@class='job-item__title-link']/@href")
        urls = [f'{self.base_url}{link}' for link in links]
        return urls

    def save_vacancy(self, url):
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

    # @staticmethod
    # async def save_vacancy(url):
    #     new_loop = asyncio.new_event_loop()
    #     asyncio.set_event_loop(new_loop)
    #     session = AsyncHTMLSession()
    #     browser = await pyppeteer.launch({
    #         'ignoreHTTPSErrors': True,
    #         'headless': True,
    #         'handleSIGINT': False,
    #         'handleSIGTERM': False,
    #         'handleSIGHUP': False
    #     })
    #     session._browser = browser
    #     resp_page = await session.get(url)
    #     await resp_page.html.arender(scrolldown=2, sleep=2)  # 1 scroll down approximately exactly 10 news
    #     return resp_page
