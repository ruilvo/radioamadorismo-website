"""
Serializer for Anytone D878UVII+ AESEncryptionCode.csv
"""

import io
import csv


def aesencryptioncode_csv() -> io.StringIO:
    """
    Generates a placeholder AESEncryptionCode.csv
    """

    header = ["id", "num", "aeskey"]

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")
    writer.writerow(header)

    for _ in range(255):
        writer.writerow(
            [
                "0",
                "0",
                "0                                                               ",
            ]
        )

    return sio
