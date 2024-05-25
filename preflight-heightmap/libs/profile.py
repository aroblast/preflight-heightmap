import math
from .files import getAltitudeData
from ..types.coordinates import Coordinates


def getVector(a: Coordinates, b: Coordinates):
    return (b["lat"] - a["lat"], b["lon"] - a["lon"])


def getDistance(a: Coordinates, b: Coordinates):
    # Convert to radian
    lat1 = a["lat"] * math.pi / 180
    lat2 = b["lat"] * math.pi / 180
    lon1 = a["lon"] * math.pi / 180
    lon2 = b["lon"] * math.pi / 180

    # Precompute squares
    sinThetas = math.sin((lat2 - lat1) / 2)
    sinPhis = math.sin((lon2 - lon1) / 2)

    # return 3963.0 * math.acos(
    #     (math.sin(lat1) * math.sin(lat2))
    #     + math.cos(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)
    # )

    return (
        2
        * 6371
        * math.asin(
            math.sqrt(
                (sinThetas * sinThetas)
                + (math.cos(lat1) * math.cos(lat2) * sinPhis * sinPhis)
            )
        )
    ) / 1.852


def getProfile(points: list[Coordinates]):
    # Params
    subpointSteps = 0.2
    averageSteps = 10
    averageRadius = 5 / 60  # 1 NM to degrees
    averageStepSize = averageRadius / (averageSteps / 2)

    # Get bounds + 1° margin
    minLat = min(points, key=lambda x: x["lat"])["lat"] - 1
    minLon = min(points, key=lambda x: x["lon"])["lon"] - 1
    maxLat = max(points, key=lambda x: x["lat"])["lat"] + 1
    maxLon = max(points, key=lambda x: x["lon"])["lon"] + 1

    # Setup data
    allData = getAltitudeData(minLat, minLon, maxLat, maxLon)
    profile = []

    # Map points to elevations
    totalDistance = 0.0
    nextPoint: Coordinates
    for i in range(len(points)):
        point = points[i]
        nextPoint = points[i + 1] if i < len(points) - 1 else None
        (latDir, lonDir) = getVector(point, nextPoint) if nextPoint != None else (0, 0)
        distance = getDistance(point, nextPoint) if nextPoint != None else subpointSteps
        nbSubpoints = math.floor(distance / subpointSteps) + 1

        for subPointIndex in range(nbSubpoints):
            # Calculate subpoint lat / lon
            lat = point["lat"] + ((latDir / (nbSubpoints)) * subPointIndex)
            lon = point["lon"] + ((lonDir / (nbSubpoints)) * subPointIndex)

            # lonDataIndex = math.floor(lon) - math.floor(minLon)
            # latDataIndex = math.floor(lat) - math.floor(minLat)

            # # Get data based on index
            # (data, dim) = allData[lonDataIndex][latDataIndex]
            # steps = 1 / (dim - 1)

            # latIndex = dim - round((lat % 1) / steps) - 1
            # lonIndex = round((lon % 1) / steps) - 1
            # elevation = math.ceil(data[latIndex][lonIndex])

            # Calculate mean elevations
            elevation = []
            elevation1 = []
            elevation5 = []

            for deltaLat in range(averageSteps):
                for deltaLon in range(averageSteps):
                    latOffset = (deltaLat - (averageSteps / 2)) * averageStepSize
                    lonOffset = (
                        (deltaLon - (averageSteps / 2))
                        * averageStepSize
                        / math.cos(lat * math.pi / 180)
                    )  # Correct for latitude
                    avgPtLat = lat + latOffset
                    avgPtLon = lon + lonOffset

                    lonDataIndex = math.floor(avgPtLon) - math.floor(minLon)
                    latDataIndex = math.floor(avgPtLat) - math.floor(minLat)

                    # Get data based on index
                    (data, dim) = allData[lonDataIndex][latDataIndex]
                    steps = 1 / (dim - 1)

                    latIndex = dim - round((avgPtLat % 1) / steps) - 1
                    lonIndex = round((avgPtLon % 1) / steps) - 1
                    value = math.ceil(data[latIndex][lonIndex])

                    # Check point position to center
                    centered = (
                        abs(deltaLat - (averageSteps / 2)) < 1
                        and abs(deltaLon - (averageSteps / 2)) < 1
                    )
                    within1NM = abs(latOffset) <= (1 / 60) and abs(lonOffset) <= (
                        (1 / 60) / math.cos(lat * math.pi / 180)
                    )

                    if centered:
                        elevation.append(value if value > 0 else 0)

                    if within1NM:
                        elevation1.append(value if value > 0 else 0)

                    elevation5.append(value if value > 0 else 0)

            profile.append(
                {
                    "elevation": math.ceil(sum(elevation) / len(elevation)),
                    "elevation1": math.ceil(sum(elevation1) / len(elevation1)),
                    "elevation5": math.ceil(sum(elevation5) / len(elevation5)),
                    "distance": totalDistance + (subPointIndex * subpointSteps),
                }
            )

        # Store distance
        totalDistance += distance

    return profile
