import requests
import pymongo
from pares_id import *
import random
from multiprocessing import Pool
#47487
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'iuuid=5B292AE1B1FD53A9BFC4CC79A04233C30CC096E5D7890AD49E4AF1A0F2964C69; latlng=39.245911%2C118.207397%2C1534902665674; _lxsdk_cuid=1655f5403c498-0ddc732e86871-9393265-144000-1655f5403c58e; _lxsdk=5B292AE1B1FD53A9BFC4CC79A04233C30CC096E5D7890AD49E4AF1A0F2964C69; mtcdn=K; lsu=; oc=-WgBFk5iQVHClW9yiR8Lkm1TGldUmgEWLjTctASC3y9vD_Y19SEbeS1uK4LJk0OXV98KafhMbAwHs5IIiefbsysKxcTewZKqszd0188AEdCHyaHb17SpHv5P_R7t6Eo0X0nqT-SeStARdmsVJIF6NaR-T7S60fW5zPfd30mRVpk; isid=A929845A1AF73F8D38EBEC1E65392BA1; oops=bKf1HKJzggkA_X5z9NHY1E1O5tUAAAAATwYAAJAIDOlYJ3p4VjfHfi2o-44QilkD_0s54C77xwRWagHMmKRixwZgoUGUIDGyoZckEQ; logintype=normal; uuid=2e26a3297a0149c687b9.1535261718.1.0.0; ci=1; rvct=1%2C104; cityname=%E5%8C%97%E4%BA%AC; _lx_utm=utm_source%3Dso.com%26utm_medium%3Dorganic; IJSESSIONID=5aww3eggyzo41nv3mlcujsnvi; u=356596725',
    'Host': 'ihotel.meituan.com',
    'Upgrade-Insecure-Requests': '1',
    'User-': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',

}
client = pymongo.MongoClient('localhost')
db = client['meituan']
def get_one_page(url, headers):
    try:
        response = requests.get(url=url, headers=headers)
        if len(response.text) > 5000:
            print('正在解析网页....')
            return response.json()
        if len(response.text) < 100:
            print('uuid不可用')
            return None
    except:
        return get_one_page(url, headers)

def pares_one_paeg(json):
    try:
        data = json.get('data')
        result = data.get('searchresult')
        for item in result:
            forward = item.get('forward')
            time = forward.get('poiExtendsInfosDesc')
            yield {
                'hotel': item.get('name'),
                'address': item.get('addr'),
                'url': 'http://hotel.meituan.com/'+ str(item.get('poiid')),
                'score': item.get('scoreIntro'),
                'consume': item.get('poiSaleAndSpanTag'),
                'commentcount': item.get('commentsCountDesc'),
                'time': time,
            }
    except:
        return None
def save_to_mongo(item, pinyin):
    try:
        if item:
            if db['hotel.'+ pinyin].update({'url': item['url']}, {'$set': item}, True):
                print('save_to_mongo 成功')
            else:
                print('save_to_mongo 失败')
    except:
        return None


def main(i):
    for item in city[0:10]:
        id = item.get('id')
        pinyin = item.get('pinyin')
        uuid = random.randint(1000000,9999999)
        statr_url = 'https://ihotel.meituan.com/hbsearch/HotelSearch?utm_medium=pc&version_name=999.9&cateId=20&attr_28=129&uuid=5B292AE1B1FD53A9BFC4CC79A04233C30CC096E5D7890AD49E4AF1A0F2964C69%40153535'
        url = statr_url +str(uuid)+ '&cityId=' + str(id) + '&offset=' + str(i) + '&limit=20&startDay=20180827&endDay=20180827&q=&sort=defaults'
        print(url)
        json = get_one_page(url, headers)
        for item in pares_one_paeg(json):
            save_to_mongo(item, pinyin)

if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i*20 for i in range(51)])