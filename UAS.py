import requests
from bs4 import BeautifulSoup
import speech_recognition as sr
import re

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',}
        
r=requests.get("https://www.wavsource.com/people/people.htm", headers=headers)

awal = BeautifulSoup(r.text, 'html.parser')
link = 'https://www.wavsource.com/people/'+awal.select('option:nth-child(7)')[0].get('value')

r =requests.get(link, headers=headers)
awal = BeautifulSoup(r.text, 'html.parser')
    

for items in range(0,63):
    select = awal.select('.c1 script')[items].string
    select = select.replace('s2p(','').replace(')','').replace('\'','').strip()
    select = select.split(',')
    select = 'https://www.wavsource.com/snds_2020-10-01_3728627494378403/'+select[0]+'/'+select[1]
    
    with requests.Session() as req:
        name = re.search(r"([^\/]+$)", select).group()
        print(f"Downloading File {name}")
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',}
        download = req.get(select, headers=headers)
        
        if download.status_code == 200:
            print ("berhasil didownload")
            with open('download/'+name, 'wb') as f:
                f.write(download.content)
        else:
            print(f"Download Gagal Boss {name}")

        if items == 2 or items == 11:
            print('File Ini Error \n')
            continue

        recog = sr.Recognizer()  

        # open the file
        with sr.AudioFile('download/'+name) as source:
            # listen for the data (load audio to memory)

            audio_data = recog.record(source)

            # recognize (convert from speech to text)
            try:
                text = recog.recognize_google(audio_data)
                print("Text dari Audio ini adalah : ")
                print(text)
            except:
                print('Suara Tidak Bisa Terdeteksi')
            print('\n')