# Local package imports
from .real_estate_utils import RealEstateUtils, FLOOR_TYPE

# Third party imports
import scrapy

class HousesSale4Zida(scrapy.Spider):
    name = "4zida-houses-sale"

    def __init__(self):
        self.current_link = 'https://4zida.rs/prodaja-stanova?search_source=home&strana=1'
        self.page_num = 1
        self.num_parsed_realestate_pages = 0

    def start_requests(self):
        urls = [
            'https://www.4zida.rs/prodaja/kuce/paracin-opstina/oglas/glavica/5e21e681273171283c0380b6',
            'https://www.4zida.rs/prodaja/kuce/cuprija-opstina/oglas/mijatovac/5e212fd427317159e165e947',
            'https://www.4zida.rs/prodaja/kuce/novi-sad/oglas/sremska-kamenica/5e53a7e027317145ee4c8ae3',
            'https://www.4zida.rs/prodaja/kuce/beograd/oglas/banjicka/5ed7effc27317169a23d31a3',
            'https://www.4zida.rs/prodaja/kuce/irig-opstina/oglas/stara-kolonija/5f36a9df0c7cde02c16213dd',
            'https://www.4zida.rs/prodaja/kuce/beograd/oglas/dusanovac/5eda22679a30911882747140',
            'https://www.4zida.rs/prodaja/kuce/novi-sad/oglas/telep/5e2218bb2731715c883b9d13',
            'https://www.4zida.rs/prodaja/kuce/novi-sad/oglas/adamovicevo-naselje/5f367d3dd0f0266eae4335ac'
            ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self._parse_real_estate_page)

    def parse(self, response):
        """
        # Getting the properties and opening their link page to parse data on the
        properties = self._get_all_real_estate_links(response)
        for prop_url_request in properties:
            sublink = prop_url_request.get() 
            # print(sublink)
            yield scrapy.Request(response.urljoin(sublink), callback=self._parse_real_estate_page)

        # Getting the link to next page (pagination)
        link_to_next_page = self._get_link_to_next_page(response)
        if link_to_next_page:
            # print(link_to_next_page)
            yield scrapy.Request(link_to_next_page, callback=self.parse)
        """

    def _parse_real_estate_page(self, response):
        property_data = RealEstateUtils.get_property_dictionary()
        try:
            property_data['listing_type'] = 's'
            property_data['property_type'] = 'h'
            property_data['price'] = self._get_price(response)
            property_data['location_city'] = self._get_location_city(response)
            property_data['location_city_district'] = self._get_location_district(response)
            property_data['area_property'] = self._get_area_of_property(response)
            property_data['area_land'] = self._get_area_of_land(response)
            property_data['construction_type'] = self._get_year_of_construction(response)
            property_data['registered'] = self._get_registration_info(response)     
            property_data['heating_type'] = self._get_heating_type(response)     
            property_data['num_rooms'] = self._get_num_of_rooms(response)     
            property_data['num_bathrooms'] = self._get_num_of_bathrooms(response)     
            property_data['source'] = response.request.url
        except Exception as e:
            yield None
            pass

        print(property_data)
        yield property_data
        self._log_progress()


    def _get_all_real_estate_links(self, response):
        return response.xpath('//div[@class="col-lg-8 card-classified-info"]/*/a[1]/@href')

    def _get_link_to_next_page(self, response):
        website_api = self.current_link.split('=')
        page_number = website_api[-1]
        website_api.remove(page_number)
        page_number = int(page_number)
        page_number += 1
        website_api.append(str(page_number))
        self.current_link = '='.join(website_api) 
        return self.current_link 

    def _log_progress(self):
        """Printing progress of scraped data."""
        self.num_parsed_realestate_pages += 1
        if self.num_parsed_realestate_pages % 20 == 0:
            # Informing on progress after every 20 scraped and processed web pages
            print('-' * 200)
            print(f'PARSED {self.num_parsed_realestate_pages} URLS OF REAL ESTATE DATA.')
            print('-' * 200)
        if self.num_parsed_realestate_pages > 20000:
            # Stopping scraper after 20,000 processed web pages
            raise scrapy.exceptions.CloseSpider(reason='SCRAPED OVER 20,000 WEB PAGES, STOPPING SPIDER...')

    def _get_price(self, response):
        price = response.xpath('//span[@class="pr-2"]/text()').get()
        if price:
            price = price.replace('.', '')
        return price

    def _get_location_city(self, response):
        city = response.xpath('//h3[@class="font-weight-light title-placeholder sub-title-placeholder-desktop ng-star-inserted"]/span/span[last()]/text()').get()
        if city:
            city = city.strip(', ')
        return city

    def _get_location_district(self, response):
        district = response.xpath('//h3[@class="font-weight-light title-placeholder sub-title-placeholder-desktop ng-star-inserted"]/span/span[last()-1]/text()').get()
        if district:
            district = district.strip(', ')
        return district

    def _get_area_of_property(self, response):
        area = response.xpath('//span[@itemprop="floorSize"]/text()').get()
        if area:
            area = area.split()[0]
            area = area.replace(',', '.')
        return area
    
    def _get_area_of_land(self, response):
        area = response.xpath('//div[div[text()="Plac oko kuće:"]]/div[last()]/span/text()').get()
        if area:
            area = area.strip()
            area = area.replace('a', '')
            area = float(area)
        return area

    def _get_year_of_construction(self, response):
        year = response.xpath('//div[div[text()="Godina izgradnje:"]]/div[last()]/span/text()').get()
        return year

    def _get_num_of_floors(self, response):
        num_of_floors = response.xpath('//div[span[text()="Sprat"]]/span[last()]/span[@itemprop="additionalProperty"]/text()').get()
        if num_of_floors:
            num_of_floors = num_of_floors.strip()
            num_of_floors = num_of_floors.replace('/', '')
            try:
                num_of_floors = int(num_of_floors)
            except ValueError as e:
                num_of_floors = None
        return num_of_floors

    def _get_apartment_floor(self, response):
        floor = response.xpath('//div[span[text()="Sprat"]]/span[last()]/text()').get()
        if floor:
            floor = floor.strip()
            floor = floor.lower()
            floor = floor.replace(' ', '')
            try:
                floor = int(floor)
            except ValueError as e:
                floor = RealEstateUtils.calculate_floor_value_based_on_type(floor)
        else:
            footer = response.xpath('//h5[@class="humanReadableText"]/text()').get()
            footer = footer.strip()
            footer = footer.lower()
            if 'prizemlju' in footer:
                return 0
        return floor

    def _get_registration_info(self, response):
        regitrated = response.xpath('//div[span[text()="Uknjiženost"]]/span[last()]/text()').get()
        if regitrated:
            return True
        else:
            return False

    def _get_heating_type(self, response):
        return response.xpath('//div[span[text()="Grejanje"]]/span[last()]/text()').get()

    def _get_num_of_rooms(self, response):
        return response.xpath('//div[span[text()="Broj soba"]]/span[last()]/text()').get()

    def _get_num_of_bathrooms(self, response):
        num_of_bathrooms_info = response.xpath('//div/span/span[@itemprop="numberOfRooms"]/text()')
        if num_of_bathrooms_info:
            num_of_bathrooms = num_of_bathrooms_info.re(r'\d+')
            if num_of_bathrooms and len(num_of_bathrooms) > 0:
                return num_of_bathrooms[0]
        return 1

    
    



