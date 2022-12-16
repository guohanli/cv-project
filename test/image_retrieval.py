# import requests

# resp = requests.post("http://127.0.0.1:5000/densenet/predict",
#                      files={"file": open('../resource/album/cat.png', 'rb')})
# print(resp.json())
import sys 
sys.path.append("..") 
from src.api.image_retrieval import search_img_by_img 

url = search_img_by_img()
