"""
Serializer for Anytone D878UVII+ DTMFEncode.csv
"""

import io
import csv


def dtmfencode_csv() -> io.StringIO:
    """
    Generates a placeholder DTMFEncode.csv
    """

    header = ["DTMF ID", "DTMF Encode"]

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")
    writer.writerow(header)

    return sio
