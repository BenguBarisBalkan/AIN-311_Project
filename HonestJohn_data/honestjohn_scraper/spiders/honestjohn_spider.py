import scrapy
from scrapy.http import HtmlResponse

class HonestJohnSpider(scrapy.Spider):
    name = 'honestjohn'
    start_urls = ['https://www.honestjohn.co.uk/real-mpg/']

    def parse(self, response: HtmlResponse):
        # Marka listesini bul
        make_list = response.css('ul.makeListThreeCol')
        brands = make_list.css('a')

        # Her marka için dön
        for brand in brands:
            brand_name = brand.css('::text').get().strip()
            print(brand_name)
            brand_link = brand.css('::attr(href)').get()

            # Marka linkine tıkla
            yield scrapy.Request(url=response.urljoin(brand_link), callback=self.parse_brand)

    def parse_brand(self, response: HtmlResponse):
        # Model listesini bul
        model_list = response.css('div.col12-12.pane-row')
        models = model_list.css('a')

        # Her model için dön
        for model in models:
            model_link = model.css('::attr(href)').get()

            # Model sayfasını aç ve MPG değerini al
            yield scrapy.Request(url=response.urljoin(model_link), callback=self.parse_model)

    def parse_model(self, response: HtmlResponse):
        # Model sayfasından veri çekme kodları
        mpg_value = response.css('div.mpgValue::text').get()

        yield {
            'Brand': response.css('h1::text').get(),
            'Model': response.url.split('/')[-1],
            'MPG': mpg_value,
        }