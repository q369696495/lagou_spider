import random
import re

import execjs
import requests


class LagouCookieSpider:

    def __init__(self, *args, **kwargs):
        self.js = execjs.compile(open("lagou.js", "r").read())

    def main(self):
        main_url = f"http://www.lagou.com/utrack/trackMid.html"
        headers = {
            "user-agent": f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/{random.randint(1, 999)}.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
            "referer": "https://www.lagou.com/"
        }
        response = requests.get(main_url, headers=headers)
        self.track_mid_parse(response)

    def track_mid_parse(self, response):
        set_cookie = response.headers["Set-Cookie"]
        user_trace_token_value = re.search("user_trace_token=(.*?);", set_cookie)
        response_time = response.headers["Date"]
        if user_trace_token_value:
            user_trace_token_value = user_trace_token_value.group(1)
            x_http_token = self.js.call("get_token", user_trace_token_value, response_time)
            web_tj = self.js.call("get_webtj_id")
            cookie_dict = {"X_HTTP_TOKEN": x_http_token,
                           "WEBTJ-ID": web_tj,
                           "user_trace_token": user_trace_token_value}
            self.demo(cookie_dict)

    def demo(self, cookie_dict):
        url = "https://www.lagou.com/jobs/positionAjax.json"
        data = {"first": "false", "pn": "1", "kd": "Java"}
        cookies_str = ";".join([f"{k}={v}" for k, v in cookie_dict.items()])
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
            "referer": "https://www.lagou.com/jobs/list_Java/p-city_215?px=default",
            "cookie": cookies_str}
        response = requests.post(url, data=data, headers=headers)
        response_json = response.json()
        print(response_json)
        pass


if __name__ == '__main__':
    lagou_cookie = LagouCookieSpider()
    lagou_cookie.main()
