from pydantic import BaseModel, ConfigDict, TypeAdapter


class AirGapBaseModel(BaseModel):
    model_config = ConfigDict(extra='ignore', use_enum_values=True)


class AirportAttributesModel(AirGapBaseModel):
    name: str
    city: str | None
    country: str
    iata: str
    icao: str
    latitude: str
    longitude: str
    altitude: int
    timezone: str | None


class AirportDataModel(AirGapBaseModel):
    id: str
    type: str
    attributes: AirportAttributesModel


class ErrorResponseModel(AirGapBaseModel):
    status: str
    title: str
    detail: str


class ErrorListResponseModel(AirGapBaseModel):
    errors: list[ErrorResponseModel]


class AirportDistanceAttributesModel(AirportAttributesModel):
    id: int


class AirportDistanceResultAttributesModel(AirGapBaseModel):
    from_airport: AirportDistanceAttributesModel
    to_airport: AirportDistanceAttributesModel
    kilometers: float
    miles: float
    nautical_miles: float


class AirportDistanceResultModel(AirGapBaseModel):
    id: str
    type: str
    attributes: AirportDistanceResultAttributesModel


class FavoriteAirportAttributesModel(AirportAttributesModel):
    id: int


class FavoriteAirportModel(AirGapBaseModel):
    airport: FavoriteAirportAttributesModel
    note: str


class FavoriteModel(AirGapBaseModel):
    id: str
    type: str
    attributes: FavoriteAirportModel


AirportDataPageResponse = TypeAdapter(list[AirportDataModel])
FavoriteAirportDataPageResponse = TypeAdapter(list[FavoriteModel])
