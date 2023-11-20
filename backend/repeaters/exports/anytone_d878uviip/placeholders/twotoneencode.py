"""
Serializer for Anytone D878UVII+ 2ToneEncode.csv
"""

import csv
import io


def twotoneencode_csv() -> io.StringIO:
    """
    Generates a placeholder 2ToneEncode.csv
    """

    header = ["NO.", "1st Tone Frequency[Hz]", "2nd Tone Frequency[Hz]", "Name"]

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")
    writer.writerow(header)

    return sio
