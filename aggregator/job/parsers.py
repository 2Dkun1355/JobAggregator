from requests_html import HTMLSession
from customers.models import UserSearch


class DjinniParser:
    base_url = 'https://djinni.co'

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

        links = response.html.xpath("//a[@class='job-item__title-link']/@href")
        urls = [f'{self.base_url}{link}' for link in links]
        return urls
