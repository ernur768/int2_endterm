import requests
from bs4 import BeautifulSoup as BS
import csv


def fetch_information(resume_url: str) -> list:
    response = requests.get(resume_url, headers={'User-agent': 'Mozilla/5.0'})
    html = BS(response.content, "html.parser")

    null_field = "not required"
    res = []

    try:
        title = html.select(".resume-block__title-text-wrapper > .bloko-header-2 > "
                            ".resume-block__title-text")[0].text
        res.append(title)
    except Exception as e:
        res.append(null_field)
        print(e)

    try:
        specialization = html.select(".resume-block__specialization")[0].text
        res.append(specialization)
    except Exception as e:
        res.append(null_field)
        print(e)

    try:
        salary = html.select(".resume-block__salary")[0].text
        salary = salary.split()[0:-2]
        salary2 = int(''.join(salary[:-1]))
        if salary[-1] == "USD":
            salary2 *= 447
        elif salary[-1] == "руб" or salary[-1] == "RUB":
            salary2 *= 6
        res.append(salary2)
    except Exception as e:
        res.append(null_field)
        print(e)

    try:
        age = html.select('[data-qa="resume-personal-age"]')[0].text
        age = age.split("\xa0")
        res.append(age[0])
    except Exception as e:
        res.append(null_field)
        print(e)

    try:
        employment = html.select(".resume-block-container > p")[0].text
        res.append(employment)
    except Exception as e:
        res.append(null_field)
        print(e)

    try:
        work_schedule = html.select(".resume-block-container > p")[1].text
        res.append(work_schedule)
    except Exception as e:
        res.append(null_field)
        print(e)

    try:
        experience_years = html.select('.resume-block__title-text > span')[0].text
        experience_years = experience_years.split("\xa0")
        res.append(experience_years[0])
    except Exception as e:
        res.append(null_field)
        print(e)

    try:
        experience_month = html.select('.resume-block__title-text > span')[1].text
        experience_month = experience_month.split("\xa0")
        res.append(experience_month[0])
    except Exception as e:
        res.append(null_field)
        print(e)

    try:
        citizenship = html.select('[data-qa="resume-block-additional"] > .resume-block-item-gap > '
                                  '.bloko-columns-row > .bloko-column > .resume-block-container > p')[0].text
        res.append(citizenship)
    except Exception as e:
        res.append(null_field)
        print(e)

    try:
        sex = html.select('[data-qa="resume-personal-gender"]')[0].text
        res.append(sex)
    except Exception as e:
        res.append(null_field)
        print(e)

    res.append(resume_url)

    return res


def collect_resumes(page_url: str, fileName: str) -> None:
    response = requests.get(page_url, headers={'User-agent': 'Mozilla/5.0'})
    html = BS(response.content, "html.parser")

    for resume in html.select(".resume-serp-content > .serp-item"):
        resume_tag = resume.select(".resume-search-item__content-wrapper > "
                                   ".resume-search-item__content-layout > .resume-search-item__content > "
                                   ".resume-search-item__header > .bloko-header-section-3 > a")
        resume_url = "https://hh.kz/" + resume_tag[0].get("href")

        row = fetch_information(resume_url)
        with open(fileName, 'a', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(row)


def go_throw_pages(theme: str, page_number: int, file_name: str) -> None:
    for page in range(page_number):
        url = f"https://hh.kz/search/resume?text={theme}" \
              f"&area=40&isDefaultArea=true&pos=full_text" \
              f"&logic=normal&exp_period=all_time" \
              f"&currency_code=KZT&ored_clusters=true&order_by=relevance&page={page}"
        collect_resumes(url, file_name)
