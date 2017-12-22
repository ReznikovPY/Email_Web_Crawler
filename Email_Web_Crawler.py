import requests
from bs4 import BeautifulSoup
import re

url = str(input('Enter your url:'))
deep = int(input('Enter deep should:'))

mail = []


def get_html(url):
    r = requests.get(url)
    html = r.text
    return html


def get_page_url(html):
    total_links = []
    soup = BeautifulSoup(html, 'html.parser')

    name = url.split('/')[2]

    # Получаем все ссылки
    for all_links in soup.find_all('a'):
        links = all_links.get('href')

        # Отсекаем с решеткой
        if not links.startswith('#'):

            # Внутреним ссылкам делаем полный путь
            if links[0] == '/':
                correct = 'https://' + name + links
                if not correct in total_links:
                    total_links.append(correct)

            # Отсекаем ссылкы не связаные с этим сайтом
            elif not links in total_links and name in links:
                total_links.append(links)

    return total_links


def get_page_mail(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()

    # Ищем mail на странице
    all_mail = re.findall(r'[\w.-]+@[\w.-]+\.?[\w]+?', text)
    for mails in all_mail:
        if not mails in mail:
            mail.append(mails)


def main():
    gpu = get_page_url(get_html(url))

    if deep == 1:
        get_page_mail(get_html(url))
        print(mail)
    elif deep > 1:
        get_page_url(get_html(url))
        for i in gpu:
            get_page_mail(get_html(i))
        for m in mail:
            print(m)


if __name__ == '__main__':
    main()
