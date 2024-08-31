import uuid
from datetime import date

from faker import Faker
from random import random, choice, choices, randint, randrange

from django.contrib.auth.models import User

from job.models import RawVacancy, Vacancy

SKILLS = ['oop', 'python', 'git', 'postgresql', 'mysql', 'django', 'github', 'celery-beat', 'postman',
          'sqlalchemy', 'fastapi', 'asyncio', 'docker', 'docker-compose', 'drf', 'api', 'rest',
          'kubernetes', 'celery', 'redis', 'graphql', 'rest', 'linux', 'ci/cd', 'aws', 'pytest', 'pandas', 'numpy',
          'tensorflow', 'pytorch', 'javascript', 'typescript', 'html', 'css', 'sass', 'less', 'react', 'vue',
          'angular', 'node.js', 'express.js', 'flask', 'ruby', 'rails', 'java', 'spring', 'kotlin', 'swift',
          'objective-c', 'c', 'c++', 'c#', '.net', 'go', 'rust', 'php', 'laravel', 'symfony', 'perl', 'elixir',
          'phoenix', 'scala', 'haskell', 'clojure', 'r', 'matlab', 'bash', 'shell', 'powershell', 'typescript',
          'graphql', 'julia', 'dart', 'flutter', 'rust', 'solidity', 'truffle', 'web3.js', 'api']
fake = Faker()


def search_for_skills(description):
    skills_in_description = []
    description = [word.lower() for word in set(description.split())]
    for word in SKILLS:
        if word in description:
            skills_in_description.append(word)
    return ', '.join(skills_in_description)


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

def generate_mock_data():
    for i in range(100):
        url = f'https://fakeurl/uuid/{uuid.uuid4().hex}'
        source = choice(['DOU', 'Djinni', 'WORK', 'ROBOTA'])
        is_processed = choice([True, False])
        data = '<h1> Fake data </h1>'
        programming_language = choice(['Python', 'Java', 'Javascript', 'PHP', None])
        salary_min = randrange(500, 5000, 100)
        salary_max = salary_min * 1.2
        location = choice(['Lviv', 'Kyiv', 'Dnipro', 'Odesa', None])
        is_remote = choice([True, False, None])
        level_need = choice(['Junior', 'Middle', 'Senior', None])
        years_need = choice([1, 2, 3, 4, 5, None])
        skills = ", ".join(choices(SKILLS, k=6))
        description = f'Skills: {skills}'
        english_lvl = choice(['Pre Intermediate', 'Intermediate', 'Upper Intermediate', None])
        created = fake.date_between(start_date=date(year=2024, month=6, day=1),
                                    end_date=date(year=2024, month=8, day=31))
        try:
            raw_vacancy = RawVacancy.objects.create(
                url=url,
                source=source,
                is_processed=is_processed,
                data=data,
            )
            vacancy = Vacancy.objects.create(
                url=url,
                source=source,
                raw_data=raw_vacancy,
                description=description,
                programming_language=programming_language,
                salary_min=salary_min,
                salary_max=salary_max,
                location=location,
                is_remote=is_remote,
                years_need=years_need,
                level_need=level_need,
                skills=skills,
                english_lvl=english_lvl,
                created_data=created,
            )

        except Exception as e:
            print(e)



