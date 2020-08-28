네이버 API를 활용하여 카메라로 사람을 촬영하고 트렌드 추천해주기

# 카메라로 사람 촬영하기
```
  import os
  import sys
  import requests
  import urllib.request
  from PIL import Image, ImageDraw
  import picamera
  import time

  with picamera.PiCamera() as camera:
      camera.resolution = (640, 480)
      camera.start_preview()
      time.sleep(1)
      camera.capture('person.jpg')
      camera.stop_preview()
```

# 얼굴 감지 API를 사용하여 사진에 대한 여러 데이터를 얻은 후 그 중 성별과 나이에 대한 데이터만 추출
##"https://openapi.naver.com/v1/vision/celebrity" - 얼굴인식 API
```
  client_id = "FIdfzEHVHf8313PRsF4D"
  client_secret = "O_RYgSTjdl"
  url = "https://openapi.naver.com/v1/vision/celebrity"  
  files = {'image': open('person.jpg', 'rb')}
  headers = {'X-Naver-Client-Id': client_id,
             'X-Naver-Client-Secret': client_secret}
  response = requests.post(url,  files=files, headers=headers)
  rescode = response.status_code
  if(rescode == 200):
      print(response.text)
  else:
      print("Error Code:" + rescode)




  file_name =  'person.jpg'
  Image.open(file_name)

  files = {'image': open(file_name, 'rb')}
  url = "https://openapi.naver.com/v1/vision/face" 
  headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }
  response = requests.post(url,  files=files, headers=headers)
  rescode = response.status_code
  if(rescode==200):
      print (response.text)

  print(response.text)

  count = 0

  gender = 'm'
  age = []

  for i in range(0, len(response.text)):
    if response.text[i] == '{':
      count = count + 1
    if count == 6 :
      for j in range(0, 1):
        if response.text[i + 10 + j] != '"':
          gender=response.text[i + 10 + j]
        else :
          break
      count = count + 1
    if count == 8 :
      for j in range(0, 2):
        if response.text[i + 10 + j] != '"':
          age.append(response.text[i + 10 + j])
        else :
          break
      break

  age = ''.join(age)

  print(gender)
  print(age)
```

# 추출한 성별과 나이 데이터를 네이버 쇼핑 API 요청에 넣고 성별과 연령대에 맞는 트렌드 데이터 얻기
##"https://openapi.naver.com/v1/datalab/shopping/categories" - 네이버  API

```
  #-*- coding: utf-8 -*-
  import os
  import sys
  import urllib.request
  import json
  import pandas as pd
  import seaborn as sns; sns.set(style='darkgrid', font='KoPutDOtum', font_scale=1.5)
  import matplotlib.pyplot as plt

  client_id = "Wcz16fZV6Y_4wZqilPCX"
  client_secret = "2TXWghrQrg"

  url = "https://openapi.naver.com/v1/datalab/shopping/categories";
  # body = "{\"startDate\":\"2017-08-01\",\"endDate\":\"2017-09-30\",\"timeUnit\":\"month\",\"category\":[{\"name\":\"패션의류\",\"param\":[\"50000000\"]},{\"name\":\"화장품/미용\",\"param\":[\"50000002\"]}],\"device\":\"pc\",\"ages\":[\"20\",\"30\"],\"gender\":\"f\"}";

  body = {
      'startDate' : '2020-08-21',
      'endDate' : '2020-08-27',
      'timeUnit' : 'date',        # input : [date, week, month]
      'category' : [{'name':'패션의류','param':['50000000']},{'name':'화장품/미용','param':['50000002']}],
      'device' : 'pc',
      'ages' : [age],
      'gender' : gender
  }

  #params : 50000807=원피스, 

  body = json.dumps(body)

  print(body)
  request = urllib.request.Request(url)
  request.add_header("X-Naver-Client-Id",client_id)
  request.add_header("X-Naver-Client-Secret",client_secret)
  request.add_header("Content-Type","application/json")
  response = urllib.request.urlopen(request, data=body.encode("utf-8"))
  json_obj = json.loads(response.read().decode('utf-8'))

  df = []

  df.append(pd.DataFrame(json_obj['results'][0]['data'])); df[0].columns=['기간','패션의류'];
  df.append(pd.DataFrame(json_obj['results'][1]['data'])); df[1].columns=['기간','화장품/미용'];


  print(df[0])
  print(df[1])
  
```  
