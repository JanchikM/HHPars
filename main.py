import requests
import bs4
import fake_headers
import json


URL = 'https://spb.hh.ru/search/vacancy?text=Django+Flask&salary=&ored_clusters=true&area=1&area=2&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line'


def gen_headers():
    headers_gen = fake_headers.Headers(os='win', browser='chrome')
    return headers_gen.generate()


response = requests.get(URL, headers=gen_headers())
main_html = response.text
main_page = bs4.BeautifulSoup(main_html, 'lxml')
vacancy_div_tag = main_page.find('div', id="a11y-main-content")
vacancy_tag = vacancy_div_tag.find_all('div', class_="serp-item serp-item_link")

vacancy_dict = []
for vacancy_tags in vacancy_tag:
    name_vacancy = vacancy_tags.find('h3', class_='bloko-header-section-3').text
    href = vacancy_tags.find('a', class_="bloko-link")['href']
    name_company_tag = vacancy_tags.find('div', class_="vacancy-serp-item__meta-info-company").text.replace('\xa0', ' ')
    city = vacancy_tags.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text.replace('\xa0', ' ')
    salary = vacancy_tags.find(class_='bloko-header-section-2')
    if salary is not None:
        salary = salary.text.replace(u"\u202F", " ")
    else:
        salary = f'Зарплата не указана'


    vacancy_dict.append({
        'name_vacancy': name_vacancy,
        'name_company': name_company_tag,
        'city': city,
        'salary': salary,
        'href': href
    })

    with open('vacancies.json', 'w', encoding='utf-8') as file:
        json.dump(vacancy_dict, file, ensure_ascii=False, indent=4)

