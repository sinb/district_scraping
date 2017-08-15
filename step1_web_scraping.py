import requests
from pyquery import PyQuery as pq
from lxml import etree
from urllib.parse import urljoin

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20',
}

level_class_name = {
    2: "citytr",
    3: "countytr",
    4: "towntr",
    5: "villagetr",
}
result = []

output_filename = "out.txt"
def append_file(data):
    with open(output_filename, "a") as f:
        f.write("\t".join(data[:3]) + "\t" + str(data[-1]) + "\n")

def get_pq_obj_from_url(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'gbk'
    return pq(response.text)

def next_level_scrap(next_url, parent_code, level):
    print(level)
    d = get_pq_obj_from_url(next_url)
    for i in d("tr[class='%s']" % level_class_name[level]).items():
        if level == 5:
            id, _, name = i.text().split(" ")
        else:
            id, name = i.text().split(" ")
        next_relative_url = i("a").attr("href")
        if not next_relative_url: # 要么是市辖区，要么到头了。如果是市辖区就continue， 否则return
            if name == "市辖区":
                continue
            else:
                item = [id, name, parent_code, level]
                result.append(item)  # append result
                append_file(item)
                print(name)
        else:
            next_absolute_url = urljoin(next_url, next_relative_url)
            item = [id, name, parent_code, level]
            result.append(item)  # append result
            append_file(item)
            print(name)
            # go next
            if level == 5:
                return
            next_level_scrap(next_absolute_url, id, level+1)

# application entrance
# level 2 市级, 父级默认620000(甘肃代码)
url = r"""http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/62.html"""
level = 2
parent_id = "620000"
next_level_scrap(url, parent_id, 2)


