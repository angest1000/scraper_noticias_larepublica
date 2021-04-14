import requests
import lxml.html as html
import os  # Sirve para crear una carpeta
import datetime

home_url = 'https://www.larepublica.co/'

# Siempre se debe cambiar 'h2' por 'text-fill'
xpath_link_to_article = '//text-fill/a/@href'
xpath_title = '//div[@class ="mb-auto"]/text-fill/span/text()'
xpath_summary = '//div[@class="lead"]/p/text()'
xpath_body = '//div[@class="html-content"]//text()'


def parse_to_notices(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(xpath_title)[0]
                title = title.replace('\"', '')
                summary = parsed.xpath(xpath_summary)[0]
                body = parsed.xpath(xpath_body)
            except IndexError:
                return

            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n ')
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(home_url)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            print(parsed)
            links_to_notices = parsed.xpath(xpath_link_to_article)
            # for link in links_to_notices:
            #     print(link)
            today = datetime.date.today().strftime('%d-%m-%Y')
            if not os.path.isdir(today):  # indica si existe esta carpeta
                os.mkdir(today)
            for link in links_to_notices:
                parse_to_notices(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()


if __name__ == '__main__':
    run()
