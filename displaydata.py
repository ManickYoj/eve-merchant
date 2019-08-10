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
  'buy price',
  'sell price',
  'TA margin',
  'TA percent margin',
]
SORT_BY = 'TA percent margin'


# SCRIPT ---------------------------------------------------------------------

def run(origin, destination, show_columns=SHOW_COLUMNS, sort_by=SORT_BY):
  filename = '{}-to-{}.csv'.format(origin, destination)
  relative_path = os.path.join('output', filename)
  table = PrettyTable()

  if not os.path.isfile(relative_path):
    raise FileNotFoundError("Data for these regions has not been retreived.")

  with open(relative_path) as csvfile:
    reader = csv.DictReader(csvfile)
    table.field_names = reader.fieldnames

    for row in reader:
      if float(row['TA margin']) < 0:
        continue

      output_row = []
      for value in row.values():
        try:
          formatted_val = '{:,.2f}'.format(float(value))
          output_row.append(formatted_val)
        except ValueError as e:
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
