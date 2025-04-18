import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


def is_shorten_link(token, url):
    try:
        parsed = urlparse(url)
        if parsed.netloc != 'vk.cc' or len(parsed.path) <= 1:
            return False

        response = requests.get(
            "https://api.vk.com/method/utils.getLinkStats",
            params={
                "access_token": token,
                "key": parsed.path[1:],
                "v": "5.131"
            },
            timeout=3
        )
        data = response.json()
        return 'error' not in data

    except requests.exceptions.RequestException:
        return False


def count_clicks(token, short_url):
    parsed = urlparse(short_url)
    response = requests.get(
        "https://api.vk.com/method/utils.getLinkStats",
        params={
            "access_token": token,
            "key": parsed.path[1:],
            "v": "5.131"
        },
        timeout=5
    )
    response.raise_for_status()
    return sum(day['views'] for day in response.json()['response']['stats'])


def shorten_link(token, original_url):
    parsed = urlparse(original_url)
    if not parsed.scheme:
        original_url = f'https://{original_url}'

    response = requests.get(
        "https://api.vk.com/method/utils.getShortLink",
        params={
            "access_token": token,
            "url": original_url,
            "v": "5.131"
        },
        timeout=5
    )
    response.raise_for_status()
    return response.json()['response']['short_url']


def main():
    load_dotenv()

    try:
        token = os.environ['VK_API_TOKEN']
        url = input("Введите URL: ").strip()

        if is_shorten_link(token, url):
            print(f"Кликов: {count_clicks(token, url)}")
        else:
            print(f"Сокращенная ссылка: {shorten_link(token, url)}")

    except KeyError:
        print("Ошибка: Укажите VK_API_TOKEN в .env")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети: {str(e)}")
    except Exception as e:
        print(f"Ошибка обработки: {str(e)}")


if __name__ == "__main__":
    main()
