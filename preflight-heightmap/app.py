import falcon
from .routes.elevation.elevationPoint import ElevationPointResource
from .routes.elevation.elevationProfile import ElevationProfileResource

# Setup cache
app = application = falcon.App()
app.add_route("/v1/elevation/profile", ElevationProfileResource())
app.add_route("/v1/elevation/{lat}/{lon}", ElevationPointResource())
