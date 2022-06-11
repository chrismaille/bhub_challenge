from uvicorn.workers import UvicornWorker


class NoLifespanUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {"loop": "auto", "http": "auto", "lifespan": "off"}
