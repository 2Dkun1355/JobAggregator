def search_for_skins(description):
    SKILLS = ['oop', 'python', 'git', 'postgresql', 'mysql', 'django', 'sqlalchemy', 'fastapi', 'asyncio']
    skills_in_description = []
    description = [word.lower() for word in set(description.split())]
    for word in SKILLS:
        if word in description:
            skills_in_description.append(word)
    return skills_in_description

def extract_salary(raw_string):
    salary = ''
    for char in raw_string:
        if char.is_digit():
            salary += char
    return salary