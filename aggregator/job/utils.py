def search_for_skills(description):
    SKILLS = ['oop', 'python', 'git', 'postgresql', 'mysql', 'django', 'sqlalchemy', 'fastapi', 'asyncio', 'docker',
              'kubernetes', 'celery', 'redis', 'graphql', 'rest', 'linux', 'ci/cd', 'aws', 'pytest', 'pandas', 'numpy',
              'tensorflow', 'pytorch', 'javascript', 'typescript', 'html', 'css', 'sass', 'less', 'react', 'vue',
              'angular', 'node.js', 'express.js', 'flask', 'ruby', 'rails', 'java', 'spring', 'kotlin', 'swift',
              'objective-c', 'c', 'c++', 'c#', '.net', 'go', 'rust', 'php', 'laravel', 'symfony', 'perl', 'elixir',
              'phoenix', 'scala', 'haskell', 'clojure', 'r', 'matlab', 'bash', 'shell', 'powershell', 'typescript',
              'graphql', 'julia', 'dart', 'flutter', 'rust', 'solidity', 'truffle', 'web3.js', 'api']

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