# Importing third party libraries
import scrapy
from scrapy_selenium import SeleniumRequest

class ApartmentsSale(scrapy.Spider):
    """Spider class for scraping data about apartments for sale."""
    name = "apartments-sale"

    def start_requests(self):
        urls = [
            'https://halooglasi.com/nekretnine/prodaja-stanova'
        ]
        for url in urls:
            yield SeleniumRequest(url=url, callback=self.parse)


    def parse(self, response):
        """Parsing the page containing links"""
        
        # Getting the properties and opening their link page to parse data on the
        properties = response.xpath('//h3[@class="product-title"]/a/@href')
        for prop in properties:
            sublink = prop.get() 
            yield SeleniumRequest(response.urljoin(sublink), callback=self.parse_realestate_page)

        # Getting the link to next page (pagination)
        next_page = response.xpath('//a[@class="page-link next"]/@href').get()
        yield SeleniumRequest(response.urljoin(next_page), callback=self.parse)

    def parse_realestate_page(self, response):
        """Parsing real estate data - property page."""

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
