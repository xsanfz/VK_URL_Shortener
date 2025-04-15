import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


def is_short_url(url):
    parsed = urlparse(url)
    return parsed.netloc == 'vk.cc' and len(parsed.path) > 1


def process_url(token, url):
    if not token:
        return "Ошибка: Не задан токен доступа"

    try:
        if is_short_url(url):
            short_code = urlparse(url).path[1:]
            response = requests.get(
                "https://api.vk.com/method/utils.getLinkStats",
                params={"access_token": token, "key": short_code, "v": "5.131"},
                timeout=5
            )
            data = response.json()
            if "error" in data:
                return f"Ошибка статистики: {data['error']['error_msg']}"
            return f"Кликов: {sum(day['views'] for day in data['response']['stats'])}"
        else:
            response = requests.get(
                "https://api.vk.com/method/utils.getShortLink",
                params={"access_token": token, "url": url, "v": "5.131"},
                timeout=5
            )
            data = response.json()
            if "error" in data:
                return f"Ошибка сокращения: {data['error']['error_msg']}"
            return f"Сокращенная ссылка: {data['response']['short_url']}"
    except requests.exceptions.RequestException as e:
        return f"Ошибка сети: {str(e)}"


def main():
    load_dotenv()
    TOKEN = os.getenv("VK_API_TOKEN")

    print("Сервис обработки ссылок VK")


    while True:
        url = input("\nВведите ссылку (или 'q' для выхода): ").strip()
        if url.lower() == 'q':
            break

        if not urlparse(url).scheme:
            url = 'https://' + url

        result = process_url(TOKEN, url)
        print(result)


if __name__ == "__main__":
    main()
    # TOKEN = "7db8c8fe7db8c8fe7db8c8fe1f7e979cf177db87db8c8fe1a45ffa0e0a7530175d2a5d5"
    # TEST_URL = "https://api.vk.com/method/utils.getShortLink"






