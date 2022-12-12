import requests

resp = requests.post("http://127.0.0.1:5000/densenet/predict",
                     files={"file": open('../resource/album/cat.png', 'rb')})
print(resp.json())
