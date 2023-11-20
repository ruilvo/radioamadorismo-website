"""
Serializer for Anytone D878UVII+ AutoRepeaterOffsetFrequencys.csv
"""

import io
import csv


def autorepeateroffsetfrequencys_csv() -> io.StringIO:
    """
    Generates a placeholder AutoRepeaterOffsetFrequencys.csv
    """

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")

    writer.writerow(["No.", "Offset Frequency"])
    writer.writerow(["1", "600.00 KHz"])
    writer.writerow(["2", "7.60000 MHz"])

    return sio
