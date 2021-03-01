# (^._.^)ﾉ Author: Vu Dinh Anh
# fil = file iter longissimum

import sys
import os
import apache_beam as beam

from apache_beam.io import ReadFromText
from pprint import pprint

if __name__ == '__main__':
    file = sys.argv[1]
    if not os.path.isfile(file):
        print('File not found')
    else:
        with beam.Pipeline() as pipeline:
            # Reading
            lines = pipeline | ReadFromText(file)

            # Mapping
            measured_paths = (
                lines
                | "Measure" >> beam.Map(
                    lambda line: (line, len(line.split('/')))
                    )
            )

            # Reducing
            max_value = (
                measured_paths
                | "Max" >> beam.CombineGlobally(
                    lambda paths: max(paths, key=lambda p: p[1])
                    )
                | beam.Map(pprint)
            )