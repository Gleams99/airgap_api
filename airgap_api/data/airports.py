
from airgap_api.data.models import AirGapBaseModel, AirportDataModel, AirportAttributesModel
from airgap_api.data.enums import AirportIATACodes, AirportDataType, AirportICAOCodes


class AirportsModel(AirGapBaseModel):
    MAG: AirportDataModel = AirportDataModel(
        id=AirportIATACodes.MAG,
        type=AirportDataType.Airport,
        attributes=AirportAttributesModel(
            name="Madang Airport",
            city="Madang",
            country="Papua New Guinea",
            iata=AirportIATACodes.MAG,
            icao=AirportICAOCodes.AYMD,
            latitude="-5.20708",
            longitude="145.789001",
            altitude=20,
            timezone="Pacific/Port_Moresby"
        )
    )
    CYG: AirportDataModel = AirportDataModel(
        id='CYG',
        type='airport',
        attributes=AirportAttributesModel(
            name='Corryong Airport',
            city=None,
            country='Australia',
            iata='CYG',
            icao='YCRG',
            latitude='-36.1828',
            longitude='147.888',
            altitude=963,
            timezone=None
        )

    )


Airports = AirportsModel()
