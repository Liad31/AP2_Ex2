import requests

url = 'http://127.0.0.1:9872/api/model?model_type=hybrid'


data = {
        "train_data": {"air_speed": "[4,6,10]",
                        "flat_train": "[8,56,78]"
                       }
        }
header = {
'Content-Type': 'application/json',
'Accept': 'application/json'
}

resp = requests.post(url=url,headers = header,data=data)
print(resp)
