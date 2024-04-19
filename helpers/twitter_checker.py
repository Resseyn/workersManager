import json
import urllib.parse

import requests

import configs

a = configs.twitter_cookies
items = a.split('; ')

cookie_dict = {}
for item in items:
    key, value = item.split('=', 1)  # Split by the first '='
    cookie_dict[key] = urllib.parse.unquote(value)  # Unquote to decode URL encoded strings

def check_verified(name):
    name.lower()
    headers = {"Authorization": configs.twitter_auth_token,
                "X-Csrf-Token": configs.twitter_X_Csrf_Token}

    try:
        response = requests.get(f'https://twitter.com/i/api/graphql/qW5u-DAuXpMEG0zA1F7UGQ/UserByScreenName?variables=%7B%22screen_name%22%3A%22{name}%22%2C%22withSafetyModeUserFields%22%3Atrue%7D&features=%7B%22hidden_profile_likes_enabled%22%3Atrue%2C%22hidden_profile_subscriptions_enabled%22%3Atrue%2C%22rweb_tipjar_consumption_enabled%22%3Atrue%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22subscriptions_verification_info_is_identity_verified_enabled%22%3Atrue%2C%22subscriptions_verification_info_verified_since_enabled%22%3Atrue%2C%22highlights_tweets_tab_ui_enabled%22%3Atrue%2C%22responsive_web_twitter_article_notes_tab_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%7D&fieldToggles=%7B%22withAuxiliaryUserLabels%22%3Afalse%7D',
                                 headers=headers, cookies=cookie_dict)
        return json.loads(response.text)["data"]["user"]["result"]["is_blue_verified"]
    except Exception as e:
        return "User doesn't exist"
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait
#
# def check_verified(name):
#     op = webdriver.ChromeOptions()
#     op.add_argument('--headless')
#     driver = webdriver.Chrome(options=op)
#     response = driver.get(f'https://twitter.com/elonmusk')
#     T = True
#     try:
#         WebDriverWait(driver, 7).until(
#             EC.presence_of_element_located(
#                 (By.XPATH,
#                  '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div/div/div/div[2]/div/div/div[1]/div/div/span/span[2]/span/span/div[1]/div')))
#     except:
#         T = False
#     return T