import pandas
import requests

from Classes.Address import AddressCreate
from Classes.Establishment import EstablishmentCreate
from DataBase.EstablishmentsTable import EstablishmentsTable


class ParserAddressToCoordinates:
    YANDEX_MAPS_API_KEY = "22955a5e-740a-4850-8379-1439a844b941"
    BASE_URL = "https://geocode-maps.yandex.ru/1.x"

    def get_coordinates(self, address: str) -> tuple[float, float] | None:
        params = {
            'apikey': self.YANDEX_MAPS_API_KEY,
            'geocode': address,
            'format': 'json'
        }

        try:
            response = requests.get(self.BASE_URL, params=params)
            data = response.json()
            pos = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
            longitude, latitude = map(float, pos.split())
            return latitude, longitude
        except Exception:
            return None


class ParserEstablishmentsData:
    def write_establishments_data(self, path_to_data):
        df = pandas.read_excel(path_to_data)
        result = df.to_dict("records")
        for establishment in result:
            params = {}
            for key, value in establishment.items():
                if value:
                    params[key] = str(value)
            if "address" in params:
                parser = ParserAddressToCoordinates()
                latitude, longitude = parser.get_coordinates(establishment["address"])
                address = AddressCreate(address=establishment["address"],
                                        latitude=latitude,
                                        longitude=longitude)
                params["address"] = address
            if "rating" in params:
                params["rating"] = round(float(establishment["rating"]), 2)
            if establishment["count_comment"]:
                params["count_comment"] = int(establishment["count_comment"])

            establishment_create = EstablishmentCreate(**params)
            establishment_repository = EstablishmentsTable()
            establishment_repository.add_establishment(establishment_create)


if __name__ == "__main__":
    parser = ParserEstablishmentsData()
    parser.write_establishments_data("EstablishmentsData.xlsx")
