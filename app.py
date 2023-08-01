import requests
import json
from datetime import datetime

# 액세스 토큰 재발급 함수
def refresh_token(refresh_token):
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type" : "refresh_token",
        "client_id" : "본인의 REST API 키",
        "refresh_token" : refresh_token
    }
    response = requests.post(url, data=data)
    tokens = response.json()

    with open("token.json", "w") as fp: # 재발급받은 토큰을 파일에 저장
        json.dump(tokens, fp)

    return tokens

# 카카오 API 엑세스 토큰
with open("token.json", "r") as fp:
    tokens = json.load(fp)

url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": "Bearer " + tokens['access_token']
}
data = {
    "template_object" : json.dumps({ "object_type" : "text",
                                     "text" : "Test "+ str(datetime.now().strftime("%Y-%m-%d %H:%M"))+ "\n" +"https://news.naver.com/",
                                     "link" : {
                                                 "web_url" : "https://search.naver.com/search.naver?where=news&sm=tab_jum&query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90"
                                              },
                                    "button_title" : "확인하기"
                                        
    })
}
response = requests.post(url, headers=headers, data=data)
response_json = response.json()
print(response_json)

if response_json.get('result_code') == 0:
    print('메시지를 성공적으로 보냈습니다.')
elif response_json.get('code') == -401:  # 액세스 토큰이 만료되었을 때의 오류 코드
    print('액세스 토큰이 만료된 것 같습니다. 재발급 중...')
    tokens = refresh_token(tokens['refresh_token'])  # 액세스 토큰 재발급
    print('메시지를 재전송 해 주세요')
    # 재발급 받은 토큰을 사용해서 메시지를 다시 보낼 수 있습니다.
else:
    print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))