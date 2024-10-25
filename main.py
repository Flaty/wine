import datetime
import pandas
import collections
from environs import Env
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_year_declension(years):
    if years % 10 == 1 and years % 100 != 11:
        return "год"
    elif 2 <= years % 10 <= 4 and not (12 <= years % 100 <= 14):
        return "года"
    else:
        return "лет"


if __name__ == '__main__':
    env = Env()
    env.read_env()
    WINE_DB = env.str('WINE_DATABASE')
    excel_database = pandas.read_excel(WINE_DB, usecols=[
        'Категория',
        'Название',
        'Сорт',
        'Цена',
        'Картинка',
        'Акция'
        ], na_values=['Nan', 'nan'], keep_default_na=False).to_dict(orient='records')

    wine_database = collections.defaultdict(list)
    for wine in excel_database:
        category = wine['Категория']
        wine_database[category].append(wine)

    year_of_foundation = 1920
    year = datetime.date.today().year - year_of_foundation
    year_declension = get_year_declension(year)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        wine_database=wine_database,
        years=year,
        years_declension=year_declension
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
