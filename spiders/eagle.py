import scrapy
from protego import Protego
from bs4 import BeautifulSoup
import requests


class EagleSpider(scrapy.Spider):
    name = 'eagle'
    start_urls = []
    url = "https://www.goodreads.com/list/show/6.Best_Books_of_the_20th_Century?page="
    for x in range(1, 2):
        new_url = url + str(x)
        res = requests.get(new_url)
        bs = BeautifulSoup(res.content, "html.parser")
        tags = bs.find_all("a", class_="bookTitle", href=True)
        for y in tags:
            first = 'https://www.goodreads.com'
            start_urls.append(first + y['href'])

    def parse(self, response, **kwargs):
        print("#" * 100)
        for data in response.css("#metacol"):
            yield {
                "name": data.xpath('//*[@id="bookTitle"]/text()').get().replace("\n", "").lstrip(),
                "writer": data.css("a.authorName span::text").get(),
                "rate": data.css("#bookMeta > span:nth-child(2)::text").get().replace("\n", "").lstrip(),
                "plot": data.xpath('/html/body/div[2]/div[3]/div[1]/div[2]/div[4]/div[1]/div[2]/div[3]/div/span['
                                   '*]/text()').get(),
                "lang": data.xpath('//*[@id="bookDataBox"]/div[3]/div[2]/text()').get().replace("/n", "").strip(),
                "char": data.css('span.toggleContent a::text').getall()[:-1],
                "setting": data.xpath('/html/body/div[2]/div[3]/div[1]/div[2]/div[4]/div[1]/div[2]/div[5]/div[3]/div['
                                      '1]/div[6]/a/text()').get(),
                "litery award": data.css('div.infoBoxRowItem a.award::text').getall(),
                "link": response.request.url
            }

        # print(response.css("title::text").get())
        # print(response.xpath("//title/text()").get())

        # next_page = response.css("li.next a::attr(href)").get()
        # if next_page:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(url=next_page, callback=self.parse)
