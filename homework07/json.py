import requests
import csv

directories = ["posts", "comments", "albums", "photos", "todos", "users"]
mainurl = 'https://jsonplaceholder.typicode.com/'
url = [mainurl + singledir for singledir in directories]

def subdict2dict(dict1:dict, parent_key='') -> dict:
    items = []
    for key1, value1 in dict1.items():
        new_key = f"{parent_key}_{key1}" if parent_key else key1
        if isinstance(value1, dict):
            items.extend(subdict2dict(value1, new_key).items())
        else:
            items.append((new_key, value1))    
    return dict(items)

for i in range(len(directories)):
    fnames = directories[i]; singleurl = url[i]
    # exit(print(singleurl))
    json_data = requests.get(singleurl).json()
    
    with open(f"{fnames}.csv", 'w') as file:
        data = [subdict2dict(item) for item in json_data]
        
        if data:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL) 
            writer.writeheader()
            
            for singlepost in data:
                if 'body' in singlepost:
                    singlepost['body'] = singlepost['body'].replace("\n", " ")
                writer.writerow(singlepost)
                
print("Files saved")
