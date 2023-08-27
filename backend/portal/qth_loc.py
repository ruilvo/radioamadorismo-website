"""
Computes the QTH locator for a given latitude and longitude, or vice-versa.
"""

import string


def qthloc_from_latlon(latitude, longitude):
    """
    Computes a QTH locator from a given latitude and longitude.
    Uses the algorithm from https://www.clearskyinstitute.com/ham/HamClock/QSTGridSquares.pdf
    """

    qth_loc = ["Z", "Z", 0, 0, "z", "z"]

    # Field -> square -> subsquare

    # 1st longitude char.
    # -180 maps to A, +180 maps to R, steps of 20 deg.
    long_char1_index = int((longitude + 180) / 20)
    qth_loc[0] = string.ascii_uppercase[long_char1_index]

    # 2nd longitude char.
    # -20..0 and 0..+20 both map to 0..9, steps of 2 deg.
    # We start by computing the remainder of the division by 20.
    longitude_remainder = (longitude + 180) % 20
    # We then divide by 2 to get the index in the 0..9 range.
    long_char2 = int(longitude_remainder / 2)
    qth_loc[2] = long_char2

    # 3rd longitude char.
    # We start by computing the remainder of the division by 2.
    longitude_remainder = longitude_remainder % 2
    # Then, we convert the decimal degrees into minutes.
    longitude_minutes = longitude_remainder * 60
    # 0..+120 maps to A..X, steps of 5 min.
    long_char3_index = int(longitude_minutes / 5)
    qth_loc[4] = string.ascii_lowercase[long_char3_index]

    # 1st latitude char.
    # -90 maps to A, +90 maps to R, steps of 10 deg.
    lat_char1_index = int((latitude + 90) / 10)
    qth_loc[1] = string.ascii_uppercase[lat_char1_index]

    # 2nd latitude char.
    # -10..0 and 0..+10 both map to 0..9, steps of 1 deg.
    # We start by computing the remainder of the division by 10.
    latitude_remainder = (latitude + 90) % 10
    # We then divide by 1 to get the index in the 0..9 range.
    lat_char2 = int(latitude_remainder / 1)
    qth_loc[3] = lat_char2

    # 3rd latitude char.
    # We start by computing the remainder of the division by 1.
    latitude_remainder = latitude_remainder % 1
    # Then, we convert the decimal degrees into minutes.
    latitude_minutes = latitude_remainder * 60
    # 0..+60 maps to A..X, steps of 2.5 min.
    lat_char3_index = int(latitude_minutes / 2.5)
    qth_loc[5] = string.ascii_lowercase[lat_char3_index]

    return "".join([str(x) for x in qth_loc])


def qthloc_to_latlon(location):
    """
    Computes the latitude and longitude from a given QTH locator.
    """

    if not (len(location) == 4 or len(location) == 6):
        raise ValueError("The grid locator must be 4 or 6 characters long")

    longitude = 0.0

    # Field
    longitude += (ord(location[0].upper()) - ord("A")) * 20
    # Square
    longitude += int(location[2]) * 2
    # Subsquare
    if len(location) == 6:
        longitude_minutes = (ord(location[4]) - ord("a")) * 5
        longitude += longitude_minutes / 60

    latitude = 0.0

    # Field
    latitude += (ord(location[1].upper()) - ord("A")) * 10
    # Square
    latitude += int(location[3])
    # Subsquare
    if len(location) == 6:
        latitude_minutes = (ord(location[5]) - ord("a")) * 2.5
        latitude += latitude_minutes / 60

    return latitude - 90, longitude - 180


if __name__ == "__main__":
    print(f"Expected 'HM58oo', got {qthloc_from_latlon(38.59166667, -28.79750)}")
    print(f"Expected 'IM59mk', got {qthloc_from_latlon(39.434294440, -8.921988889)}")
    print(f"Expected '38.59166667, -28.79750', got {qthloc_to_latlon('HM58oo')}")
    print(f"Expected '39.434294440, -8.921988889', got {qthloc_to_latlon('IM59mk')}")
