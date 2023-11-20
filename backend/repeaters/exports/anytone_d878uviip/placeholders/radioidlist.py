"""
Serializer for Anytone D878UVII+ RadioIDList.csv
"""

import csv
import io


def radioidlist_csv() -> io.StringIO:
    """
    Generates a placeholder RadioIDList.csv
    """

    header = ["No.", "Radio ID", "Name"]

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")
    writer.writerow(header)

    placeholder_radio_id = ("1", "268000", "CT0ZZZ")
    writer.writerow(
        [
            f"{placeholder_radio_id[0]}",
            f"{placeholder_radio_id[1]}",
            f"{placeholder_radio_id[2]}",
        ]
    )

    return sio
