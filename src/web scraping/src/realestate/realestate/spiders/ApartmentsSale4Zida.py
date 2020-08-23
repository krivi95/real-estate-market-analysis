# Local package imports
from .real_estate_utils import RealEstateUtils, FLOOR_TYPE

# Third party imports
import scrapy

class ApartmentsSale4Zida(scrapy.Spider):
    name = "4zida-apartments-sale"

    def start_requests(self):
        urls = [
            'https://4zida.rs/prodaja/stanovi/beograd/oglas/nodilova/5f2b0c3b0c7cde7aff2e19b4',
            'https://4zida.rs/prodaja/stanovi/beograd/oglas/bulevar-mihajla-pupina/5ed7e1c627317159674a7c93',
            'https://4zida.rs/prodaja/stanovi/novi-sad/oglas/novo-naselje/5e43eaa82731713f411b772d',
            'https://4zida.rs/prodaja/stanovi/novi-sad/oglas/sajmiste/5ed20e422731712afa741d53',
            'https://4zida.rs/prodaja/stanovi/beograd/oglas/bulevar-zorana-djindjica/5de67473273171036f55f433',
            'https://4zida.rs/prodaja/stanovi/novi-sad/oglas/centar-novi-sad/5f24ad520fa51a28d65e95ad',
            'https://4zida.rs/prodaja/stanovi/novi-sad/oglas/telep/5f1060d9c7765813446efbb5',
            'https://4zida.rs/prodaja/stanovi/subotica-opstina/oglas/centar-2/5ee379ce2731712e8c79d613',
            'https://4zida.rs/prodaja/stanovi/beograd/oglas/mihajla-pupina/5f3d5955c1ef9f42e90907ce',
            'https://4zida.rs/prodaja/stanovi/beograd/oglas/miloja-djaka/5f2d6c3a67b12c082f048137',
            'https://4zida.rs/prodaja/stanovi/beograd/oglas/miloja-djaka/5d51bd492731712f3e7dfa87'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        property_data = RealEstateUtils.get_property_dictionary()
        try:
            property_data['listing_type'] = 's'
            property_data['property_type'] = 'a'
            property_data['price'] = self._get_price(response)
            property_data['location_city'] = self._get_location_city(response)
            property_data['location_city_district'] = self._get_location_district(response)
            property_data['area_property'] = self._get_area_of_property(response)
            property_data['construction_type'] = self._get_year_of_construction(response)
            property_data['num_floors_building'] = self._get_num_of_floors(response)
            property_data['apartment_floor'] = self._get_apartment_floor(response)
            property_data['registered'] = self._get_registration_info(response)     
            property_data['heating_type'] = self._get_heating_type(response)     
            property_data['num_rooms'] = self._get_num_of_rooms(response)     
            property_data['num_bathrooms'] = self._get_num_of_bathrooms(response)     
        except Exception as e:
            yield None

        yield property_data

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

    
    



