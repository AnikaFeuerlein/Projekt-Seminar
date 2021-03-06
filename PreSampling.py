import pandas as pd
from gurobipy import *

# ------------------------- Excel-Dateien ------------------------------------------------------------------------------
schedules = 'Schedule.xlsx'
aircrafts = 'Aircrafts.xlsx'
through_values = 'Through_Values.xlsx'
airports = 'Airports.xlsx'

# ---------------------- Aircraft-Datei --------------------------------------------------------------------------------

# TODO Aicrafttype[0][i]:
#       i=0: AIRCRAFT_ID
#       i=1: AIRLINE
#       i=2: PRODUCER
#       i=3: TYPE
#       i=4: COUNT
#       i=5: SEATS
#       i=6: RANGE
#       i=7: FEASIBLE_AIRPORTS
#       i=8: AIRCRAFT_USAGE_COSTS
#       i=9: AIRCRAFT_KM_COSTS
#       i=10: MAINTENANCE_COSTS
#       i=11: MAINTENANCE_DURATION
#       i=12: MAINTENANCE_TOTALTIME
#       i=13: MAINTENANCE_FLYINGTIME
#       i=14: MAINTENANCE_FLYINGTIME

df = pd.read_excel(aircrafts)
Aircrafttypes = {}

for i in range(0, 6):  # TODO müsste noch automatisch an Spaltenanzahl des Excel Sheets angepasst werden
    list = []
    list.append(df['AIRCRAFT_ID'][i])
    list.append(df['AIRLINE'][i])
    list.append(df['PRODUCER'][i])
    list.append(df['TYPE'][i])
    list.append(df['COUNT'][i])
    list.append(df['SEATS'][i])
    list.append(df['RANGE'][i])
    list.append(df['FEASIBLE_AIRPORTS'][i])
    list.append(df['AIRCRAFT_USAGE_COSTS'][i])
    list.append(df['AIRCRAFT_KM_COSTS'][i])
    list.append(df['MAINTENANCE_COSTS'][i])
    list.append(df['MAINTENANCE_DURATION'][i])
    list.append(df['MAINTENANCE_TOTALTIME'][i])
    list.append(df['MAINTENANCE_FLYINGTIME'][i])
    list.append(df['MAINTENANCE_STARTS'][i])
    Aircrafttypes[i] = list

# -------------------------------------------- Schedule-Datei --------------------------------------------------------

# TODO Flights[0][i]:
#       i=0: FLIGHT_NUMBER
#       i=1: FLIGHT_TYPE
#       i=2: EXECUTING_AIRLINE
#       i=3: ORIGIN_IATA
#       i=4: DESTINATION_IATA
#       i=5: DEPARTURE_TIME
#       i=6: ARRIVAL_TIME
#       i=7: DISTANCE
#       i=8: DURATION
#       i=9: DEMAND
#       i=10: CANCELLATION_COSTS
#       i=11: COSTS_PER_SPILLED_PASSENGER
#       i=12: PRE_FLIGHT_TA_TIME
#       i=13: POST_FLIGHT_TA_TIME


sf = pd.read_excel(schedules)
Flights = {}

for i in range(0, 100):  # TODO müsste noch automatisch an Spaltenanzahl des Excel Sheets angepasst werden
    list = []
    list.append(sf['FLIGHT_NUMBER'][i])
    list.append(sf['FLIGHT_TYPE'][i])
    list.append(sf['EXECUTING_AIRLINE'][i])
    list.append(sf['ORIGIN_IATA'][i])
    list.append(sf['DESTINATION_IATA'][i])
    list.append(sf['DEPARTURE_TIME'][i])
    list.append(sf['ARRIVAL_TIME'][i])
    list.append(sf['DISTANCE'][i])
    list.append(sf['DURATION'][i])
    list.append(sf['DEMAND'][i])
    list.append(sf['CANCELLATION_COSTS'][i])
    list.append(sf['COSTS_PER_SPILLED_PASSENGER'][i])
    list.append(sf['PRE_FLIGHT_TA_TIME'][i])
    list.append(sf['POST_FLIGHT_TA_TIME'][i])
    Flights[i] = list

# -------------------------------------- Airport-Datei ---------------------------------------------------------
# TODO Airport['DUS'][i] / Airport[FLights[j][4]][i]:
#       i=0: AIRPORT_CITY
#       i=1: AIRPORT_TYPE
#       i=2: AIRPORT_CATEGORY
#       i=3: AIRPORT_TA_MULTIPLIER
# der key ist hier: AIRPORT_IATA


af = pd.read_excel("Airports.xlsx")

Airports = {}
for i in range(0, 6):  # TODO müsste noch automatisch an Spaltenanzahl des Excel Sheets angepasst werden,hier bla
    list = []
    list.append(af['AIRPORT_CITY'][i])
    list.append(af['AIRPORT_TYPE'][i])
    list.append(af['AIRPORT_CATEGORY'][i])
    list.append(af['AIRPORT_TA_MULTIPLIER'][i])
    Airports[af['AIRPORT_IATA'][i]] = list


# ------------------- Pre-Sampling Methoden -------------------------------------------------------------------


# hier werden alle Kombis zugelassen, auch vorerst die, die örtlich, zeitlich gar nicht möglich sind

def Kombi1(Flights, Aircrafttypes):
    kombinationen = []
    for i in Flights:
        for j in Flights:
            for t in Aircrafttypes:
                kombinationen.append([i, j, 0, t])
                kombinationen.append([i, j, 1, t])
    return len(kombinationen), kombinationen


# print(Kombi1(Flights, Aircrafttypes))


# hier werden nur die Kombis zugelassen, bei denen der Ort passt, Zeit egal

def Kombi2(Flights, Aircrafttypes):
    kombinationen = []
    for i in Flights:
        for j in Flights:
            for t in Aircrafttypes:
                if Flights[i][4] == Flights[j][3]:
                    kombinationen.append([i, j, 0, t])
                    kombinationen.append([i, j, 1, t])
    return len(kombinationen), kombinationen


# print(Kombi2(Flights, Aircrafttypes))


# hier wird zusätzlich betrachtet ob der Abflugzeitpunkt des 2. Flugs nach der Ankunft des 1. FLugs ist

def Kombi3(Flights, Aircrafttypes):
    kombinationen = []
    for i in Flights:
        for j in Flights:
            for t in Aircrafttypes:
                if Flights[i][4] == Flights[j][3]:
                    if Flights[i][6] <= Flights[j][5]:
                        kombinationen.append([i, j, 0, t])
                        kombinationen.append([i, j, 1, t])
    return len(kombinationen), kombinationen


# print(Kombi3(Flights, Aircrafttypes))


# hier betrachtet man zusätzlich noch, dass das zeitlich auch mit den TA Zeiten klappt

def Kombi4(Flights, Aircrafttypes, Airports):
    kombinationen = []
    for i in Flights:
        for j in Flights:
            for t in Aircrafttypes:
                if Flights[i][4] == Flights[j][3]:
                    multiplier = Airports[Flights[i][4]][3]
                    if Flights[i][6] + (Flights[i][13] + Flights[j][12]) * multiplier <= Flights[j][5]:
                        kombinationen.append([i, j, 0, t])
                        kombinationen.append([i, j, 1, t])
    return len(kombinationen), kombinationen


# print(Kombi4(Flights, Aircrafttypes, Airports))


# hier wird zusätzlich geschaut ob zwischen den beiden Flügen eine Wartung ausgeführt werden kann r=1 oder nicht =0

def Kombi5(Flights, Aircrafttypes, Airports):
    kombinationen = []
    for i in Flights:
        for j in Flights:
            for t in Aircrafttypes:
                if Flights[i][4] == Flights[j][3]:
                    multiplier = Airports[Flights[i][4]][3]
                    if Flights[i][6] + (Flights[i][13] + Flights[j][12]) * multiplier <= Flights[j][5]:
                        if Flights[i][6] + (Flights[i][13] + Flights[j][12]) * multiplier + Aircrafttypes[t][11] <= \
                                Flights[j][5] \
                                and Airports[Flights[i][4]][1] == "HUB LH":
                            kombinationen.append([i, j, 0, t])
                            kombinationen.append([i, j, 1, t])
                        else:
                            kombinationen.append([i, j, 0, t])
    return len(kombinationen), kombinationen


# print(Kombi5(Flights, Aircrafttypes, Airports))


# hier wird zusätzlich überprüft ob die Range des Flugzeugs für die  Distanz des Fluges auch ausreicht

def Kombi6(Flights, Aircrafttypes, Airports):
    kombinationen = []
    for i in Flights:
        for j in Flights:
            for t in Aircrafttypes:
                if Aircrafttypes[t][6] >= Flights[i][7] and Aircrafttypes[t][6] >= Flights[j][7]:  # hier ergänzt
                    if Flights[i][4] == Flights[j][3]:
                        multiplier = Airports[Flights[i][4]][3]
                        if Flights[i][6] + (Flights[i][13] + Flights[j][12]) * multiplier <= Flights[j][5]:
                            if Flights[i][6] + (Flights[i][13] + Flights[j][12]) * multiplier + Aircrafttypes[t][11] <= \
                                    Flights[j][5] \
                                    and Airports[Flights[i][4]][1] == "HUB LH":
                                kombinationen.append([i, j, 0, t])
                                kombinationen.append([i, j, 1, t])
                            else:
                                kombinationen.append([i, j, 0, t])
    return kombinationen  # len(kombinationen)


print(Kombi6(Flights, Aircrafttypes, Airports))


# ------------------------------------------------------------------------------------------------------------------------------------------------

def Kilometerkosten():
    kombisVomPreSampling = Kombi6(Flights, Aircrafttypes, Airports)
    KilometerFlugKosten = [0 for i in range(len(kombisVomPreSampling))]
    for i in range(len(kombisVomPreSampling)):
        KilometerFlugKosten[i] = Flights[kombisVomPreSampling[i][1]][7] * Aircrafttypes[kombisVomPreSampling[i][3]][
            9]  # =dist_j* kmCost_t
    return KilometerFlugKosten


print(Kilometerkosten())


def VariablenListeFürGurobi():
    kombis = Kombi6(Flights, Aircrafttypes, Airports)
    Liste = []
    for i in range(len(kombis)):
        Liste.append((kombis[i][0], kombis[i][1], kombis[i][2], kombis[i][3]))
    return Liste


print(VariablenListeFürGurobi())

# You can also provide your own list of tuples as indices. For example, x = model.addVars([(3,'a'), (3,'b'), (7,'b'), (7,'c')])
# would be accessed in the same way as the previous example x[3,'a'], x[7,'c']

m = Model('test')

x = m.addVars(VariablenListeFürGurobi(),
              vtype=GRB.BINARY,
              obj=Kilometerkosten())

m.addConstrs(
    (x.sum(i, '*', '*', '*') <= 1 for i in Flights.keys()), 'Jeder Flug hat höchstens einen Nachfolger')

m.addConstrs(
    (x.sum('*', j, '*', '*') <= 1 for j in Flights.keys()), 'Jeder FLug hat höchstens einen Vorgänger')

for t in Aircrafttypes.keys():
    m.addConstrs(
        (x.sum(i, '*', '*', t) == x.sum('*', i, '*', t) for i in Flights.keys()), 'Flusserhaltung')


#Zielfunktion nimmt auch tatsächlich (sinvolle?) Werte an, falls diese Nebenbedingung einkommentiert wird muss der Constraint drüber auskommentiert werden
#m.addConstrs(
 #  (x.sum('*', '*', '*', t) == 3  for t in Aircrafttypes.keys()))

m.write('Test.lp')
m.optimize()

# print(x)
# print(x.keys()[0])    #so kann man für die Nebenbedingungen auf unsere Indizes zugreifen
# print(x.keys()[i][0])


# Example usage:

# x = m.addVars([(1,2), (1,3), (2,3)])
# expr = x.sum()       # LinExpr: x[1,2] + x[1,3] + x[2,3]
# expr = x.sum(1, '*') # LinExpr: x[1,2] + x[1,3]
# expr = x.sum('*', 3) # LinExpr: x[1,3] + x[2,3]
# expr = x.sum(1, 3)   # LinExpr: x[1,3]
