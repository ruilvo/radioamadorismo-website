"""
Serializer for Anytone D878UVII+ PrefabricatedSMS.csv
"""

import io
import csv


def prefabricatedsms_csv() -> io.StringIO:
    """
    Generates a placeholder PrefabricatedSMS.csv
    """

    header = ["No.", "Text"]

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")
    writer.writerow(header)

    content = ["1", "SOTA_REF FREQ_MHz MODE CALLSIGN COMMENT"]
    writer.writerow(content)

    return sio
