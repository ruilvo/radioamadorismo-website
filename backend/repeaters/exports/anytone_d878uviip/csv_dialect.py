"""
CSV dialect for the Anytone D878UVII+
"""

import csv


class D878UVIIPlusDialect(csv.excel):
    quotechar = '"'
    quoting = csv.QUOTE_ALL


csv.register_dialect("d878uviiplus", D878UVIIPlusDialect)
