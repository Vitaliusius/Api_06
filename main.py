import telegram
import imghdr
import random
import requests

from dotenv import load_dotenv
from environs import env


FIRST_COMIC_NUMBER = 1


def get_actual_comic_number():
	response = requests.get("https://xkcd.com/info.0.json")
	response.raise_for_status()
	actual_comic_number = response.json().get("num")
	return actual_comic_number


def get_comic_text_and_img_url(comic_number):
	comic_url = f"https://xkcd.com/{comic_number}/info.0.json"
	response = requests.get(comic_url)
    response.raise_for_status()
    comic_img_url = response.json().get('img')
    comic_text = response.json().get('alt')
    return comic_img_url, comic_text

    
def send_comic_in_tg(url, tg_token, tg_chat_id, caption):
	bot = telegram.Bot(token=tg_token)
	bot.send_photo(chat_id=tg_chat_id, photo=url, caption=caption)   


def main():
	load_dotenv()
	tg_token = env.str("TLGRM_BOT_API_KEY")
	tg_chat_id = env.str("TLGRM_CHAT_ID")
	comic_number = random.randint(FIRST_COMIC_NUMBER, get_actual_comic_number())
	comic_img_url, comic_text = get_comic_text_and_img_url(comic_number)
	send_comic_in_tg(comic_img_url, tg_token, tg_chat_id, comic_text)


if __name__ == "__main__":
	main()