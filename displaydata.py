from prettytable import PrettyTable
import os.path
import csv
from decimal import *

cntxt = getcontext()

# CONFIG ---------------------------------------------------------------------

ORIGIN = 'Kador'
DESTINATION = 'Domain'
SHOW_COLUMNS = [
  'name',
  'unit buy price',
  'unit sell price',
  'unit tax-adjusted margin',
  'unit tax-adjusted percent margin',
]
SORT_BY = 'unit tax-adjusted margin'


# SCRIPT ---------------------------------------------------------------------

def run(origin, destination, show_columns=SHOW_COLUMNS, sort_by=SORT_BY):
  filename = '{}-to-{}.csv'.format(origin, destination)
  table = PrettyTable()

  with open(os.path.join('output', filename)) as csvfile:
    reader = csv.DictReader(csvfile)
    table.field_names = reader.fieldnames

    for row in reader:
      if float(row['unit tax-adjusted margin']) < 0:
        continue

      output_row = []
      for value in row.values():
        try:
          # Decimal acrobatics to get decimals to nicely display 2 points
          # after the decimal
          output_row.append(
            Decimal(
              Decimal(
                float(value)
              ).quantize(
                Decimal('.01')
              )
            )
          )
        except ValueError:
          output_row.append(value)

      table.add_row(output_row)

    table.align = 'r'
    return(
      table.get_string(
        fields=show_columns,
        sortby=sort_by,
        reversesort=True,
      )
    )


if __name__ == "__main__":
  print(run(ORIGIN, DESTINATION, SHOW_COLUMNS, SORT_BY))
