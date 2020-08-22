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
            'https://www.halooglasi.com/nekretnine/prodaja-stanova/extra-extra-lux-stanovi-na-vozdovcu--bez-prov/5425635146102?kid=4&sid=1598110387082',
            'https://www.halooglasi.com/nekretnine/prodaja-stanova/extra-garsonjera---tasmajdan---bez-provizije/5425635810031?kid=4&sid=1598110387082',
            'https://www.halooglasi.com/nekretnine/prodaja-stanova/5-0-miloja-djaka-dedinje-245m2/5425635625522?kid=4&sid=1598110434524'
        ]
        for url in urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        # Determining GPS coordinates of property
        embeded_location = response.xpath('//div[@class="widget-operator-panel widget-operator-panel widget-operator-panel"]/script').re(r'44.\d+,20.\d+')
        if len(embeded_location) > 0:
            embeded_location = embeded_location[0]
        else:
            embeded_location = None

        # Determining apartment floor
        apartment_floor = response.xpath('//span[@id="plh18"]/text()').get()
        if apartment_floor:
            try:
                apartment_floor = int(apartment_floor)
            except ValueError as e:
                if apartment_floor == 'PR':
                    apartment_floor = 0
                elif apartment_floor == 'VPR':
                    apartment_floor = 0.5
                elif apartment_floor == 'PSUT' or apartment_floor == 'SUT':
                    apartment_floor = -1

        yield {
            'listing_type': 'a',
            'price': response.xpath('//span[@class="offer-price-value"]/text()').get().replace('.', ''),
            'location_city': response.xpath('//span[@data-code="grad"]/text()').get(),
            'location_city_district': response.xpath('//span[@data-code="lokacija"]/text()').get(),
            'location_lat': embeded_location.split(',')[0] if embeded_location is not None else None,
            'location_long': embeded_location.split(',')[1] if embeded_location is not None else None,
            'area_property': response.xpath('//span[@id="plh12"]/text()').get().split()[0].replace(',', '.') if response.xpath('//span[@id="plh12"]/text()').get() else None,
            'construction_type': response.xpath('//span[@id="plh15"]/text()').get(),
            'num_floors_building': response.xpath('//span[@id="plh19"]/text()').get(),
            'apartment_floor': apartment_floor,
            'registered': True if response.xpath('//label[text()="Uknjižen"]').get() else False,
            'heating_type': response.xpath('//span[@id="plh17"]/text()').get(),
            'num_rooms': response.xpath('//span[@id="plh13"]/text()').get(),
            'source': response.request.url
            }
