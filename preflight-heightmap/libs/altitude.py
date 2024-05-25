import os
import math
import numpy


def getAltitude(lat: float, lon: float) -> float:
    """Get altitude of point at coordinates."""

    baseLat = math.floor(lat)
    baseLon = math.floor(lon)
    fileName = f"preflight-heightmap/data/{'S' if baseLat < 0 else 'N'}{abs(baseLat)}{'W' if baseLon < 0 else 'E'}{abs(baseLon):03}.hgt"

    # Get file size
    size = os.path.getsize(fileName)
    dim = int(math.sqrt(size / 2))

    # Make sure file is square
    assert dim * dim * 2 == size, "Invalid file size"

    # Get steps and data
    steps = 1 / (dim - 1)
    data = numpy.fromfile(fileName, numpy.dtype(">i2"), dim * dim).reshape((dim, dim))

    # Get values nearest to point
    latIndex = dim - round((lat - baseLat) / steps) - 1
    lonIndex = round((lon - baseLon) / steps) - 1
    altitudes = [
        data[min(dim - 1, max(0, latIndex + i))][min(dim - 1, max(0, lonIndex + j))]
        for j in range(-1, 2)
        for i in range(-1, 2)
    ]

    # Average all altitudes to conteract lack of resolution
    altitudeAvg = sum(altitudes) / len(altitudes)

    return altitudeAvg
