import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

class CianSpider(scrapy.Spider):
    name = "cian"
    start_urls = ["https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=1&region=1"]
    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.cian.ru/'
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)
    def parse(self, response):
        # Извлечение цен
        prices = response.css('.price::text').getall()

        # Извлечение названий
        names = response.css('.description::text').getall()

        # Извлечение местоположений
        locations = response.css('.location::text').getall()

        # Сохранение данных в JSON-файл
        data = []
        for price, name, location in zip(prices, names, locations):
            data.append({
                'Цена': price.strip(),
                'Название': name.strip(),
                'Местоположение': location.strip()
            })

        return data

if __name__ == "__main__":
    # Настройки Scrapy
    settings = Settings()
    settings.set('FEEDS', {
        'cian_flats.json': {
            'format': 'json',
            'encoding': 'utf8',
            'tore_empty': False,
            'fields': None,
            'overwrite': True,
        },
    })
    settings.set('LOG_ENABLED', True)

    # Запуск процесса сбора данных
    process = CrawlerProcess(settings)
    process.crawl(CianSpider)
    process.start()
