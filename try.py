url = 'https://ihotel.meituan.com/hbsearch/HotelSearch?utm_medium=pc&version_name=999.9&cateId=20&attr_28=129&uuid=5B292AE1B1FD53A9BFC4CC79A04233C30CC096E5D7890AD49E4AF1A0F2964C69%401535356656569&cityId=50&offset=20&limit=20&startDay=20180827&endDay=20180827&q=&sort=defaults'
headers = {'user-agent':'Mozilla/5.0'}
import requests
req = requests.get(url=url,headers=headers)
print(req.text)