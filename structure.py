import pydantic

class HttpsLog(pydantic.BaseModel):
    method: str
    url: str
    requestBody: str = ''
    responseBody: str = ''