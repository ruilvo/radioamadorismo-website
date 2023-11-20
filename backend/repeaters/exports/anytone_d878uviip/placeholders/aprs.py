"""
Serializer for Anytone D878UVII+ APRS.py
"""

import io
import csv


def aprs_csv() -> io.StringIO:
    """
    Generates an APRS.csv
    """

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

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")
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
