"""
On the Anytone D878UVII, names are limited to 16 chars.
"""

import io, csv, textwrap


from repeaters.models import (
    DimDmr,
    DimDmrTg,
)


class D878UVIIDialect(csv.excel):
    quotechar = "%"  # Just to make the package `csv` happy. This shouldn't happen.
    quoting = csv.QUOTE_NONE


csv.register_dialect("d878uvii", D878UVIIDialect)


def tgs_csv() -> io.StringIO:
    """
    Generates `TalkGroups.csv` as a StringIO object.
    """

    qs = DimDmrTg.objects.all()

    header = ['"No."', '"Radio ID"', '"Name"', '"Call Type"', '"Call Alert"']

    call_type_str = '"Group Call"'
    call_alert_str = '"None"'

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")
    writer.writerow(header)

    idx: int
    item: DimDmrTg
    for idx, item in enumerate(qs):
        writer.writerow(
            [
                f'"{idx+1}"',
                f'"{str(item.dmr_id):.16}"',
                f'"{str(item.name):.16}"',
                call_type_str,
                call_alert_str,
            ]
        )

    return sio


def receive_groups_csv() -> io.StringIO:
    """
    Generates `ReceiveGroupCallList.csv` as a StringIO.

    We'll be generating 2 groups:
     - The expected TS1 slot TGs
     - All TGs
    """

    ts1_default_tgs_qs = DimDmrTg.objects.filter(
        dimdmr_ts1_default_tg__isnull=False
    ).distinct()
    ts1_alternative_tgs_qs = DimDmrTg.objects.filter(
        dimdmr_ts1_alternative_tgs__in=DimDmr.objects.all()
    ).distinct()

    ts1_tgs_qs = (ts1_default_tgs_qs | ts1_alternative_tgs_qs).distinct()
    tgs_qs = DimDmrTg.objects.all()

    # RG's definition
    data_input = [
        ("TS1 Tipicos", ts1_tgs_qs),
        ("Todos TGs", tgs_qs),
    ]

    data = []
    for name, qs in data_input:
        contact = "|".join(f"{str(tg.name):.16}" for tg in qs)
        ids = "|".join(f"{str(tg.dmr_id):.16}" for tg in qs)
        data.append((name, contact, ids))

    header = ['"No."', '"Group Name"', '"Contact"', '"Contact TG/DMR ID"']

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")
    writer.writerow(header)

    for idx, (name, contact, ids) in enumerate(data):
        writer.writerow(
            [
                f'"{idx+1}"',
                f'"{name}"',
                f'"{contact}"',
                f'"{ids}"',
            ]
        )

    return sio


def radio_id_csv() -> io.StringIO:
    """
    Generates a placeholder RadioIDList.csv
    """

    header = ['"No."', '"Radio ID"', '"Name"']

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")
    writer.writerow(header)

    placeholder_radio_id = ("1", "268000", "CT0ZZZ")
    writer.writerow(
        [
            f'"{placeholder_radio_id[0]}"',
            f'"{placeholder_radio_id[1]}"',
            f'"{placeholder_radio_id[2]}"',
        ]
    )

    return sio


def scanlist_csv() -> io.StringIO:
    """
    Generates a placeholder ScanList.csv
    """

    header = [
        '"No."',
        '"Scan List Name"',
        '"Scan Channel Member"',
        '"Scan Channel Member RX Frequency"',
        '"Scan Channel Member TX Frequency"',
        '"Scan Mode"',
        '"Priority Channel Select"',
        '"Priority Channel 1"',
        '"Priority Channel 1 RX Frequency"',
        '"Priority Channel 1 TX Frequency"',
        '"Priority Channel 2"',
        '"Priority Channel 2 RX Frequency"',
        '"Priority Channel 2 TX Frequency"',
        '"Revert Channel"',
        '"Look Back Time A[s]"',
        '"Look Back Time B[s]"',
        '"Dropout Delay Time[s]"',
        '"Dwell Time[s]"',
    ]

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")
    writer.writerow(header)

    return sio


def roamingzone_csv() -> io.StringIO:
    """
    Generates a placeholder RoamingZone.csv
    """

    header = [
        '"No."',
        '"Name"',
        '"Roaming Channel Member"',
        "",
    ]

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")
    writer.writerow(header)

    return sio


def roaming_channel_csv() -> io.StringIO:
    """
    Generates a placeholder RoamingChannel.csv
    """

    header = [
        '"No."',
        '"Receive Frequency"',
        '"Transmit Frequency"',
        '"Color Code"',
        '"Slot"',
        '"Name"',
    ]

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")
    writer.writerow(header)

    return sio


def prefabricated_sms_csv() -> io.StringIO:
    """
    Generates a placeholder PrefabricatedSMS.csv
    """

    header = [
        '"No."',
        '"Text"',
    ]

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")
    writer.writerow(header)

    return sio
