import  xmltodict
import requests

r = requests.get("https://www.homedepot.com/sitemap/d/pip_sitemap.xml",headers={"User-Agent":"Mozilla/5.0"})
xml = r.text
raw = xmltodict.parse(xml)

pages  = []
urls = [] # parents 
prod_links = [] # child

for info in raw['sitemapindex']['sitemap']:
    url = info['loc']
    if 'https://www.homedepot.com/sitemap/d/pip/' in url:
        urls.append(url)

for l in urls:
    print(l)
    req = requests.get(l,headers={"User-Agent":"Mozilla/5.0"})
    xml_prod = req.text
    raw_prod = xmltodict.parse(xml_prod)
    #print(raw_prod['urlset'])
    if 'urlset' in raw_prod:
        for info in raw_prod['urlset']['url']:
            prod_link = info['loc']
            if 'https://www.homedepot.com/p/' in prod_link:
                prod_links.append(prod_link)
    else:
        continue


if len(prod_links)>0:
    with open('./output/links_file_0.txt', 'a+', encoding='utf8') as f:
        f.write('\n'.join(prod_links))

