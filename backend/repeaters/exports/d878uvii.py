"""
On the Anytone D878UVII, names are limited to 16 chars.
"""

import io, csv


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

    tgs_qs = DimDmrTg.objects.all()

    tgs_header = ['"No."', '"Radio ID"', '"Name"', '"Call Type"', '"Call Alert"']
    call_type_str = '"Group Call"'
    call_alert_str = '"None"'

    tg_sio = io.StringIO()
    tg_writer = csv.writer(tg_sio, dialect="d878uvii")
    tg_writer.writerow(tgs_header)

    idx: int
    item: DimDmrTg
    for idx, item in enumerate(tgs_qs):
        tg_writer.writerow(
            [
                f'"{idx+1}"',
                f'"{str(item.dmr_id):.16}"',
                f'"{str(item.name):.16}"',
                call_type_str,
                call_alert_str,
            ]
        )

    return tg_sio


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
    rgs_input = [
        ("TS1 Tipicos", ts1_tgs_qs),
        ("Todos TGs", tgs_qs),
    ]

    rgs_data = []
    for rg_name, rg_qs in rgs_input:
        rg_contact = "|".join(f"{str(tg.name):.16}" for tg in rg_qs)
        rg_ids = "|".join(f"{str(tg.dmr_id):.16}" for tg in rg_qs)
        rgs_data.append((rg_name, rg_contact, rg_ids))

    rgs_header = ['"No."', '"Group Name"', '"Contact"', '"Contact TG/DMR ID"']

    rgs_sio = io.StringIO()
    rgs_writer = csv.writer(rgs_sio, dialect="d878uvii")
    rgs_writer.writerow(rgs_header)

    for idx, (rg_name, rg_contact, rg_ids) in enumerate(rgs_data):
        rgs_writer.writerow(
            [
                f'"{idx+1}"',
                f'"{rg_name}"',
                f'"{rg_contact}"',
                f'"{rg_ids}"',
            ]
        )

    return rgs_sio
