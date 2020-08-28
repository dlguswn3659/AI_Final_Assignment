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


client_id = "FIdfzEHVHf8313PRsF4D"
client_secret = "O_RYgSTjdl"
# url = "https://openapi.naver.com/v1/vision/face" # 얼굴감지
url = "https://openapi.naver.com/v1/vision/celebrity"  # 유명인 얼굴인식
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
# image_url = 'https://steemitimages.com/u/ned/avatar'
# urllib.request.urlretrieve(image_url, file_name)
Image.open(file_name)

files = {'image': open(file_name, 'rb')}
url = "https://openapi.naver.com/v1/vision/face" # 얼굴감지
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

  
# body = json.dumps(response.text)

# request = urllib.request.Request(url)
# request.add_header("X-Naver-Client-Id",client_id)
# request.add_header("X-Naver-Client-Secret",client_secret)
# request.add_header("Content-Type","application/json")
# response = urllib.request.urlopen(request, data=body.encode("utf-8"))
# json_obj = json.loads(response.read().decode('utf-8'))

# print(json_obj)

# df = []

# df.append(pd.DataFrame(json_obj['results'][0]['data'])); df[0].columns=['기간','패션의류'];
df.append(pd.DataFrame(json_obj['results'][1]['data'])); df[1].columns=['기간','화장품/미용'];

