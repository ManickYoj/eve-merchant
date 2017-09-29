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
    IDS_BY_NAME = {entry[1]: entry[0] for entry in constants.type_ids.TYPE_IDS}
    NAMES_BY_ID = {entry[0]: entry[1] for entry in constants.type_ids.TYPE_IDS}

    @classmethod
    def getID(cls, name):
        return cls.IDS_BY_NAME[name]

    @classmethod
    def getName(cls, id):
        return cls.NAMES_BY_ID[id]


class Region(object):
    IDS_BY_NAME = {entry[1]: entry[0] for entry in constants.region_ids.REGION_IDS}
    NAMES_BY_ID = {entry[0]: entry[1] for entry in constants.region_ids.REGION_IDS}

    @classmethod
    def getID(cls, name):
        return cls.IDS_BY_NAME[name]

    @classmethod
    def getName(cls, id):
        return cls.NAMES_BY_ID[id]

    def __init__(self, id, region_data):
        self.id = id
        self.name = Region.getName(id)
        self.items = [{
            'id': type_id,
            'name': Type.getName(type_id),
            'sell_price': data['buy']['max'],   # Sell at the max price on buy market
            'buy_price': data['sell']['min']    # Buy at the min price on sell market
        } for type_id, data in region_data.items()]

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
            unit_tax_adjusted_percent_margin = ((unit_tax_adjusted_margin / unit_buy_price) * 100)

            comparisons.append(
                {
                    'id' : item_bought['id'],
                    'name': item_bought['name'],
                    'unit margin': round(unit_margin, 2),
                    'unit tax-adjusted margin': round(unit_tax_adjusted_margin, 2),
                    'unit buy price': round(unit_buy_price, 2),
                    'unit sell price': round(unit_sell_price, 2),
                    'unit tax-adjusted percent margin': round(unit_tax_adjusted_percent_margin, 1),
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
        with open(os.path.join('output', self.name + '.csv'), 'w', newline='') as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=self.comparison[0].keys()
            )

            writer.writeheader()
            for row in self.comparison:
                writer.writerow(row)


def run():
    item_list = [Type.getID(item) for item in prefs.ITEMS]
    regions = []
    comparisons = []

    for region in prefs.REGIONS:
        region_id = Region.getID(region)

        payload = {
            'region': region_id,
            'types': ','.join(item_list),
        }

        request = requests.get(BASE_URL, params=payload)
        regions.append(Region(region_id, request.json()))

    for region1 in regions:
        for region2 in regions:
            comparisons.append(Comparison(region1, region2))

    for comparison in comparisons:
        comparison.csv()


if __name__ == "__main__":
    run()
