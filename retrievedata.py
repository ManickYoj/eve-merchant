import requests
import pprint
import csv
import os.path

import constants.region_ids
import constants.type_ids
import preferences as prefs

BASE_URL = 'https://market.fuzzwork.co.uk/aggregates/'
TAX_RATE = 0.02


class Type(object):
  IDS_BY_NAME = {
    entry[1].upper(): entry[0] for entry in constants.type_ids.TYPE_IDS
  }

  NAMES_BY_ID = {
    entry[0]: entry[1] for entry in constants.type_ids.TYPE_IDS
  }

  @classmethod
  def getID(cls, name):
    return cls.IDS_BY_NAME[name.upper()]

  @classmethod
  def getName(cls, id):
    return cls.NAMES_BY_ID[id]


class Region(object):
  IDS_BY_NAME = {
    entry[1].upper(): entry[0] for entry in constants.region_ids.REGION_IDS
  }

  NAMES_BY_ID = {
    entry[0]: entry[1] for entry in constants.region_ids.REGION_IDS
  }

  @classmethod
  def getID(cls, name):
      return cls.IDS_BY_NAME[name.upper()]

  @classmethod
  def getName(cls, id):
      return cls.NAMES_BY_ID[id]

  def __init__(self, id, item_ids):
    self.id = id
    self.name = Region.getName(id)
    self.items = self.getItemData(item_ids)

  def getItemData(self, item_ids):
    payload = {
      'region': self.id,
      'types': ','.join(item_ids),
    }

    request = requests.get(BASE_URL, params=payload)

    return [{
      'id': type_id,
      'name': Type.getName(type_id),
      'sell_price': data['buy']['max'],  # Sell at max price on buy market
      'buy_price': data['sell']['min']   # Buy at min price on sell market
    } for type_id, data in request.json().items()]

  def print(self):
    pp = pprint.PrettyPrinter()
    print("================")
    print(self.name)
    print("================")
    pp.pprint(self.items)
    print("")
    print("")


class Comparison(object):
  @staticmethod
  def compare(buy_region, sell_region):
    comparisons = []

    for i in range(len(buy_region.items)):
      item_bought = buy_region.items[i]
      item_sold = sell_region.items[i]

      if item_bought['buy_price'] == 0 or item_sold['sell_price'] == 0:
          continue

      assert item_bought['id'] == item_sold['id']
      assert item_bought['name'] == item_sold['name']

      unit_buy_price = float(item_bought['buy_price'])
      unit_sell_price = float(item_sold['sell_price'])
      unit_margin = unit_sell_price - unit_buy_price
      unit_taxes = (TAX_RATE) * unit_sell_price
      unit_tax_adjusted_margin = unit_margin - unit_taxes
      unit_tax_adjusted_percent_margin = (
        (unit_tax_adjusted_margin / unit_buy_price) * 100
      )

      comparisons.append(
        {
          'id': item_bought['id'],
          'name': item_bought['name'],
          'margin': round(unit_margin, 2),
          'buy price': round(unit_buy_price, 2),
          'sell price': round(unit_sell_price, 2),
          'TA margin': round(unit_tax_adjusted_margin, 2),
          'TA percent margin': round(unit_tax_adjusted_percent_margin, 1),
        }
      )

    return comparisons

  def __init__(self, buy_region, sell_region):
    self.buy_region = buy_region
    self.sell_region = sell_region
    self.comparison = Comparison.compare(buy_region, sell_region)
    self.name = buy_region.name + '-to-' + sell_region.name

  def print(self):
    pp = pprint.PrettyPrinter()
    print("================")
    print(self.name)
    print("================")
    pp.pprint(self.comparison)
    print("")
    print("")

  def csv(self):
    filename = os.path.join('output', self.name + '.csv')
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w+', newline='') as csvfile:
      writer = csv.DictWriter(
        csvfile,
        fieldnames=self.comparison[0].keys()
      )

      writer.writeheader()
      for row in self.comparison:
        writer.writerow(row)


def run(region_names=None, item_names=None, item_ids=None):
  # One or both of item_names or item_ids should be None
  assert (
    ((item_names is None) or (item_ids is None)) or
    ((item_names is None) and (item_ids is None))
  )

  # Case 1: item_ids passed. No operation necessary
  # Case 2: item_names passed. Need to convert to item_ids
  # Case 3: neither passed. Need to load default item_names and convert to ids
  if item_names is not None:
    item_ids = [Type.getID(item_name) for item_name in item_names]
  elif (item_names is None) and (item_ids is None):
    item_names = prefs.ITEMS
    item_ids = [Type.getID(item_name) for item_name in item_names]

  if region_names is None:
    region_names = prefs.REGIONS

  region_ids = [Region.getID(region_name) for region_name in region_names]
  regions = [Region(region_id, item_ids) for region_id in region_ids]

  comparisons = [
    Comparison(region1, region2)
    for region1 in regions
    for region2 in regions
  ]

  for comparison in comparisons:
      comparison.csv()


if __name__ == "__main__":
    run()
