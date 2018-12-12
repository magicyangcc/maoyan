import re
import json
import requests
from multiprocessing import Pool
from requests.exceptions import RequestException

# 获取网页
def get_one_page(url, headers):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

#解析网页
def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)"'
                         '.*?boarditem-click.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime"'
                         '>(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[4:],
            'score': item[5]+item[6]
        }

#将爬取的内容写入到文件
def write_one_page(content):
    with open('maoyantop.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False)+'\n')
        f.close()

#主函数
def main(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36"}
    html = get_one_page(url, headers)
    for item in parse_one_page(html):
        write_one_page(item)

if __name__ == "__main__":
    #创建连接池
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])