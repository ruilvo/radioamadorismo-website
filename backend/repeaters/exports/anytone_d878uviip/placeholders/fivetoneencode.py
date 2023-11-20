"""
Serializer for Anytone D878UVII+ 5ToneEncode.csv
"""

import io
import csv


def fivetoneencode_csv() -> io.StringIO:
    """
    Generates a placeholder 5ToneEncode.csv
    """

    header = [
        "NO.",
        "Encode ID",
        "Encode/Decode Standard",
        "Time Of Encode Tone[ms]",
        "Name",
    ]

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")
    writer.writerow(header)

    return sio
