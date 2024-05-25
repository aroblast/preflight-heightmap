import falcon
from ...libs.altitude import getAltitude


class ElevationPointResource:
    def on_get(self, _: falcon.Request, resp: falcon.Response, lat: str, lon: str):
        """Handle GET requests."""

        latFloat = float(lat)
        lonFloat = float(lon)

        # Get point altitude
        altitude = getAltitude(latFloat, lonFloat)

        # Response
        resp.status = falcon.HTTP_200
        resp.media = {
            "altitude": altitude,
        }
