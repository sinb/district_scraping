import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20',
}

output_filename = "out_lng_lat.txt"
def append_file(data):
    with open(output_filename, "a") as f:
        f.write("\t".join(data) + "\n")

def load_data(filename):
    data = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                item = line.strip().split("\t")
                data.append(item)
    return  data

def add_lat_long(data, city_code):
    url_prefix = r"https://maps.google.com/maps/api/geocode/json?sensor=false&address="
    count = 0
    for item in data:
        print(count)
        count += 1
        name = item[1]
        if item[-1] != "2": # 非市级，名字前面加上市，后面去掉 居委会 村委会 办事处
            name = city_code[item[0][:4]] + name
            name = name.rstrip("办事处").rstrip("居委会").rstrip("委会")
        print(name)
        url = url_prefix + name
        response = requests.get(url, headers=headers)
        json_obj = response.json()
        if json_obj.get("status") == "OK":
            result = json_obj.get("results")
            if len(result) > 0:
                lat_lng = result[0].get("geometry").get("location")
                lat = lat_lng.get("lat")
                lng = lat_lng.get("lng")
                item.append(str(lng))
                item.append(str(lat))
            else:
                item.append("999.999")
                item.append("999.999")
        else:
            item.append("999.999")
            item.append("999.999")
        append_file(item)

def get_city_code(filename):
    data = {}
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                item = line.strip().split("\t")
                if item[-1] == "2":
                    print(line)
                    data[item[0][:4]] = item[1]
    return data

city_code = get_city_code("out.txt")
data = load_data("out.txt")

add_lat_long(data, city_code)
