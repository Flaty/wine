import datetime
import pandas
import collections
from pprint import pprint
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_year_declension(years):
    if years % 10 == 1 and years % 100 != 11:
        return "год"
    elif 2 <= years % 10 <= 4 and not (12 <= years % 100 <= 14):
        return "года"
    else:
        return "лет"


excel_database = pandas.read_excel('wine3.xlsx', usecols=[
    'Категория',
    'Название',
    'Сорт',
    'Цена',
    'Картинка',
    'Акция'
    ], na_values=['Nan', 'nan'], keep_default_na=False).to_dict(orient='records')

wine_database = {'Белые вина': [], 'Красные вина': [], 'Напитки': []}
dict_of_lists = collections.defaultdict(list)
for wine in excel_database:
    category = wine['Категория']
    dict_of_lists[category].append(wine)


year = datetime.date.today().year - 1920
year_declension = get_year_declension(year)

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

rendered_page = template.render(
    dict_of_lists=dict_of_lists,
    years=year,
    years_declension=year_declension
)
pprint(dict_of_lists)
with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
print(1)
