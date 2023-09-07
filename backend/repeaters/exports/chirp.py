"""
Module to generate a CSV file for use in CHIRP.
"""

import io
import csv

from django.db.models import Q

from repeaters.models import FactRepeater, DimLocation, DimRf


def chirp_csv() -> io.StringIO:
    """
    Generates a CSV file for use with CHIRP as a StringIO object.
    """
    header = [
        "Location",
        "Name",
        "Frequency",
        "Duplex",
        "Offset",
        "Tone",
        "rToneFreq",
        "cToneFreq",
        "DtcsCode",
        "DtcsPolarity",
        "Mode",
        "TStep",
        "Skip",
        "Comment",
        "URCALL",
        "RPT1CALL",
        "RPT2CALL",
        "DVCODE",
    ]

    # Generate the querysets for the data that is going to be written to the CSV file.
    qss = [
        FactRepeater.objects.filter(  # Continent 2m FM
            Q(info_location__region=DimLocation.RegionOptions.CONTINENT)
            & Q(info_rf__band=DimRf.BandOptions.B_2M)
            & Q(modes__contains=[FactRepeater.ModeOptions.FM])
        ).order_by("-info_location__latitude"),
        FactRepeater.objects.filter(  # Continent 70cm FM
            Q(info_location__region=DimLocation.RegionOptions.CONTINENT)
            & Q(info_rf__band=DimRf.BandOptions.B_70CM)
            & Q(modes__contains=[FactRepeater.ModeOptions.FM])
        ).order_by("-info_location__latitude"),
        FactRepeater.objects.filter(  # Madeira 2m FM
            Q(info_location__region=DimLocation.RegionOptions.MADEIRA)
            & Q(info_rf__band=DimRf.BandOptions.B_2M)
            & Q(modes__contains=[FactRepeater.ModeOptions.FM])
        ).order_by("info_location__longitude"),
        FactRepeater.objects.filter(  # Madeira 70cm FM
            Q(info_location__region=DimLocation.RegionOptions.MADEIRA)
            & Q(info_rf__band=DimRf.BandOptions.B_70CM)
            & Q(modes__contains=[FactRepeater.ModeOptions.FM])
        ).order_by("info_location__longitude"),
        FactRepeater.objects.filter(  # Azores 2m FM
            Q(info_location__region=DimLocation.RegionOptions.AZORES)
            & Q(info_rf__band=DimRf.BandOptions.B_2M)
            & Q(modes__contains=[FactRepeater.ModeOptions.FM])
        ).order_by("info_location__longitude"),
        FactRepeater.objects.filter(  # Azores 70cm FM
            Q(info_location__region=DimLocation.RegionOptions.AZORES)
            & Q(info_rf__band=DimRf.BandOptions.B_70CM)
            & Q(modes__contains=[FactRepeater.ModeOptions.FM])
        ).order_by("info_location__longitude"),
    ]

    data = []

    index = 1

    def tone_or_67_0(ctcss):
        if ctcss:
            return f"{ctcss:.1f}"
        return "67.0"

    for qs in qss:
        for repeater in qs:
            # Create the data for the CSV file
            data.append(
                {
                    "Location": f"{index}",
                    "Name": f"{repeater.callsign}",
                    "Frequency": f"{repeater.info_rf.tx_mhz:.4f}",
                    "Duplex": "-",
                    "Offset": f"{repeater.info_rf.shift_mhz:.4f}",
                    "Tone": "Tone" if repeater.info_fm.ctcss else "",
                    "rToneFreq": tone_or_67_0(repeater.info_fm.ctcss),
                    "cToneFreq": tone_or_67_0(repeater.info_fm.ctcss),
                    "DtcsCode": "023",
                    "DtcsPolarity": "NN",
                    "Mode": "FM",  # TODO(ruilvo, 2023-08-22): Consider differentiating between FM and NFM.
                    "TStep": "6.25",
                    "Skip": "",
                    "Comment": f"{repeater.info_location.place}",
                    "URCALL": "",
                    "RPT1CALL": "",
                    "RPT2CALL": "",
                    "DVCODE": "",
                }
            )
            index = index + 1

    # Create the StringIO object
    sio = io.StringIO()
    writer = csv.writer(sio)

    writer.writerow(header)

    for row in data:
        writer.writerow(row.values())

    return sio
