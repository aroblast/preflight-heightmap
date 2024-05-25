import falcon
from ...libs.profile import getProfile


class ElevationProfileResource:
    def on_post(self, req: falcon.Request, resp: falcon.Response):
        """Handle POST requests."""

        points = req.media["points"]

        # Get point altitude
        profile = getProfile(points)

        # Response
        resp.status = falcon.HTTP_200
        resp.media = {
            "profile": profile,
        }
