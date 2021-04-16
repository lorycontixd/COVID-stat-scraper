import argparse
from modules import report_maker as rm
from modules import app
import sys
from modules import mylogger as ml

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
    "country",
    "total cases",
    "new cases",
    "total deaths",
    "new deaths",
    "total recovered",
    "active cases",
    "serious",
    "total Cases/1m pop",
    "deaths/1m pop",
    "total tests",
    "tests/1m pop",
    "population"
]

def calculate_percentage(value,total):
    return float("{:.2f}".format(float(value)/float(total)*100))

def get_value(attr,list):
    for k in list:
        if k[0] == attr:
            return k[1]
    return None

totalcases = get_value("total cases",data)
newcases = get_value("new cases",data)
totaldeaths = get_value("total deaths",data)
newdeaths = get_value("new deaths",data)
totalrecovered = get_value("total recovered",data)

def graph_value():
    pass

report = """
# {country}

- Total tases: {cases} ----> {world_cases}%% of world's
- New cases: {newcases} ----> {world_newcases}%% of world's
- Total deaths: {totaldeaths} ----> {world_totaldeaths}%% of world's
- New deaths: {newdeaths} ----> {world_newdeaths}%% of world's
- Total recovered: {recovered} ----> {world_recovered}%% of world's
""".format(
    country=country.capitalize(),
    cases=totalcases,
    world_cases=calculate_percentage(totalcases,get_value("total cases",TOTAL)),
    newcases=newcases,
    world_newcases=calculate_percentage(newcases,get_value("new cases",TOTAL)),
    totaldeaths=totaldeaths,
    world_totaldeaths=calculate_percentage(totaldeaths,get_value("total deaths",TOTAL)),
    newdeaths=newdeaths,
    world_newdeaths=calculate_percentage(newdeaths,get_value("new deaths",TOTAL)),
    recovered=totalcases,
    world_recovered=calculate_percentage(totalrecovered,get_value("total recovered",TOTAL))
)

print("main: making report... ")
reportmaker.append_text(report)
reportmaker.compile()


myapp.quit()
