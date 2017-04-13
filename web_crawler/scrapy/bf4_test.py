import urllib.request
import urllib.parse
import re
from bs4 import BeautifulSoup

# Pattern 1:
# <div class="a-fixed-left-grid-col a-col-right" style="padding-left:2%;*width:97.6%;float:left;">
# 	<div class="a-row sx-badge-region"></div>
# 	<div class="a-row a-spacing-small">
# 		<div class="a-row a-spacing-none">
# 			<a class="a-link-normal s-access-detail-page  a-text-normal" title="LEGO Technic Mercedes-Benz Arocs 3245 42043 Building Kit" href="https://www.amazon.com/LEGO-Technic-Mercedes-Benz-Arocs-Building/dp/B01FAPFFCC/ref=sr_1_1?ie=UTF8&amp;qid=1488886835&amp;sr=8-1&amp;keywords=lego+42043">
# 				<h2 data-attribute="LEGO Technic Mercedes-Benz Arocs 3245 42043 Building Kit" data-max-rows="0" data-truncate-by-character="false" class="a-size-medium a-color-null s-inline  s-access-title  color-variation-title-replacement a-text-normal">
# 					LEGO Technic Mercedes-Benz Arocs 3245 42043 Building Kit
# 				</h2>
# 			</a>
# 		</div>
# 		<div class="a-row a-spacing-none"><span class="a-size-small a-color-secondary">by </span>
# 		<span class="a-size-small a-color-secondary">LEGO</span>
# 	</div>
# </div>
# <div class="a-row">
# 	<div class="a-column a-span7">
# 		<div class="a-row a-spacing-none">
# 			<a class="a-link-normal a-text-normal" href="https://www.amazon.com/LEGO-Technic-Mercedes-Benz-Arocs-Building/dp/B01FAPFFCC/ref=sr_1_1?ie=UTF8&amp;qid=1488886835&amp;sr=8-1&amp;keywords=lego+42043">
# 				<span aria-label="$212.49" class="a-color-base sx-zero-spacing">
# 					<span class="sx-price sx-price-large">
#                     	<sup class="sx-price-currency">$</sup>
#                     	<span class="sx-price-whole">212</span>
#                     	<sup class="sx-price-fractional">49</sup>
#                 	</span>
#             	</span>
#             </a>
# =====================================
# Pattern 2:
# <div class="a-fixed-left-grid-col a-col-right" style="padding-left:2%;*width:97.6%;float:left;">
# 	<div class="a-row sx-badge-region"></div>
# 	<div class="a-row a-spacing-small">
# 		<div class="a-row a-spacing-none"><a class="a-link-normal s-access-detail-page  a-text-normal" title="LEGO TECHNIC Container Truck 8052" href="https://www.amazon.com/LEGO-TECHNIC-Container-Truck-8052/dp/B003F7WOFO/ref=sr_1_28/162-7485620-2024301?ie=UTF8&amp;qid=1488890065&amp;sr=8-28&amp;keywords=lego+42043">
# 			<h2 data-attribute="LEGO TECHNIC Container Truck 8052" data-max-rows="0" data-truncate-by-character="false" class="a-size-medium a-color-null s-inline  s-access-title  color-variation-title-replacement a-text-normal">
# 				LEGO TECHNIC Container Truck 8052
# 			</h2>
# 		</a>
# 	</div>
# 	<div class="a-row a-spacing-none">
# 		<span class="a-size-small a-color-secondary">by </span>
# 		<span class="a-size-small a-color-secondary">LEGO</span>
# 	</div>
# </div>
# <div class="a-row">
# 	<div class="a-column a-span7">
# 		<div class="a-row a-spacing-mini">
# 			<div class="a-row a-spacing-none">
# 				<a class="a-size-small a-link-normal a-text-normal" href="https://www.amazon.com/gp/offer-listing/B003F7WOFO/ref=sr_1_28_olp/162-7485620-2024301?ie=UTF8&amp;qid=1488890065&amp;sr=8-28&amp;keywords=lego+42043&amp;condition=new">
# 					<span class="a-color-secondary a-text-strike"></span>
# 					<span class="a-size-base a-color-base">$525.45</span>
# 					<span class="a-letter-space"></span>
# 					(1 new offer)
# 				</a>
# 			</div>

class Amazon(object):
    def urlEncodeNonAscii(self, b):
        if b is None:
            return ''
        return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

    def iriToUri(self, iri):
        parts = urllib.parse.urlparse(iri)
        print(parts)

        new_uri = urllib.parse.urlunparse(
            part.encode('idna') if parti == 1 else self.urlEncodeNonAscii(part)
            for parti, part in enumerate(parts)
        )

        print(type(new_uri))
        print(new_uri)
        return new_uri

        # return urllib.parse.urlunparse(
        #     part.encode('idna') if parti == 1 else self.urlEncodeNonAscii(part)
        #     for parti, part in enumerate(parts)
        # )

    def __init__(self):
        self.rate = {'us': 0, 'uk': 0, 'de': 0}
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}

        self.amazons = {
            'uk': ('https://www.amazon.co.uk/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=lego+',
                   self.get_page_items_uk),
            'us': ('https://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=lego+',
                   self.get_page_items_us),
            'de': ('https://www.amazon.de/s/ref=nb_sb_noss_2?' +
                   urllib.parse.urlencode({'__mk_de_DE': 'ÅMÅŽÕÑ', 'url': 'search-alias%3Daps'}) +
                   '&field-keywords=lego+',
                   self.get_page_items_de)
        }

    def get_page(self, url, filter):
        try:
            # request = urllib.request.Request(self.iriToUri(url), headers=self.headers)
            request = urllib.request.Request(url+filter, headers=self.headers)
            response = urllib.request.urlopen(request)
            page_code = response.read().decode('utf-8')
            # print(page_code)

            return page_code
        except urllib.error.URLError as e:
            if hasattr(e, "reason"):
                print(u"连接失败,错误原因", e.reason)
                return None

    def get_page_items_uk(self, url, filter):
        page_code = self.get_page(url, filter)
        if not page_code:
            print("页面加载失败....")
            return None
        soup = BeautifulSoup(page_code, "lxml")
        soup.prettify()
        for result in soup.findAll('li', id=re.compile("result_\d+$")):
            name = result.find('h2')
            price = result.find('span', class_=re.compile("a-color-price"))
            if price is None:
                price = result.find('span', class_=re.compile("a-text-strike"))

            if filter not in name.text:
                continue

            rmb = float(price.text[1:]) * self.rate['uk'] / 100
            print(result['id'], name.text, price.text, "%0.2f" % rmb)

    def get_page_items_us(self, url, filter):
        page_code = self.get_page(url, filter)

        if not page_code:
            print("页面加载失败....")
            return None

        soup = BeautifulSoup(page_code, "lxml")
        soup.prettify()
        for result in soup.findAll('li', id=re.compile("result_\d+$")):
            name = result.find('h2')
            currency = result.find('sup', class_=re.compile("sx-price-currency"))
            price_whole = result.find('span', class_=re.compile("sx-price-whole"))
            price_fractional = result.find('sup', class_=re.compile("sx-price-fractional"))
            if currency is None:
                # print( result.find('span', class_=re.compile("a-size-base")))
                price = result.find('span', class_=re.compile("a-size-base")).text
            else:
                price = currency.text + price_whole.text + '.' + price_fractional.text

            if filter not in name.text:
                continue

            rmb = float(price[1:]) * self.rate['us'] / 100
            print(result['id'], name.text, price, "%0.2f" % rmb)

    def get_page_items_de(self, url, filter):
        page_code = self.get_page(url, filter)
        if not page_code:
            print("页面加载失败....")
            return None
        soup = BeautifulSoup(page_code, "lxml")
        soup.prettify()
        for result in soup.findAll('li', id=re.compile("result_\d+$")):
            name = result.find('h2')
            price = result.find('span', class_=re.compile("a-color-price"))

            if filter not in name.text:
                continue

            rmb = float(price.text[4:].replace(',', '.')) * self.rate['de'] / 100
            print(result['id'], name.text, price.text, "%0.2f" % rmb)

    def get_rate(self):
        page_code = self.get_page(u'http://www.boc.cn/sourcedb/whpj/', '')
        if not page_code:
            print("页面加载失败....")
            return None
        soup = BeautifulSoup(page_code, "lxml")
        soup.prettify()
        for result in soup.findAll('div', class_=re.compile("main"), id='DefaultMain'):
            for sibling in result.find_next_siblings():
                for tr in sibling.findAll('tr'):
                    rate = tr.findAll('td')
                    if len(rate) < 4:
                        continue
                    elif rate[0].text == u'英镑':
                        self.rate['uk'] = float(rate[3].text)
                    elif rate[0].text == u'欧元':
                        self.rate['de'] = float(rate[3].text)
                    elif rate[0].text == u'美元':
                        self.rate['us'] = float(rate[3].text)

    def start(self, pn):
        self.get_rate()
        for key, value in self.amazons.items():
            print(key + ": " + str(self.rate[key]))
            (url, method) = value
            method(url, pn)

if __name__ == '__main__':
    models = ['42043', '10255', '42055', '10220']
    spider = Amazon()
    for model in models:
        print(model)
        spider.start(model)