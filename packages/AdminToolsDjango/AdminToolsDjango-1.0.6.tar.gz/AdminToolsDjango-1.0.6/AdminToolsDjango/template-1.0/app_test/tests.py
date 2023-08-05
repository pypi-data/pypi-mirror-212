from django.test import TestCase
import requests
# Create your tests here.

ls_test_url = [
    'http://43.139.189.169:82/app_test/test',
    # 'http://43.139.189.169:82/admin',
    'http://43.139.189.169:82/static/test.txt',
]
for test_url in ls_test_url:
    response = requests.get(test_url)
    if response.status_code == 200:
        print(test_url, response.status_code, response.text)
    else:
        print(test_url, response.status_code)


