import requests
import json

url = 'https://kauth.kakao.com/oauth/token'
client_id = '본인의 REST API 키'
redirect_uri = 'https://example.com/oauth'
code = '발급받은 인증 코드'

data = {
    'grant_type':'authorization_code',
    'client_id':client_id,
    'redirect_uri':redirect_uri,
    'code': code,
    }

response = requests.post(url, data=data)
tokens = response.json()
print(tokens)

#발행된 토큰 저장
with open("token.json","w") as kakao:
    json.dump(tokens, kakao)


