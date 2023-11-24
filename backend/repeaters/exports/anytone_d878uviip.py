"""
Codeplug generation for the Anytone D878UVII+.
"""

import io
import csv
import zipfile

from enum import StrEnum
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import requests

from django.db.models import Q
from django.db.models.manager import BaseManager

from unidecode import unidecode

from repeaters.models import (
    DimLocation,
    DimRf,
    DimFm,
    DimDmr,
    DimDmrTg,
    FactRepeater,
)


class CSVDialect(csv.excel):
    quotechar = '"'
    quoting = csv.QUOTE_ALL


csv.register_dialect("d878uviiplus", CSVDialect)

_CPT = DimLocation.RegionOptions.CONTINENT
_MDA = DimLocation.RegionOptions.MADEIRA
_AZR = DimLocation.RegionOptions.AZORES
_B_2M = DimRf.BandOptions.B_2M
_B_70CM = DimRf.BandOptions.B_70CM
_FM = FactRepeater.ModeOptions.FM
_DMR = FactRepeater.ModeOptions.DMR
_NFM = DimFm.BandwidthOptions.NFM
_WFM = DimFm.BandwidthOptions.WFM
_GROUP_CALL = DimDmrTg.CallModeOptions.GROUP_CALL
_PRIVATE_CALL = DimDmrTg.CallModeOptions.PRIVATE_CALL

_MAXIMUM_CHANNELS_PER_SCAN_ZONE = 48
_MAXIMUM_TGS_PER_RX_LIST = 64
_MAXIMUM_CHANNELS_PER_ROAMING_ZONE = 64


class ChannelMode(StrEnum):
    FM = "A-Analog"
    DMR = "D-Digital"


class CallType(StrEnum):
    GROUP = "Group Call"
    PRIVATE = "Private Call"


@dataclass
class RoamingChannel:
    idx: int
    rx_mhz: float
    tx_mhz: float
    cc: int
    slot: int
    name: str

    def serialize(self) -> List[str]:
        return [
            f"{self.idx}",  # "No."
            f"{self.rx_mhz:.5f}",  # "Receive Frequency"
            f"{self.rx_mhz:.5f}",  # "Transmit Frequency"
            f"{self.cc}",  # "Color Code"
            f"{self.slot}",  # "Slot"
            self.name,  # "Name"
        ]


@dataclass
class RoamingZone:
    idx: int
    name: str
    channels: list[RoamingChannel] = field(default_factory=lambda: [])

    def serialize(self) -> List[str]:
        return [
            f"{self.idx}",  # "No."
            self.name,  # "Name"
            "|".join(
                [channel.name for channel in self.channels]
            ),  # "Roaming Channel Member"
        ]


@dataclass
class TalkGroup:
    idx: int
    radio_id: int
    name: str
    call_type: CallType = CallType.GROUP

    def serialize(self) -> List[str]:
        return [
            f"{self.idx}",  # "No."
            f"{self.radio_id}",  # "Radio ID"
            self.name,  # "Name"
            self.call_type,  # "Call Type"
            "None",  # "Call Alert"
        ]


@dataclass
class RadioId:
    idx: int
    radio_id: int
    name: str

    def serialize(self) -> List[str]:
        return [
            f"{self.idx}",  # "No."
            f"{self.radio_id}",  # "Radio ID"
            self.name,  # "Name"
        ]


@dataclass
class ScanList:
    idx: int
    name: str
    channels: list["Channel"] = field(default_factory=lambda: [])

    def serialize(self) -> List[str]:
        return [
            f"{self.idx}",  # "No."
            self.name,  # "Scan List Name"
            "|".join([c.name for c in self.channels]),  # "Scan Channel Member"
            "|".join(
                f"{c.rx_mhz:.5f}" for c in self.channels
            ),  # "Scan Channel Member RX Frequency"
            "|".join(
                f"{c.tx_mhz:.5f}" for c in self.channels
            ),  # "Scan Channel Member TX Frequency"
            "Off",  # "Scan Mode"
            "Off",  # "Priority Channel Select"
            "Off",  # "Priority Channel 1"
            "",  # "Priority Channel 1 RX Frequency"
            "",  # "Priority Channel 1 TX Frequency"
            "Off",  # "Priority Channel 2"
            "",  # "Priority Channel 2 RX Frequency"
            "",  # "Priority Channel 2 TX Frequency"
            "Selected",  # "Revert Channel"
            "2.0",  # "Look Back Time A[s]"
            "3.0",  # "Look Back Time B[s]"
            "3.1",  # "Dropout Delay Time[s]"
            "3.1",  # "Dwell Time[s]"
        ]


@dataclass
class RxList:
    idx: int
    name: str
    tgs: list[TalkGroup] = field(default_factory=lambda: [])

    def serialize(self) -> List[str]:
        return [
            f"{self.idx}",  # "No."
            self.name,  # "Group Name"
            "|".join([tg.name for tg in self.tgs]),  # "Contact"
            "|".join(f"{tg.radio_id}" for tg in self.tgs),  # "Contact TG/DMR ID"
        ]


@dataclass
class Channel:
    idx: int
    name: str
    rx_mhz: float
    tx_mhz: float
    mode: ChannelMode
    tg: TalkGroup
    radio_id: RadioId
    scan_list: ScanList
    rx_list: RxList
    bw: str = _NFM
    ctcss: Optional[float] = None
    color_code: int = 1
    slot: int = 1

    def serialize(self) -> List[str]:
        bw = "12.5K" if self.bw == _NFM else "25K"
        ctcss = "Off" if not self.ctcss else f"{self.ctcss:.1f}"
        scan_list = "None" if not self.scan_list else self.scan_list.name
        rx_list = "None" if not self.rx_list else self.rx_list.name  # TODO: implement
        send_talker_alias = "0" if self.mode == ChannelMode.FM else "1"
        return [
            f"{self.idx}",  # "No."
            self.name,  # "Channel Name"
            f"{self.rx_mhz:.5f}",  # "Receive Frequency"
            f"{self.tx_mhz:.5f}",  # "Transmit Frequency"
            self.mode,  # "Channel Type"
            "High",  # "Transmit Power"
            bw,  # "Band Width"
            "Off",  # "CTCSS/DCS Decode"
            ctcss,  # "CTCSS/DCS Encode"
            self.tg.name,  # "Contact"
            self.tg.call_type,  # "Contact Call Type"
            self.tg.radio_id,  # "Contact TG/DMR ID"
            self.radio_id.name,  # "Radio ID"
            "Off",  # "Busy Lock/TX Permit"
            "Carrier",  # "Squelch Mode"
            "Off",  # "Optional Signal"
            "1",  # "DTMF ID"
            "1",  # "2Tone ID"
            "1",  # "5Tone ID"
            "Off",  # "PTT ID"
            f"{self.color_code}",  # "Color Code"
            f"{self.color_code}",  # "Slot"
            scan_list,  # "Scan List"
            rx_list,  # "Receive Group List"
            "Off",  # "PTT Prohibit"
            "Off",  # "Reverse"
            "Off",  # "Simplex TDMA"
            "Off",  # "Slot Suit"
            "Normal Encryption",  # "AES Digital Encryption"
            "Off",  # "Digital Encryption"
            "Off",  # "Call Confirmation"
            "Off",  # "Talk Around(Simplex)"
            "Off",  # "Work Alone"
            "251.1",  # "Custom CTCSS"
            "1",  # "2TONE Decode"
            "Off",  # "Ranging"
            "On",  # "Through Mode"
            "Off",  # "APRS RX"
            "Off",  # "Analog APRS PTT Mode"
            "Off",  # "Digital APRS PTT Mode"
            "Off",  # "APRS Report Type"
            "1",  # "Digital APRS Report Channel"
            "0",  # "Correct Frequency[Hz]"
            "Off",  # "SMS Confirmation"
            "0",  # "Exclude channel from roaming"
            "0",  # "DMR MODE"
            "0",  # "DataACK Disable"
            "0",  # "R5toneBot"
            "0",  # "R5ToneEot"
            "0",  # "Auto Scan"
            "0",  # "Ana Aprs Mute"
            send_talker_alias,  # "Send Talker Alias"
            "0",  # "AnaAprsTxPath"
            "0",  # "ARC4"
            "0",  # "ex_emg_kind"
        ]


@dataclass
class Zone:
    idx: int
    name: str
    channels: list[Channel] = field(default_factory=lambda: [])

    def serialize(self) -> List[str]:
        return [
            f"{self.idx}",  # "No."
            self.name,  # "Zone Name"
            "|".join([c.name for c in self.channels]),  # "Zone Channel Member"
            "|".join(
                f"{c.rx_mhz:.5f}" for c in self.channels
            ),  # "Zone Channel Member RX Frequency"
            "|".join(
                f"{c.tx_mhz:.5f}" for c in self.channels
            ),  # "Zone Channel Member TX Frequency"
            self.channels[0].name,  # "A Channel"
            f"{self.channels[0].rx_mhz:.5f}",  # "A Channel RX Frequency"
            f"{self.channels[0].tx_mhz:.5f}",  # "A Channel TX Frequency"
            self.channels[0].name,  # "B Channel"
            f"{self.channels[0].rx_mhz:.5f}",  # "B Channel RX Frequency"
            f"{self.channels[0].tx_mhz:.5f}",  # "B Channel TX Frequency"
            "0",  # "Zone Hide "
        ]


@dataclass
class GPSRoamingChannel:
    idx: int
    zone: Zone
    latitude: float
    longitude: float
    radius: int

    @property
    def latitude_degrees(self) -> int:
        return abs(int(self.latitude))

    @property
    def latitude_minutes(self):
        return (abs(self.latitude) - self.latitude_degrees) * 60

    @property
    def latitude_minutes_integer_part(self) -> int:
        return int(self.latitude_minutes)

    @property
    def latitude_minutes_decimal_part(self) -> int:
        return int((self.latitude_minutes - self.latitude_minutes_integer_part) * 100)

    @property
    def latitude_hemisphere(self) -> str:
        if self.latitude > 0:
            return "0"
        return "1"

    @property
    def longitude_degrees(self) -> int:
        return abs(int(self.longitude))

    @property
    def longitude_minutes(self):
        return (abs(self.longitude) - self.longitude_degrees) * 60

    @property
    def longitude_minutes_integer_part(self) -> int:
        return int(self.longitude_minutes)

    @property
    def longitude_minutes_decimal_part(self) -> int:
        return int((self.longitude_minutes - self.longitude_minutes_integer_part) * 100)

    @property
    def longitude_hemisphere(self) -> str:
        if self.longitude > 0:
            return "0"
        return "1"

    def serialize(self) -> List[str]:
        return [
            "1",  # "OnOff"
            f"{self.zone.idx}",  # "Zone"
            f"{self.latitude_degrees}",  # "Latitude Degree"
            self.latitude_hemisphere,  # "North or South"
            self.longitude_degrees,  # "Longtitude Degree"
            self.longitude_hemisphere,  # "East or West"
            f"{self.latitude_minutes_integer_part:02.2f}",  # "Latitude Minute"
            f"{self.latitude_minutes_decimal_part:02.2f}",  # "Latitude Minute1"
            f"{self.longitude_minutes_integer_part:02.2f}",  # "Longtitude Minute"
            f"{self.longitude_minutes_decimal_part:02.2f}",  # "Longtitude Minute1"
            "30000",  # "Radius(Meter)"
        ]


# 23
# 0,"Channel.CSV"  -> ChannelCSVSerializer
# 1,"RadioIDList.CSV"  -> RadioIDListCSVSerializer
# 2,"Zone.CSV"  -> ZoneCSVSerializer
# 3,"ScanList.CSV"  -> ScanListCSVSerializer
# 4,"AnalogAddressBook.CSV"  -> AnalogAddressBookCSVSerializer
# 5,"TalkGroups.CSV"  -> TalkGroupsCSVSerializer
# 6,"PrefabricatedSMS.CSV"  -> PrefabricatedSMSCSVSerializer
# 7,"FM.CSV"  -> FMCSVSerializer
# 8,"ReceiveGroupCallList.CSV"  -> ReceiveGroupCallListCSVSerializer
# 9,"5ToneEncode.CSV"  -> FiveToneEncodeCSVSerializer
# 10,"2ToneEncode.CSV"  -> TwoToneEncodeCSVSerializer
# 11,"DTMFEncode.CSV"  -> DTMFEncodeCSVSerializer
# 12,"HotKey_QuickCall.CSV"
# 13,"HotKey_State.CSV"
# 14,"HotKey_HotKey.CSV"
# 15,"DigitalContactList.CSV"  -> DigitalContactListCSVSerializer
# 16,"AutoRepeaterOffsetFrequencys.CSV"  -> AutoRepeaterOffsetFrequencysCSVSerializer
# 17,"RoamingChannel.CSV"  -> RoamingChannelCSVSerializer
# 18,"RoamingZone.CSV"  -> RoamingZoneCSVSerializer
# 19,"APRS.CSV"  -> APRSCSVSerializer
# 20,"GPSRoaming.CSV"
# 21,"AESEncryptionCode.CSV"  -> AESEncryptionCodeCSVSerializer
# 22,"AR4EncryptionCode.CSV"  -> AR4EncryptionCodeCSVSerializer


class AR4EncryptionCodeCSVSerializer:
    @property
    def filename(self) -> str:
        return "AR4EncryptionCode.CSV"

    def write(self) -> io.StringIO:
        sio = io.StringIO()
        writer = csv.writer(sio, dialect="d878uviiplus")

        header = ["id", "aeskey"]

        writer.writerow(header)

        for _ in range(255):
            writer.writerow(
                [
                    "0",
                    "          ",
                ]
            )

        return sio


class AESEncryptionCodeCSVSerializer:
    @property
    def filename(self) -> str:
        return "AESEncryptionCode.CSV"

    def write(self) -> io.StringIO:
        sio = io.StringIO()
        writer = csv.writer(sio, dialect="d878uviiplus")

        header = ["id", "num", "aeskey"]

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


class AutoRepeaterOffsetFrequencysCSVSerializer:
    @property
    def filename(self) -> str:
        return "AutoRepeaterOffsetFrequencys.CSV"

    def write(self) -> io.StringIO:
        sio = io.StringIO()
        writer = csv.writer(sio, dialect="d878uviiplus")

        header = ["No.", "Offset Frequency"]

        writer.writerow(header)

        rows = [
            ["1", "600.00 KHz"],
            ["2", "7.60000 MHz"],
        ]
        for row in rows:
            writer.writerow(row)

        return sio


class AnalogAddressBookCSVSerializer:
    @property
    def filename(self) -> str:
        return "AnalogAddressBook.CSV"

    def write(self) -> io.StringIO:
        sio = io.StringIO()
        writer = csv.writer(sio, dialect="d878uviiplus")

        header = ["No.", "Number", "Name"]

        writer.writerow(header)

        return sio


class APRSCSVSerializer:
    @property
    def filename(self) -> str:
        return "APRS.CSV"

    def write(self) -> io.StringIO:
        sio = io.StringIO()
        writer = csv.writer(sio, dialect="d878uviiplus")

        header = [
            "Manual TX Interval[s]",
            "APRS Auto TX Interval[s]",
            "Support For Roaming",
            "Fixed Location Beacon",
            "LatiDegree",
            "LatiMinInt",
            "LatiMinMark",
            "North or South",
            "LongtiDegree",
            "LongtiMinInt",
            "LongtiMinMark",
            "East or West Hemisphere",
            "channel1",
            "slot1",
            "Aprs Tg1",
            "Call Type1",
            "channel2",
            "slot2",
            "Aprs Tg2",
            "Call Type2",
            "channel3",
            "slot3",
            "Aprs Tg3",
            "Call Type3",
            "channel4",
            "slot4",
            "Aprs Tg4",
            "Call Type4",
            "channel5",
            "slot5",
            "Aprs Tg5",
            "Call Type5",
            "channel6",
            "slot6",
            "Aprs Tg6",
            "Call Type6",
            "channel7",
            "slot7",
            "Aprs Tg7",
            "Call Type7",
            "channel8",
            "slot8",
            "Aprs Tg8",
            "Call Type8",
            "APRS TG",
            "Call Type",
            "Repeater Activation Delay[ms]",
            "APRS TX Tone",
            "TOCALL",
            "TOCALL SSID",
            "Your Call Sign",
            "Your SSID",
            "APRS Symbol Table",
            "APRS Map Icon",
            "Digipeater Path",
            "Enter Your Sending Text",
            "Transmission Frequency [MHz]",
            "Transmit Delay[ms]",
            "Send Sub Tone",
            "CTCSS",
            "DCS",
            "Prewave Time[ms]",
            "Transmit Power",
            "Receive Filter1",
            "Call Sign1",
            "SSID1",
            "Receive Filter2",
            "Call Sign2",
            "SSID2",
            "Receive Filter3",
            "Call Sign3",
            "SSID3",
            "Receive Filter4",
            "Call Sign4",
            "SSID4",
            "Receive Filter5",
            "Call Sign5",
            "SSID5",
            "Receive Filter6",
            "Call Sign6",
            "SSID6",
            "Receive Filter7",
            "Call Sign7",
            "SSID7",
            "Receive Filter8",
            "Call Sign8",
            "SSID8",
            "Receive Filter9",
            "Call Sign9",
            "SSID9",
            "Receive Filter10",
            "Call Sign10",
            "SSID10",
            "Receive Filter11",
            "Call Sign11",
            "SSID11",
            "Receive Filter12",
            "Call Sign12",
            "SSID12",
            "Receive Filter13",
            "Call Sign13",
            "SSID13",
            "Receive Filter14",
            "Call Sign14",
            "SSID14",
            "Receive Filter15",
            "Call Sign15",
            "SSID15",
            "Receive Filter16",
            "Call Sign16",
            "SSID16",
            "Receive Filter17",
            "Call Sign17",
            "SSID17",
            "Receive Filter18",
            "Call Sign18",
            "SSID18",
            "Receive Filter19",
            "Call Sign19",
            "SSID19",
            "Receive Filter20",
            "Call Sign20",
            "SSID20",
            "Receive Filter21",
            "Call Sign21",
            "SSID21",
            "Receive Filter22",
            "Call Sign22",
            "SSID22",
            "Receive Filter23",
            "Call Sign23",
            "SSID23",
            "Receive Filter24",
            "Call Sign24",
            "SSID24",
            "Receive Filter25",
            "Call Sign25",
            "SSID25",
            "Receive Filter26",
            "Call Sign26",
            "SSID26",
            "Receive Filter27",
            "Call Sign27",
            "SSID27",
            "Receive Filter28",
            "Call Sign28",
            "SSID28",
            "Receive Filter29",
            "Call Sign29",
            "SSID29",
            "Receive Filter30",
            "Call Sign30",
            "SSID30",
            "Receive Filter31",
            "Call Sign31",
            "SSID31",
            "Receive Filter32",
            "Call Sign32",
            "SSID32",
            "POSITION",
            "MIC-E",
            "OBJECT",
            "ITEM",
            "MESSAGE",
            "WX REPORT",
            "NMEA REPORT",
            "STATUS REPORT",
            "OTHER",
            "Transmission Frequency0",
            "Transmission Frequency1",
            "Transmission Frequency2",
            "Transmission Frequency3",
            "Transmission Frequency4",
            "Transmission Frequency5",
            "Transmission Frequency6",
            "Transmission Frequency7",
        ]

        writer.writerow(header)

        contents = [
            "0",  # Manual TX Interval[s]
            "10",  # APRS Auto TX Interval[s]
            "1",  # Support For Roaming
            "0",  # Fixed Location Beacon
            "23",  # LatiDegree
            "0",  # LatiMinInt
            "0",  # LatiMinMark
            "0",  # North or South
            "113",  # LongtiDegree
            "0",  # LongtiMinInt
            "0",  # LongtiMinMark
            "0",  # East or West Hemisphere
            "0",  # channel1
            "2",  # slot1
            "268967",  # Aprs Tg1
            "0",  # Call Type1
            "0",  # channel2
            "0",  # slot2
            "268967",  # Aprs Tg2
            "0",  # Call Type2
            "0",  # channel3
            "0",  # slot3
            "268967",  # Aprs Tg3
            "0",  # Call Type3
            "0",  # channel4
            "0",  # slot4
            "268967",  # Aprs Tg4
            "0",  # Call Type4
            "0",  # channel5
            "0",  # slot5
            "268967",  # Aprs Tg5
            "0",  # Call Type5
            "0",  # channel6
            "0",  # slot6
            "268967",  # Aprs Tg6
            "0",  # Call Type6
            "0",  # channel7
            "0",  # slot7
            "268967",  # Aprs Tg7
            "0",  # Call Type7
            "0",  # channel8
            "0",  # slot8
            "268967",  # Aprs Tg8
            "0",  # Call Type8
            "1",  # APRS TG
            "0",  # Call Type
            "0",  # Repeater Activation Delay[ms]
            "0",  # APRS TX Tone
            "APAT81",  # TOCALL
            "0",  # TOCALL SSID
            "CQ0ZZZ",  # Your Call Sign
            "7",  # Your SSID
            "/",  # APRS Symbol Table
            "[",  # APRS Map Icon
            "WIDE1-1,WIDE2-1",  # Digipeater Path
            "portaldoradioamador.pt. Plz QSO!",  # Enter Your Sending Text
            "145",  # Transmission Frequency [MHz]
            "0",  # Transmit Delay[ms]
            "0",  # Send Sub Tone
            "0",  # CTCSS
            "17",  # DCS
            "0",  # Prewave Time[ms]
            "2",  # Transmit Power
            "0",  # Receive Filter1
            "",  # Call Sign1
            "16",  # SSID1
            "0",  # Receive Filter2
            "",  # Call Sign2
            "16",  # SSID2
            "0",  # Receive Filter3
            "",  # Call Sign3
            "16",  # SSID3
            "0",  # Receive Filter4
            "",  # Call Sign4
            "16",  # SSID4
            "0",  # Receive Filter5
            "",  # Call Sign5
            "16",  # SSID5
            "0",  # Receive Filter6
            "",  # Call Sign6
            "16",  # SSID6
            "0",  # Receive Filter7
            "",  # Call Sign7
            "16",  # SSID7
            "0",  # Receive Filter8
            "",  # Call Sign8
            "16",  # SSID8
            "0",  # Receive Filter9
            "",  # Call Sign9
            "16",  # SSID9
            "0",  # Receive Filter10
            "",  # Call Sign10
            "16",  # SSID10
            "0",  # Receive Filter11
            "",  # Call Sign11
            "16",  # SSID11
            "0",  # Receive Filter12
            "",  # Call Sign12
            "16",  # SSID12
            "0",  # Receive Filter13
            "",  # Call Sign13
            "16",  # SSID13
            "0",  # Receive Filter14
            "",  # Call Sign14
            "16",  # SSID14
            "0",  # Receive Filter15
            "",  # Call Sign15
            "16",  # SSID15
            "0",  # Receive Filter16
            "",  # Call Sign16
            "16",  # SSID16
            "0",  # Receive Filter17
            "",  # Call Sign17
            "16",  # SSID17
            "0",  # Receive Filter18
            "",  # Call Sign18
            "16",  # SSID18
            "0",  # Receive Filter19
            "",  # Call Sign19
            "16",  # SSID19
            "0",  # Receive Filter20
            "",  # Call Sign20
            "16",  # SSID20
            "0",  # Receive Filter21
            "",  # Call Sign21
            "16",  # SSID21
            "0",  # Receive Filter22
            "",  # Call Sign22
            "16",  # SSID22
            "0",  # Receive Filter23
            "",  # Call Sign23
            "16",  # SSID23
            "0",  # Receive Filter24
            "",  # Call Sign24
            "16",  # SSID24
            "0",  # Receive Filter25
            "",  # Call Sign25
            "16",  # SSID25
            "0",  # Receive Filter26
            "",  # Call Sign26
            "16",  # SSID26
            "0",  # Receive Filter27
            "",  # Call Sign27
            "16",  # SSID27
            "0",  # Receive Filter28
            "",  # Call Sign28
            "16",  # SSID28
            "0",  # Receive Filter29
            "",  # Call Sign29
            "16",  # SSID29
            "0",  # Receive Filter30
            "",  # Call Sign30
            "16",  # SSID30
            "0",  # Receive Filter31
            "",  # Call Sign31
            "16",  # SSID31
            "0",  # Receive Filter32
            "",  # Call Sign32
            "16",  # SSID32
            "0",  # POSITION
            "0",  # MIC-E
            "0",  # OBJECT
            "0",  # ITEM
            "0",  # MESSAGE
            "0",  # WX REPORT
            "0",  # NMEA REPORT
            "0",  # STATUS REPORT
            "0",  # OTHER
            "144.8",  # Transmission Frequency0
            "144.8",  # Transmission Frequency1
            "144.8",  # Transmission Frequency2
            "144.8",  # Transmission Frequency3
            "144.8",  # Transmission Frequency4
            "144.8",  # Transmission Frequency5
            "144.8",  # Transmission Frequency6
            "144.8",  # Transmission Frequency7
        ]

        writer.writerow(contents)

        return sio


class DTMFEncodeCSVSerializer:
    @property
    def filename(self) -> str:
        return "DTMFEncode.CSV"

    def write(self) -> io.StringIO:
        sio = io.StringIO()
        writer = csv.writer(sio, dialect="d878uviiplus")

        header = ["DTMF ID", "DTMF Encode"]

        writer.writerow(header)

        return sio


class FiveToneEncodeCSVSerializer:
    @property
    def filename(self) -> str:
        return "5ToneEncode.CSV"

    def write(self) -> io.StringIO:
        sio = io.StringIO()
        writer = csv.writer(sio, dialect="d878uviiplus")

        header = [
            "NO.",
            "Encode ID",
            "Encode/Decode Standard",
            "Time Of Encode Tone[ms]",
            "Name",
        ]

        writer.writerow(header)

        return sio


class PrefabricatedSMSCSVSerializer:
    @property
    def filename(self) -> str:
        return "PrefabricatedSMS.CSV"

    def write(self) -> io.StringIO:
        sio = io.StringIO()
        writer = csv.writer(sio, dialect="d878uviiplus")

        header = ["No.", "Text"]

        writer.writerow(header)

        content = ["1", "SOTA_REF FREQ_MHz MODE CALLSIGN COMMENT"]

        writer.writerow(content)

        return sio


class TwoToneEncodeCSVSerializer:
    @property
    def filename(self) -> str:
        return "2ToneEncode.CSV"

    def write(self) -> io.StringIO:
        sio = io.StringIO()
        writer = csv.writer(sio, dialect="d878uviiplus")

        header = [
            "NO.",
            "1st Tone Frequency[Hz]",
            "2nd Tone Frequency[Hz]",
            "Name",
        ]

        writer.writerow(header)

        return sio


class RadioIDListCSVSerializer:
    def __init__(self):
        self._radio_ids: List[RadioId] = []

    @property
    def filename(self) -> str:
        return "RadioIDList.CSV"

    @property
    def radio_ids(self) -> List[RadioId]:
        return self._radio_ids

    def add_radio_id(self, radio_id: int, name: str) -> RadioId:
        self._radio_ids.append(RadioId(len(self.radio_ids) + 1, radio_id, name))
        return self.radio_ids[-1]

    def write(self) -> io.StringIO:
        sio = io.StringIO()
        writer = csv.writer(sio, dialect="d878uviiplus")

        header = ["No.", "Radio ID", "Name"]

        writer.writerow(header)

        for radio_id in self.radio_ids:
            writer.writerow(radio_id.serialize())

        return sio


class FMCSVSerializer:
    @property
    def filename(self) -> str:
        return "FM.CSV"

    def write(self) -> io.StringIO:
        sio = io.StringIO()
        writer = csv.writer(sio, dialect="d878uviiplus")

        header = ["No.", "Frequency[MHz]", "Scan"]

        writer.writerow(header)

        contents = [
            ["1", "88.700", "Add"],
            ["2", "87.800", "Add"],
            ["3", "87.700", "Add"],
            ["4", "100.100", "Add"],
            ["5", "101.300", "Add"],
            ["6", "91.800", "Add"],
        ]

        for content in contents:
            writer.writerow(content)

        return sio


class DigitalContactListCSVSerializer:
    @property
    def filename(self) -> str:
        return "DigitalContactList.CSV"

    def write(self) -> io.StringIO:
        sio = io.StringIO()
        writer = csv.writer(sio, dialect="d878uviiplus")

        header = [
            "No.",
            "Radio ID",
            "Callsign",
            "Name",
            "City",
            "State",
            "Country",
            "Remarks",
            "Call Type",
            "Call Alert",
        ]

        writer.writerow(header)

        data = requests.get(
            "https://radioid.net/api/dmr/user/?country=Portugal", timeout=5.0
        ).json()["results"]

        for idx, user in enumerate(data):
            writer.writerow(
                [
                    f"{idx+1}",
                    f"{user['id']}",
                    user["callsign"],
                    unidecode(user["fname"] if user["fname"] else ""),
                    unidecode(user["city"] if user["city"] else ""),
                    unidecode(user["state"] if user["state"] else ""),
                    unidecode(user["country"] if user["country"] else ""),
                    unidecode(user["remarks"] if user["remarks"] else ""),
                    CallType.PRIVATE,
                    "None",
                ]
            )

        return sio


class ZoneCSVSerializer:
    def __init__(self):
        self._zones: List[Zone] = []

    @property
    def filename(self) -> str:
        return "Zone.CSV"

    @property
    def zones(self) -> List[Zone]:
        return self._zones

    def add_zone(self, name: str) -> Zone:
        self._zones.append(Zone(len(self.zones) + 1, name))
        return self.zones[-1]

    def write(self) -> io.StringIO:
        sio = io.StringIO()
        writer = csv.writer(sio, dialect="d878uviiplus")

        header = [
            "No.",
            "Zone Name",
            "Zone Channel Member",
            "Zone Channel Member RX Frequency",
            "Zone Channel Member TX Frequency",
            "A Channel",
            "A Channel RX Frequency",
            "A Channel TX Frequency",
            "B Channel",
            "B Channel RX Frequency",
            "B Channel TX Frequency",
            "Zone Hide ",
        ]

        writer.writerow(header)

        for zone in self.zones:
            writer.writerow(zone.serialize())

        return sio


class TalkGroupsCSVSerializer:
    def __init__(self):
        self._tgs: List[TalkGroup] = []

    @property
    def filename(self) -> str:
        return "TalkGroups.CSV"

    @property
    def tgs(self) -> List[TalkGroup]:
        return self._tgs

    def add_tg(self, radio_id: int, name: str, call_type: CallType) -> TalkGroup:
        self._tgs.append(TalkGroup(len(self.tgs) + 1, radio_id, name, call_type))
        return self.tgs[-1]

    def write(self) -> io.StringIO:
        sio = io.StringIO()
        writer = csv.writer(sio, dialect="d878uviiplus")

        header = [
            "No.",
            "Radio ID",
            "Name",
            "Call Type",
            "Call Alert",
        ]

        writer.writerow(header)

        for tg in self.tgs:
            writer.writerow(tg.serialize())

        return sio


class ReceiveGroupCallListCSVSerializer:
    def __init__(self):
        self._rx_lists: List[RxList] = []

    @property
    def filename(self) -> str:
        return "ReceiveGroupCallList.CSV"

    @property
    def rx_lists(self) -> List[RxList]:
        return self._rx_lists

    def add_rx_list(self, name: str) -> RxList:
        self._rx_lists.append(RxList(len(self.rx_lists) + 1, name))
        return self.rx_lists[-1]

    def write(self) -> io.StringIO:
        sio = io.StringIO()
        writer = csv.writer(sio, dialect="d878uviiplus")

        header = [
            "No.",
            "Group Name",
            "Contact",
            "Contact TG/DMR ID",
        ]

        writer.writerow(header)

        for rx_list in self.rx_lists:
            writer.writerow(rx_list.serialize())

        return sio


class ScanListCSVSerializer:
    def __init__(self):
        self._scan_lists: List[ScanList] = []

    @property
    def filename(self) -> str:
        return "ScanList.CSV"

    @property
    def scan_lists(self) -> List[ScanList]:
        return self._scan_lists

    def add_scan_list(self, name: str) -> ScanList:
        self._scan_lists.append(ScanList(len(self.scan_lists) + 1, name))
        return self.scan_lists[-1]

    def write(self) -> io.StringIO:
        sio = io.StringIO()
        writer = csv.writer(sio, dialect="d878uviiplus")

        header = [
            "No.",
            "Scan List Name",
            "Scan Channel Member",
            "Scan Channel Member RX Frequency",
            "Scan Channel Member TX Frequency",
            "Scan Mode",
            "Priority Channel Select",
            "Priority Channel 1",
            "Priority Channel 1 RX Frequency",
            "Priority Channel 1 TX Frequency",
            "Priority Channel 2",
            "Priority Channel 2 RX Frequency",
            "Priority Channel 2 TX Frequency",
            "Revert Channel",
            "Look Back Time A[s]",
            "Look Back Time B[s]",
            "Dropout Delay Time[s]",
            "Dwell Time[s]",
        ]

        writer.writerow(header)

        for scan_list in self.scan_lists:
            writer.writerow(scan_list.serialize())

        return sio


class ChannelCSVSerializer:
    def __init__(self):
        self._channels: List[Channel] = []

    @property
    def filename(self) -> str:
        return "Channel.CSV"

    @property
    def channels(self) -> List[Channel]:
        return self._channels

    def add_channel(
        self,
        name: str,
        rx_mhz: float,
        tx_mhz: float,
        mode: ChannelMode,
        tg: TalkGroup,
        radio_id: RadioId,
        scan_list: ScanList,
        rx_list: RxList,
        bw: str = _NFM,
        ctcss: Optional[float] = None,
        color_code: int = 1,
        slot: int = 1,
    ) -> Channel:
        self._channels.append(
            Channel(
                len(self.channels) + 1,
                name,
                rx_mhz,
                tx_mhz,
                mode,
                tg,
                radio_id,
                scan_list,
                rx_list,
                bw,
                ctcss,
                color_code,
                slot,
            )
        )
        return self.channels[-1]

    def write(self) -> io.StringIO:
        sio = io.StringIO()
        writer = csv.writer(sio, dialect="d878uviiplus")

        header = [
            "No.",
            "Channel Name",
            "Receive Frequency",
            "Transmit Frequency",
            "Channel Type",
            "Transmit Power",
            "Band Width",
            "CTCSS/DCS Decode",
            "CTCSS/DCS Encode",
            "Contact",
            "Contact Call Type",
            "Contact TG/DMR ID",
            "Radio ID",
            "Busy Lock/TX Permit",
            "Squelch Mode",
            "Optional Signal",
            "DTMF ID",
            "2Tone ID",
            "5Tone ID",
            "PTT ID",
            "Color Code",
            "Slot",
            "Scan List",
            "Receive Group List",
            "PTT Prohibit",
            "Reverse",
            "Simplex TDMA",
            "Slot Suit",
            "AES Digital Encryption",
            "Digital Encryption",
            "Call Confirmation",
            "Talk Around(Simplex)",
            "Work Alone",
            "Custom CTCSS",
            "2TONE Decode",
            "Ranging",
            "Through Mode",
            "APRS RX",
            "Analog APRS PTT Mode",
            "Digital APRS PTT Mode",
            "APRS Report Type",
            "Digital APRS Report Channel",
            "Correct Frequency[Hz]",
            "SMS Confirmation",
            "Exclude channel from roaming",
            "DMR MODE",
            "DataACK Disable",
            "R5toneBot",
            "R5ToneEot",
            "Auto Scan",
            "Ana Aprs Mute",
            "Send Talker Alias",
            "AnaAprsTxPath",
            "ARC4",
            "ex_emg_kind",
        ]

        writer.writerow(header)

        for channel in self.channels:
            writer.writerow(channel.serialize())

        return sio


class RoamingChannelCSVSerializer:
    def __init__(self):
        self._roaming_channels: List[RoamingChannel] = []

    @property
    def filename(self) -> str:
        return "RoamingChannel.CSV"

    @property
    def roaming_channels(self) -> List[RoamingChannel]:
        return self._roaming_channels

    def add_roaming_channel(
        self, rx_mhz: float, tx_mhz: float, cc: int, slot: int, name: str
    ) -> RoamingChannel:
        self._roaming_channels.append(
            RoamingChannel(
                len(self.roaming_channels) + 1, rx_mhz, tx_mhz, cc, slot, name
            )
        )
        return self._roaming_channels[-1]

    def write(self) -> io.StringIO:
        sio = io.StringIO()
        writer = csv.writer(sio, dialect="d878uviiplus")

        header = [
            "No.",
            "Receive Frequency",
            "Transmit Frequency",
            "Color Code",
            "Slot",
            "Name",
        ]

        writer.writerow(header)

        for roaming_channel in self.roaming_channels:
            writer.writerow(roaming_channel.serialize())

        return sio


class RoamingZoneCSVSerializer:
    def __init__(self):
        self._roaming_zones: List[RoamingZone] = []

    @property
    def filename(self) -> str:
        return "RoamingZone.CSV"

    @property
    def roaming_zones(self) -> List[RoamingZone]:
        return self._roaming_zones

    def add_roaming_zone(self, name: str) -> RoamingZone:
        self._roaming_zones.append(RoamingZone(len(self.roaming_zones) + 1, name))
        return self._roaming_zones[-1]

    def write(self) -> io.StringIO:
        sio = io.StringIO()
        writer = csv.writer(sio, dialect="d878uviiplus")

        header = [
            "No.",
            "Name",
            "Roaming Channel Member",
        ]

        writer.writerow(header)

        for roaming_zone in self.roaming_zones:
            writer.writerow(roaming_zone.serialize())

        return sio


class RepeatersSerializer:
    def __init__(self, radio_id: int = 268000, name: str = "CT0ZZZ"):
        self._channel_csv = ChannelCSVSerializer()
        self._radio_id_list_csv = RadioIDListCSVSerializer()
        self._zone_csv = ZoneCSVSerializer()
        self._scan_list_csv = ScanListCSVSerializer()
        self._analog_address_book_csv = AnalogAddressBookCSVSerializer()
        self._talk_groups_csv = TalkGroupsCSVSerializer()
        self._prefabricated_sms_csv = PrefabricatedSMSCSVSerializer()
        self._fm_csv = FMCSVSerializer()
        self._receive_group_call_list_csv = ReceiveGroupCallListCSVSerializer()
        self._five_tone_encode_csv = FiveToneEncodeCSVSerializer()
        self._two_tone_encode_csv = TwoToneEncodeCSVSerializer()
        self._dtmf_encode_csv = DTMFEncodeCSVSerializer()
        self._digital_contact_list_csv = DigitalContactListCSVSerializer()
        self._auto_repeater_offset_frequencys_csv = (
            AutoRepeaterOffsetFrequencysCSVSerializer()
        )
        self._aprs_csv = APRSCSVSerializer()
        self._aes_encryption_code_csv = AESEncryptionCodeCSVSerializer()
        self._ar4_encryption_code_csv = AR4EncryptionCodeCSVSerializer()

        self._roaming_channel_csv = RoamingChannelCSVSerializer()
        self._roaming_zone_csv = RoamingZoneCSVSerializer()

        self._add_radio_ids([(radio_id, name)])
        self._add_tgs()
        self._add_rx_lists()
        self._add_fm_channels()
        self._add_dmr_channels()

    @property
    def _data(self) -> dict[str, dict[str, dict[str, BaseManager[FactRepeater]]]]:
        return {
            _CPT: {
                _B_2M: {
                    _FM: FactRepeater.objects.filter(
                        Q(info_location__region=_CPT)
                        & Q(info_rf__band=_B_2M)
                        & Q(modes__contains=[_FM])
                    ).order_by("-info_location__latitude"),
                    _DMR: FactRepeater.objects.filter(
                        Q(info_location__region=_CPT)
                        & Q(info_rf__band=_B_2M)
                        & Q(modes__contains=[_DMR])
                    ).order_by("-info_location__latitude"),
                },
                _B_70CM: {
                    _FM: FactRepeater.objects.filter(
                        Q(info_location__region=_CPT)
                        & Q(info_rf__band=_B_70CM)
                        & Q(modes__contains=[_FM])
                    ).order_by("-info_location__latitude"),
                    _DMR: FactRepeater.objects.filter(
                        Q(info_location__region=_CPT)
                        & Q(info_rf__band=_B_70CM)
                        & Q(modes__contains=[_DMR])
                    ).order_by("-info_location__latitude"),
                },
            },
            _MDA: {
                _B_2M: {
                    _FM: FactRepeater.objects.filter(
                        Q(info_location__region=_MDA)
                        & Q(info_rf__band=_B_2M)
                        & Q(modes__contains=[_FM])
                    ).order_by("info_location__longitude"),
                    _DMR: FactRepeater.objects.filter(
                        Q(info_location__region=_MDA)
                        & Q(info_rf__band=_B_2M)
                        & Q(modes__contains=[_DMR])
                    ).order_by("info_location__longitude"),
                },
                _B_70CM: {
                    _FM: FactRepeater.objects.filter(
                        Q(info_location__region=_MDA)
                        & Q(info_rf__band=_B_70CM)
                        & Q(modes__contains=[_FM])
                    ).order_by("info_location__longitude"),
                    _DMR: FactRepeater.objects.filter(
                        Q(info_location__region=_MDA)
                        & Q(info_rf__band=_B_70CM)
                        & Q(modes__contains=[_DMR])
                    ).order_by("info_location__longitude"),
                },
            },
            _AZR: {
                _B_2M: {
                    _FM: FactRepeater.objects.filter(
                        Q(info_location__region=_AZR)
                        & Q(info_rf__band=_B_2M)
                        & Q(modes__contains=[_FM])
                    ).order_by("info_location__longitude"),
                    _DMR: FactRepeater.objects.filter(
                        Q(info_location__region=_AZR)
                        & Q(info_rf__band=_B_2M)
                        & Q(modes__contains=[_DMR])
                    ).order_by("info_location__longitude"),
                },
                _B_70CM: {
                    _FM: FactRepeater.objects.filter(
                        Q(info_location__region=_AZR)
                        & Q(info_rf__band=_B_70CM)
                        & Q(modes__contains=[_FM])
                    ).order_by("info_location__longitude"),
                    _DMR: FactRepeater.objects.filter(
                        Q(info_location__region=_AZR)
                        & Q(info_rf__band=_B_70CM)
                        & Q(modes__contains=[_DMR])
                    ).order_by("info_location__longitude"),
                },
            },
        }

    def _add_radio_ids(self, ids: List[Tuple[int, str]]) -> None:
        for radio_id, name in ids:
            self._radio_id_list_csv.add_radio_id(radio_id, name)

    def _add_tgs(self):
        tgs = DimDmrTg.objects.all().order_by("id")
        for tg in tgs:
            call_type = (
                CallType.GROUP if tg.call_mode == _GROUP_CALL else CallType.PRIVATE
            )
            self._talk_groups_csv.add_tg(tg.id, tg.name, call_type)

    def _add_rx_lists(self):
        used_ts1_tgs = DimDmrTg.objects.filter(dimdmr_ts1_tgs__isnull=False).distinct()
        used_ts2_tgs = DimDmrTg.objects.filter(dimdmr_ts2_tgs__isnull=False).distinct()

        for tg_list, name in (
            (used_ts1_tgs, "TS1 TGs"),
            (used_ts2_tgs, "TS2 TGs"),
        ):
            rx_list = None
            for idx, tg_db in enumerate(tg_list):
                if idx % _MAXIMUM_TGS_PER_RX_LIST == 0:
                    rx_list = self._receive_group_call_list_csv.add_rx_list(
                        f"{name} {idx // _MAXIMUM_TGS_PER_RX_LIST + 1}"
                    )
                # Find the TG in the talk groups CSV
                tg = [
                    test_tg
                    for test_tg in self._talk_groups_csv.tgs
                    if test_tg.radio_id == tg_db.id
                ][0]
                rx_list.tgs.append(tg)

    def _add_fm_channels(self):
        for region in [_CPT, _MDA, _AZR]:
            for band in [_B_2M, _B_70CM]:
                zone = self._zone_csv.add_zone(f"{region} {band} FM")
                scan_list = None
                for idx, repeater in enumerate(self._data[region][band][_FM]):
                    if idx % _MAXIMUM_CHANNELS_PER_SCAN_ZONE == 0:
                        scan_list = self._scan_list_csv.add_scan_list(
                            f"{region} {band} FM {idx // _MAXIMUM_CHANNELS_PER_SCAN_ZONE + 1}"
                        )
                    channel = self._channel_csv.add_channel(
                        repeater.callsign,
                        repeater.info_rf.tx_mhz,  # Repeater Tx is radio Rx
                        repeater.info_rf.rx_mhz,  # Repeater Rx is radio Tx
                        ChannelMode.FM,
                        self._talk_groups_csv.tgs[0],  # Doesn't matter
                        self._radio_id_list_csv.radio_ids[0],  # Doesn't matter
                        scan_list,
                        self._receive_group_call_list_csv.rx_lists[0],  # Doesn't matter
                        repeater.info_fm.bandwidth,
                        repeater.info_fm.ctcss,
                    )
                    zone.channels.append(channel)
                    scan_list.channels.append(channel)

    def _add_dmr_channels(self):
        idx = 0
        # Don't add a roaming zone if it's going to be empty
        roaming_zone = None
        for region in [_CPT, _MDA, _AZR]:
            for band in [_B_2M, _B_70CM]:
                for repeater in self._data[region][band][_DMR]:
                    # Don't add a Zone if it's going to be empty
                    zone = None
                    # Determine the roaming zone
                    if idx % _MAXIMUM_CHANNELS_PER_ROAMING_ZONE == 0:
                        roaming_zone = self._roaming_zone_csv.add_roaming_zone(
                            f"DMR TS1 {idx // _MAXIMUM_CHANNELS_PER_ROAMING_ZONE + 1}"
                        )
                    # Create the roaming channel
                    roaming_channel = self._roaming_channel_csv.add_roaming_channel(
                        repeater.info_rf.tx_mhz,  # Repeater Tx is radio Rx
                        repeater.info_rf.rx_mhz,  # Repeater Rx is radio Tx
                        repeater.info_dmr.color_code,
                        1,
                        f"{repeater.callsign} TS1",
                    )
                    roaming_zone.channels.append(roaming_channel)
                    idx += 1
                    # Add channels for each TS1 and TS2 channels
                    for tg_set in (
                        repeater.info_dmr.ts1_tgs,
                        repeater.info_dmr.ts2_tgs,
                    ):
                        for tg_db in tg_set.all():
                            # Find the TG in the talk groups CSV
                            tg = [
                                test_tg
                                for test_tg in self._talk_groups_csv.tgs
                                if test_tg.radio_id == tg_db.id
                            ][0]
                            if zone is None:
                                # Add a zone for each repeater
                                zone = self._zone_csv.add_zone(f"{repeater.callsign}")
                            # Find the Rx list in the Rx list CSV
                            rx_list = [
                                test_rx_list
                                for test_rx_list in self._receive_group_call_list_csv.rx_lists
                                if tg in test_rx_list.tgs
                            ][0]
                            # Create the channel
                            channel = self._channel_csv.add_channel(
                                f"{repeater.callsign} {tg_db.id}",
                                repeater.info_rf.tx_mhz,  # Repeater Tx is radio Rx
                                repeater.info_rf.rx_mhz,  # Repeater Rx is radio Tx
                                ChannelMode.DMR,
                                tg,
                                self._radio_id_list_csv.radio_ids[0],
                                self._scan_list_csv.scan_lists[0],
                                rx_list,
                                slot=1,
                            )
                            zone.channels.append(channel)

    @property
    def codeplug(self) -> io.BytesIO:
        """
        Makes a .zip file with the files needed to import into the radio.
        """
        file_io = io.BytesIO()

        with zipfile.ZipFile(file_io, "w") as zip_file:
            for serializer in (
                self._channel_csv,
                self._radio_id_list_csv,
                self._zone_csv,
                self._scan_list_csv,
                self._analog_address_book_csv,
                self._talk_groups_csv,
                self._prefabricated_sms_csv,
                self._fm_csv,
                self._receive_group_call_list_csv,
                self._five_tone_encode_csv,
                self._two_tone_encode_csv,
                self._dtmf_encode_csv,
                self._digital_contact_list_csv,
                self._auto_repeater_offset_frequencys_csv,
                self._aprs_csv,
                self._aes_encryption_code_csv,
                self._ar4_encryption_code_csv,
                self._roaming_channel_csv,
                self._roaming_zone_csv,
            ):
                with zip_file.open(serializer.filename, "w") as csv_file:
                    csv_file.write(serializer.write().getvalue().encode("utf-8"))

        return file_io
