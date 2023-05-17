from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests
import csv

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict = {
  "type": "service_account",
  "project_id": "aerial-utility-385622",
  "private_key_id": "899e3822d89a2f3cb8271445897c7bf0dc0da67f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCy39UWUSnamxlL\n2lpLKCrRq+uscu6kByFrngigX2dVFUIdNJ2EV3PPMijfP+7BwKTKAGItzvyvvUFU\nubiTc2W95IOLBkeMVjwn2rfjhwfw9lSvq7lXQyLFuztbt7D0F3uljmk3ZY9DnFcY\nByi9XuDwvjvCkCBrL7MJLFYH3AuwwIj+SwJxN0IJhHXnCuI04/TPjafPwBJB/Fyf\nzviqDtKMYm4+Df6UOZw6Dcqh6igZEAbZc3WPAikH5b8/1A79ePPPUhFelLDp3FA2\nmVlv4zbJ1Mm9VC57zBVZ+WHpXGps7uyRmkX4vKxSTaYUfM8Yu05Gd2b2JIwqiRk2\nBTVsnHJ5AgMBAAECggEACqHaYSa25asVcFhMyK3dCbR94DS+sZpI5sQwgBPbqQeH\n9AN2H3ExTY4ONuLudq7UPLuUGmP0yh9mPDqD2aPg1s438XIQm6tejQHnr0sN8kk6\nFG0RKbowXW95IkUDbCbfLyKNZ4EOaHbpCGEYj1UN6tFr7O8zNhvSOQfdHz95pGpb\n6BU/6UcsFcNbvfOq5IitLF7MTE8VwNpGRT8FbgoyvuOz8GyAb78d/C2HWiYIviF1\nN4HSg4g/83D1jHMelhqIuc4BXUwK9pRLBV5tv0dewguXv2HGbCvi/IMyq75hD4X9\n1V028/+mbNkOl+ycIQnmmkRf83bGY07gHBIrmwCuAQKBgQDa4lS+Rv4qg9p3gBmC\n7xEorvlZ6bo6+hYgbqbNyDTeUcm4jJDqeZuh0cHXiWjjmSN4a5xE6OS6iNgOI7Iz\nz402/0BNsq/oj18r5I7Jl48K2evOs9ffyCQUxyRUs7QFbPijthbyrD6LkGMgzVGh\nZZqATbEIEH1wMbO61+JWvP9K+QKBgQDRNLGw7Kx3gX6nNVUj+5/i1FEZBbS+BE7I\nVPQTSS7GlTDKMEsLWOnEbzqZLvRpIEKOkBOVG028D/92/URjVH0dS7NRb4nx4OVU\nUOT/QRtKkRcpCl8LHZJOKK/5qaUOSvlyy1fucTi8aHGa/6fGL5gJ3JV2iGsnAclZ\nDFVLw7zDgQKBgBYhP/Qk9VmTDyl52Bp21UNJvYgrq1p/InGQ/mhbz4yStFRmUdiD\nBwsrS+/gwqwQNZfdOWV2Lnn1j/KOBVxbpalj0TqJ0GMw66xiZVVYb2vncIHriO3l\nLFC1eaTerlrGE7VpmZRbec9ef8c3OwOYZDCIqldoY2ZOgB9p6EZgwWbxAoGAD3QO\nAByrbLRzD5Tf8iV/HPlD+E40mKimzSOBV/9a5i5VCUph8LejpO/2ayRNx4orgG5i\nE+yNZGvmGfsBVzkBeO2DlGthzC0po33KPJSpmGt5Q33RoXeQvBdDUHTYjWK6ZGFi\n4GkaoMgyRBnIYdpYJ7pUjAntqFb4cYx4rH0L74ECgYBF5XAv1ZG4eb/paqT7BMsV\n4AKmBMM09GpYhn8ZMUbc78U+t7pdRLjVNznPDrueKUhUDAQ2AS3Fjjuidi1heL44\n2kKY7J8FVZO5PqtUBZdj2WIxPhYQ/ErXqnNzY2yc3A2Un4Q6+4HWhmeYgm7zlIbs\nD37u2Y/1dt+JWodc4HYOWA==\n-----END PRIVATE KEY-----\n",
  "client_email": "dados-90@aerial-utility-385622.iam.gserviceaccount.com",
  "client_id": "116014305891511972247",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dados-90%40aerial-utility-385622.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('atividade-4') ### Nome do seu bucket
  blob = bucket.blob('artist-names.csv')

  pages = []
  names = "Name \n"

  for i in range(1, 5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + str(i) + '.htm'
    pages.append(url)

  for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')

    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    artist_name_list = soup.find(class_='BodyText')
    artist_name_list_items = artist_name_list.find_all('a')

    for artist_name in artist_name_list_items:
      names = names + artist_name.contents[0] + "\n"

    blob.upload_from_string(names, content_type="text/csv")

except Exception as ex:
  print(ex) 
