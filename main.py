import argparse
import report_maker as rm
import app
import sys
import mylogger as ml

parser = argparse.ArgumentParser(
    usage="COVID-19 data scraper",
    description="Extract CoronaVirus data from Worldometer website",
    epilog="Created by Lorenzo Conti",
    add_help=True
)
log = ml.Logger()
reportmaker = rm.ReportMaker()
parser.add_argument('country',nargs="?", type=str,help='Country of interest')
args = vars(parser.parse_args())
country = str(args["country"])
print(f"Accepted country argument: {country}")

myapp = app.App("Chrome")
data = myapp.get_country(country)
TOTAL = myapp.get_total()

cols = [
    "Country",
    "Total cases",
    "New Cases",
    "Total Deaths",
    "New deaths",
    "Total Recovered",
    "Active Cases",
    "Serious",
    "Total Cases/1M pop",
    "Deaths/1M pop",
    "Total tests",
    "Tests/1M pop",
    "Population"
]

def calculate_percentage(value,total):
    return value/total*100

def get_value(attr,list):
    for k in list:
        if k[0] == attr:
            return k[1]
    return None

totalcases = get_value("Total Cases",data)
newcases = get_value("New Cases",data)
totaldeaths = get_value("Total Deaths",data)

report = f"""
# {country}

- Total Cases: {totalcases}
- New Cases: {newcases}
- Total Deaths: {totaldeaths}
"""

reportmaker.append(report)
reportmaker.compile()


myapp.quit()