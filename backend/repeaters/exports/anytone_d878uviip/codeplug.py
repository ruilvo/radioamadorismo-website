"""
Codeplug generation for the Anytone D878UVII+.
"""

import io
import zipfile


def codeplug_zip() -> io.BytesIO:
    """
    Makes a .zip file with the necessary csv files.
    """
    tgs_serializer = DimDmrTgAnytoneUVIIPlusSerializer()
    rx_group_call_list_serializer = ReceiveGroupCallListAnytoneUVIIPlusSerializer(
        tgs_serializer
    )
    channel_serializer = ChannelAnytoneUVIIPlusSerializer()
    zones_serializer = ZoneAnytoneUVIIPlusSerializer(channel_serializer)

    file_io = io.BytesIO()
    with zipfile.ZipFile(file_io, "w") as zip_file:
        for fname, fdata in (
            ("TalkGroups.csv", tgs_serializer),
            ("ReceiveGroupCallList.csv", rx_group_call_list_serializer),
            ("Channel.csv", channel_serializer),
            ("Zone.csv", zones_serializer),
        ):
            with zip_file.open(fname, "w") as csv_file:
                csv_file.write(fdata.generate_csv().getvalue().encode("utf-8"))

    return file_io
