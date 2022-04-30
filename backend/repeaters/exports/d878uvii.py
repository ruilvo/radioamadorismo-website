"""
On the Anytone D878UVII, names are limited to 16 chars.
"""

import io
import csv

from django.db.models import Q

from repeaters.models import (
    DimDmr,
    DimDmrTg,
    FactRepeater,
)

from repeaters.filters import rf_search, freq_mhz_search__gte, freq_mhz_search__lte


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


def channel_csv() -> io.StringIO:
    """
    Generates a Channel.csv
    """

    # First we need to get only compatible repeaters

    class Band2m:
        min = 144.0
        max = 146.0

    class Band70cm:
        min = 430.0
        max = 440.0

    qs = FactRepeater.objects.all()

    qs_hd = qs.filter(info_half_duplex__isnull=False)
    qs_sp = qs.filter(info_simplex__isnull=False)

    # Rx between 144.0 and 146.0 OR between 430.0 and 440.0
    q_hd_rx_2m = Q(info_half_duplex__rx_mhz__gte=Band2m.min) & Q(
        info_half_duplex__rx_mhz__lte=Band2m.max
    )
    q_hd_rx_70cm = Q(info_half_duplex__rx_mhz__gte=Band70cm.min) & Q(
        info_half_duplex__rx_mhz__lte=Band70cm.max
    )
    q_hd_rx = q_hd_rx_2m | q_hd_rx_70cm
    # AND Tx between 144.0 and 146.0 OR between 430.0 and 440.0
    q_hd_tx_2m = Q(info_half_duplex__tx_mhz__gte=Band2m.min) & Q(
        info_half_duplex__tx_mhz__lte=Band2m.max
    )
    q_hd_tx_70cm = Q(info_half_duplex__tx_mhz__gte=Band70cm.min) & Q(
        info_half_duplex__tx_mhz__lte=Band70cm.max
    )
    q_hd_tx = q_hd_tx_2m | q_hd_tx_70cm
    # AND
    q_hd = q_hd_rx & q_hd_tx

    # For simplex it's just TRx between 144.0 and 146.0 OR between 430.0 and 440.0
    q_sp_2m = Q(info_simplex__freq_mhz__gte=Band2m.min) & Q(
        info_simplex__freq_mhz__lte=Band2m.max
    )
    q_sp_70cm = Q(info_simplex__freq_mhz__gte=Band70cm.min) & Q(
        info_simplex__freq_mhz__lte=Band70cm.max
    )
    q_sp = q_sp_2m | q_sp_70cm
    # And filter
    qs_hd = qs_hd.filter(q_hd)
    qs_sp = qs_sp.filter(q_sp)

    # Repeaters also need to have either FM or DMR information
    qs_hd_fm = qs_hd.filter(info_fm__isnull=False)
    qs_hd_dmr = qs_hd.filter(info_dmr__isnull=False)
    qs_sp_fm = qs_sp.filter(info_fm__isnull=False)
    qs_sp_dmr = qs_sp.filter(info_dmr__isnull=False)

    # Due to the way the DB is set, the 1750Hz tone is considered a "tone".
    # Let's filter for only standard tones.
    # This is just a dirty protection, in the future a list would be nice.
    cutoff = 500.0
    qs_hd_fm = qs_hd_fm.filter(info_fm__tone__lte=cutoff)
    qs_sp_fm = qs_sp_fm.filter(info_fm__tone__lte=cutoff)

    # Now that these conditions are met, we can generate the CSV

    header = [
        '"No."',
        '"Channel Name"',
        '"Receive Frequency"',
        '"Transmit Frequency"',
        '"Channel Type"',
        '"Transmit Power"',
        '"Band Width"',
        '"CTCSS/DCS Decode"',
        '"CTCSS/DCS Encode"',
        '"Contact"',
        '"Contact Call Type"',
        '"Contact TG/DMR ID"',
        '"Radio ID"',
        '"Busy Lock/TX Permit"',
        '"Squelch Mode"',
        '"Optional Signal"',
        '"DTMF ID"',
        '"2Tone ID"',
        '"5Tone ID"',
        '"PTT ID"',
        '"Color Code"',
        '"Slot"',
        '"Scan List"',
        '"Receive Group List"',
        '"PTT Prohibit"',
        '"Reverse"',
        '"Simplex TDMA"',
        '"Slot Suit"',
        '"AES Digital Encryption"',
        '"Digital Encryption"',
        '"Call Confirmation"',
        '"Talk Around(Simplex)"',
        '"Work Alone"',
        '"Custom CTCSS"',
        '"2TONE Decode"',
        '"Ranging"',
        '"Through Mode"',
        '"APRS RX"',
        '"Analog APRS PTT Mode"',
        '"Digital APRS PTT Mode"',
        '"APRS Report Type"',
        '"Digital APRS Report Channel"',
        '"Correct Frequency[Hz]"',
        '"SMS Confirmation"',
        '"Exclude channel from roaming"',
        '"DMR MODE"',
        '"DataACK Disable"',
        '"R5toneBot"',
        '"R5ToneEot"',
        '"Auto Scan"',
        '"Ana Aprs Mute"',
        '"Send Talker Alias"',
    ]

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")
    writer.writerow(header)

    elem: FactRepeater
    count = 0
    # FM
    qs_fm = qs_hd_fm | qs_sp_fm
    for elem in qs_fm:
        count = count + 1
        rx_freq = (
            elem.info_half_duplex.tx_mhz
            if elem.info_half_duplex != None
            else elem.info_simplex.freq_mhz
        )
        tx_freq = (
            elem.info_half_duplex.rx_mhz
            if elem.info_half_duplex != None
            else elem.info_simplex.freq_mhz
        )
        writer.writerow(
            [
                f'"{count}"',  # No.
                f'"{str(elem.callsign):.16}"',  # Channel Name
                f'"{rx_freq:.5f}"',  # Receive Frequency
                f'"{tx_freq:.5f}"',  # Transmit Frequency
                '"A-Analog"',  # Channel Type
                '"High"',  # Transmit Power
                f'"{"12.5K" if elem.info_fm.bandwidth=="NFM" else "25K"}"',  # Band Width
                '"Off"',  # CTCSS/DCS Decode
                f'"{elem.info_fm.tone:.1f}"',  # CTCSS/DCS Encode
                '"Portugal"',  # Contact
                '"Group Call"',  # Contact Call Type
                '"268"',  # Contact TG/DMR ID
                '"CT0ZZZ"',  # Radio ID
                '"Off"',  # Busy Lock/TX Permit
                '"Carrier"',  # Squelch Mode
                '"Off"',  # Optional Signal
                '"1"',  # DTMF ID
                '"1"',  # 2Tone ID
                '"1"',  # 5Tone ID
                '"Off"',  # PTT ID
                '"1"',  # Color Code
                '"1"',  # Slot
                '"None"',  # Scan List
                '"None"',  # Receive Group List
                '"Off"',  # PTT Prohibit
                '"Off"',  # Reverse
                '"Off"',  # Simplex TDMA
                '"Off"',  # Slot Suit
                '"Normal Encryption"',  # AES Digital Encryption
                '"Off"',  # Digital Encryption
                '"Off"',  # Call Confirmation
                '"Off"',  # Talk Around(Simplex)
                '"Off"',  # Work Alone
                '"251.1"',  # Custom CTCSS
                '"1"',  # 2TONE Decode
                '"Off"',  # Ranging
                '"On"',  # Through Mode
                '"Off"',  # APRS RX
                '"Off"',  # Analog APRS PTT Mode
                '"Off"',  # Digital APRS PTT Mode
                '"Off"',  # APRS Report Type
                '"1"',  # Digital APRS Report Channel
                '"0"',  # Correct Frequency[Hz]
                '"Off"',  # SMS Confirmation
                '"0"',  # Exclude channel from roaming
                '"0"',  # DMR MODE
                '"0"',  # DataACK Disable
                '"0"',  # R5toneBot
                '"0"',  # R5ToneEot
                '"0"',  # Auto Scan
                '"0"',  # Ana Aprs Mute
                '"0"',  # Send Talker Alias
            ]
        )
    # DMR
    qs_dmr = qs_hd_dmr | qs_sp_dmr
    for elem in qs_dmr:
        rx_freq = (
            elem.info_half_duplex.tx_mhz
            if elem.info_half_duplex != None
            else elem.info_simplex.freq_mhz
        )
        tx_freq = (
            elem.info_half_duplex.rx_mhz
            if elem.info_half_duplex != None
            else elem.info_simplex.freq_mhz
        )
        if elem.info_dmr.ts1_default_tg is not None:
            ts1_contact = elem.info_dmr.ts1_default_tg.name
            ts1_id = str(elem.info_dmr.ts1_default_tg.dmr_id)
        else:
            ts1_contact = "Portugal"
            ts1_id = "268"
        if elem.info_dmr.ts2_default_tg is not None:
            ts2_contact = elem.info_dmr.ts2_default_tg.name
            ts2_id = str(elem.info_dmr.ts2_default_tg.dmr_id)
        else:
            ts2_contact = "Local"
            ts2_id = "2"
        # ("TS1 Tipicos", ts1_tgs_qs),
        # ("Todos TGs", tgs_qs),
        for ts_n, ts_contact, ts_id, rgl in [
            ("1", ts1_contact, ts1_id, "TS1 Tipicos"),
            ("2", ts2_contact, ts2_id, "Todos TGs"),
        ]:
            count = count + 1
            writer.writerow(
                [
                    f'"{count}"',  # No.
                    f'"{str(elem.callsign) + " TS" + ts_n:.16}"',  # Channel Name
                    f'"{rx_freq:.5f}"',  # Receive Frequency
                    f'"{tx_freq:.5f}"',  # Transmit Frequency
                    '"D-Digital"',  # Channel Type
                    '"High"',  # Transmit Power
                    '"12.5K"',  # Band Width
                    '"Off"',  # CTCSS/DCS Decode
                    '"Off"',  # CTCSS/DCS Encode
                    f'"{ts_contact}"',  # Contact
                    '"Group Call"',  # Contact Call Type
                    f'"{ts_id}"',  # Contact TG/DMR ID
                    '"CT0ZZZ"',  # Radio ID
                    '"Always"',  # Busy Lock/TX Permit
                    '"Carrier"',  # Squelch Mode
                    '"Off"',  # Optional Signal
                    '"1"',  # DTMF ID
                    '"1"',  # 2Tone ID
                    '"1"',  # 5Tone ID
                    '"Off"',  # PTT ID
                    f'"{str(elem.info_dmr.color_code)}"',  # Color Code
                    f'"{ts_n}"',  # Slot
                    '"None"',  # Scan List
                    f'"{rgl}"',  # Receive Group List
                    '"Off"',  # PTT Prohibit
                    '"Off"',  # Reverse
                    '"Off"',  # Simplex TDMA
                    '"Off"',  # Slot Suit
                    '"Normal Encryption"',  # AES Digital Encryption
                    '"Off"',  # Digital Encryption
                    '"Off"',  # Call Confirmation
                    '"Off"',  # Talk Around(Simplex)
                    '"Off"',  # Work Alone
                    '"251.1"',  # Custom CTCSS
                    '"1"',  # 2TONE Decode
                    '"Off"',  # Ranging
                    '"On"',  # Through Mode
                    '"Off"',  # APRS RX
                    '"Off"',  # Analog APRS PTT Mode
                    '"Off"',  # Digital APRS PTT Mode
                    '"Off"',  # APRS Report Type
                    '"1"',  # Digital APRS Report Channel
                    '"0"',  # Correct Frequency[Hz]
                    '"Off"',  # SMS Confirmation
                    '"0"',  # Exclude channel from roaming
                    '"1"',  # DMR MODE
                    '"0"',  # DataACK Disable
                    '"0"',  # R5toneBot
                    '"0"',  # R5ToneEot
                    '"0"',  # Auto Scan
                    '"0"',  # Ana Aprs Mute
                    '"0"',  # Send Talker Alias
                ]
            )

    return sio
