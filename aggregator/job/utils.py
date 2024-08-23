
SKILLS = ['python', 'django', 'sql']

def extract_salary(raw_string):
    salary = ''
    for char in raw_string:
        if char.is_digit():
            salary += char
    return salary