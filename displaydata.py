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

    # Use show_columns for order and filtering
    table.field_names = show_columns

    for row in reader:
      if float(row['TA margin']) < 0:
        continue

      output_row = []

      # Use show_columns for order and filtering
      ordered_row = [row[col_name] for col_name in show_columns]

      for value in ordered_row:
        try:
          formatted_val = '{:,.2f}'.format(float(value))
          output_row.append(formatted_val)
        except ValueError as e:
          output_row.append(value)

      table.add_row(output_row)

    table.align = 'r'

    # Not sure why, but there's an off by one error on this index
    sort_column_index = show_columns.index(sort_by) + 1

    return(
      table.get_string(
        fields=show_columns,
        sortby=sort_by,
        sort_key=lambda row: float(row[sort_column_index].replace(',','')),
        reversesort=True,
      )
    )


if __name__ == "__main__":
  print(run(ORIGIN, DESTINATION, SHOW_COLUMNS, SORT_BY))
