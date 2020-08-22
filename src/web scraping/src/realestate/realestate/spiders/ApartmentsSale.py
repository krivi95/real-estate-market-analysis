# Importing third party libraries
import scrapy
from scrapy_selenium import SeleniumRequest

class ApartmentsSale(scrapy.Spider):
    """Spider class for scraping data about apartments for sale."""
    name = "apartments-sale"

    def start_requests(self):
        urls = [
            'https://halooglasi.com/nekretnine/prodaja-stanova/lux-stan-na-crvenom-krstu-bez-provizije/5425615521968?kid=4&sid=1598031139346'
            'https://www.halooglasi.com/nekretnine/prodaja-stanova/novi-beograd-a-blok-savada-65m2-uknjizen-id15/5425635628505?kid=4&sid=1598076525379',
            'https://www.halooglasi.com/nekretnine/prodaja-stanova/novi-beograd-a-blok-savada-dvosoban-uknjizen/5425635628506?kid=4&sid=1598076525379',
            'https://www.halooglasi.com/nekretnine/prodaja-stanova/vidikovac-dvoiposoban-stan-72m2/5425635846342?sid=1598076525379',
            'https://www.halooglasi.com/nekretnine/prodaja-stanova/extra-lux-stanovi-kod-tempa--bez-provizije/5425635770671?kid=4&sid=1598076525379',
            'https://www.halooglasi.com/nekretnine/prodaja-stanova/lux-stan-kod-tempa-bez-provizije/5425635712613?sid=1598076525379',
            'https://www.halooglasi.com/nekretnine/prodaja-stanova/renoviran-penthouse-stojana-aralice-bez-kosa/5425635448086?kid=4&sid=1598076525379',
            'https://www.halooglasi.com/nekretnine/prodaja-stanova/dedinje-lux-polunamesten-id-14277/5425635656706?kid=4&sid=1598076525379',
            'https://www.halooglasi.com/nekretnine/prodaja-stanova/stan-od-100m2-u-naselju-west65/5425635500690?kid=4&sid=1598076525379',
            'https://www.halooglasi.com/nekretnine/prodaja-stanova/vozdovac-lekino-brdo---mazuraniceva/5425635651683?kid=4&sid=1598076525379',
            'https://www.halooglasi.com/nekretnine/prodaja-stanova/beograd-na-vodi-parkview-30m2-id1417/5425635623734?kid=4&sid=1598076525379',
            'https://www.halooglasi.com/nekretnine/prodaja-stanova/aparatman-zlatibor-top-lokacija/5425635767030?kid=4&sid=1598076525379',
            'https://www.halooglasi.com/nekretnine/prodaja-stanova/aparatman-zlatibor-top-lokacija/5425635767030?kid=4&sid=1598076525379',
            'https://www.halooglasi.com/nekretnine/prodaja-stanova/uknjizeni-lux-sa-gradjevinskom-dozvolom/5425635204765?kid=4&sid=1598076525379',
            'https://www.halooglasi.com/nekretnine/prodaja-stanova/stari-grad-dorcol-skender-begova-3-0-70m2/5425635837079?kid=4&sid=1598076525379',
            'https://www.halooglasi.com/nekretnine/prodaja-stanova/stari-grad-dorcol-skender-begova-3-0-70m2/5425635837079?kid=4'
        ]
        for url in urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        embeded_location = response.xpath('//div[@class="widget-operator-panel widget-operator-panel widget-operator-panel"]/script').re(r'44.\d+,20.\d+')[0]

        yield {
            'listing_type': 'a',
            'price': response.xpath('//span[@class="offer-price-value"]/text()').get(),
            'location_city': response.xpath('//span[@data-code="grad"]/text()').get(),
            'location_city_district': response.xpath('//span[@data-code="lokacija"]/text()').get(),
            'location_lat': embeded_location.split(',')[0],
            'location_long': embeded_location.split(',')[1],
            'area_property': response.xpath('//span[@id="plh12"]/text()').get().split()[0],
            'construction_type': response.xpath('//span[@id="plh15"]/text()').get(),
            'num_floors_building': response.xpath('//span[@id="plh19"]/text()').get(),
            'apartment_floor': response.xpath('//span[@id="plh18"]/text()').get(),
            'registered': True if response.xpath('//label[text()="Uknjižen"]').get() else False,
            'heating_type': response.xpath('//span[@id="plh17"]/text()').get(),
            'num_rooms': response.xpath('//span[@id="plh13"]/text()').get(),
            'source': response.request.url
            }
