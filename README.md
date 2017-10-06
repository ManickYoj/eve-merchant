# eve-merchant
A tool for finding strong inter-regional trades in EVE Online

### Installation/Setup

To run this script, you must have [python 3.X.X](https://www.python.org/downloads/) installed.

With python installed, clone this repo into the directory of your choosing with:

`git clone git@github.com:ManickYoj/eve-merchant.git`

### Usage

```
# Enter this directory
cd eve-merchant

# Find the best trades going from origin region to destination region
# Note: TA stands for 'tax-adjusted'. Assumes no accounting skill upgrades.
python cli.py <origin> <destination> [--refresh] [--sort-by='TA Margin']

# Example
python cli.py tash-murkon domain
```

By default, the script will use cached data when run again on a set of regions it has loaded before. To get the newest data, use the `--refresh` flag. Note that the data source - the [fuzzworks market](https://market.fuzzwork.co.uk/) aggregate API - only refreshes on a 30 minute cycle, so the refresh flag will only change the data every 30 minutes at most.


#### Buy/Sell Fidelity
Note that the data source does not distinguish between a buy or sell order of 1 item or 1000. For that reason, if you're relying on this tool to pick the best trades, percent margin may be a misleading measure because you may not be able to buy or sell enough of the desired trade good to make it worth your time.

#### Item List
The items that this script considers are currently set in the preferences file. In the future, all items will be considered, but for now that causes bugs.