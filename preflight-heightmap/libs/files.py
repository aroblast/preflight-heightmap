import os
import math
import numpy


def getFileData(fileName: str):
    size = os.path.getsize(fileName)
    dim = int(math.sqrt(size / 2))

    # Make sure file is square
    assert dim * dim * 2 == size, "Invalid file size"

    # Get data
    data = numpy.fromfile(fileName, numpy.dtype(">i2"), dim * dim).reshape((dim, dim))

    return (data, dim)


def getAltitudeData(
    minLat: float, minLon: float, maxLat: float | None, maxLon: float | None
):
    """Get altitude of point at coordinates."""

    baseMinLat = math.floor(minLat)
    baseMinLon = math.floor(minLon)
    baseMaxLat = math.floor(maxLat)
    baseMaxLon = math.floor(maxLon)

    fileNames = [
        [
            f"preflight-heightmap/data/{'S' if lat < 0 else 'N'}{abs(lat)}{'W' if lon < 0 else 'E'}{abs(lon):03}.hgt"
            for lat in range(baseMinLat, baseMaxLat + 1)
        ]
        for lon in range(baseMinLon, baseMaxLon + 1)
    ]

    # Get files data
    data = [[getFileData(fileName) for fileName in row] for row in fileNames]

    return data
