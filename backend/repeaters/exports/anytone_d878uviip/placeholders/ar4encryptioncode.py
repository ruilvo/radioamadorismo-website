"""
Serializer for Anytone D878UVII+ AR4EncryptionCode.csv
"""

import io
import csv


def ar4encryptioncode_csv() -> io.StringIO:
    """
    Generates a placeholder AR4EncryptionCode.csv
    """

    header = ["id", "aeskey"]

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")
    writer.writerow(header)

    for _ in range(255):
        writer.writerow(
            [
                "0",
                "          ",
            ]
        )

    return sio
