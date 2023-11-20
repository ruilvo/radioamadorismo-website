"""
Serializer for Anytone D878UVII+ AnalogAddressBook.csv
"""

import io
import csv


def analogaddressbook_csv() -> io.StringIO:
    """
    Generates a placeholder AnalogAddressBook.csv
    """

    header = ["No.", "Number", "Name"]

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")
    writer.writerow(header)

    return sio
