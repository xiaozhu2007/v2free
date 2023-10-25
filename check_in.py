# coding=UTF-8

import json
import logging
import argparse
import requests

class CheckIn(object):
    client = requests.Session()
    login_url = "https://v2free.org/auth/login"
    sign_url = "https://v2free.org/user/checkin"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.masked_username = self.email_masking(username)

    # 1234567@qq.com -> 1******@q*.com
    def email_masking(self, email):
        length = len(email)
        at_index = email.rfind('@')
        dot_index = email.rfind('.')
        masked_email = email[0].ljust(at_index, '*') + email[at_index:at_index + 2] + \
            email[dot_index:length].rjust(length - at_index - 2, '*')
        return masked_email

    def check_in(self):
        headers = {
            "Host": "v2free.org",
            "Origin": "https://v2free.org",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Referer": "https://v2free.org/auth/login",
            "X-Requested-With": "XMLHttpRequest",
        }
        data = {
            "email": self.username,
            "passwd": self.password,
            "code": "",
            "remember_me": "week",
        }
        resp = self.client.post(self.login_url, data=data, headers=headers)
        ##### DEBUG #####
        print(resp.cookies)
        ##### DEBUG #####
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Referer": "https://v2free.org/user",
            "X-Requested-With": "XMLHttpRequest",
        }
        response = self.client.post(self.sign_url, cookies=resp.cookies, headers=headers)
        ##### DEBUG #####
        print(response.text)
        ##### DEBUG #####
        logging.info(self.masked_username + " " + response.json()["msg"])


if __name__ == "__main__":
    LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"
    logging.basicConfig(filename='run.log',
                        level=logging.INFO, format=LOG_FORMAT)

    parser = argparse.ArgumentParser(description='V2free 自动签到脚本')
    parser.add_argument('--username', type=str, help='您的账号(仅支持单个)')
    parser.add_argument('--password', type=str, help='您的密码(仅支持单个)')
    args = parser.parse_args()
    helper = CheckIn(args.username, args.password)
    helper.check_in()
