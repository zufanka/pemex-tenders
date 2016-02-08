import csv, numpy

def median(lst):

    return numpy.median(numpy.array(lst))

inputfile = open("clean_output.csv")
reader = csv.reader(inputfile)

reader.next()
data = [row for row in reader]


# median & average costs of contracts per year
with open("stats_pesos_per_year.csv", "w") as spy:
    w = csv.writer(spy)
    header = ["year", "contracts", "median", "average"]
    w.writerow(header)

    for year in range(2003,2015):

        pesos = [float(r[6]) for r in data if r[1] == str(year)]
        w.writerow([year, len(pesos), median(pesos), numpy.average(pesos)])

# median & average costs of contracts per procedure
with open("stats_pesos_per_proc.csv", "w") as spy:
    w = csv.writer(spy)
    header = ["proc", "contracts", "median", "average"]
    w.writerow(header)

    procs = ["ADJUDICACION DIRECTA", "CONTRATOS ENTRE ENTIDADES", "INVITACION A TRES PERSONAS", "LICITACION PUBLICA INTERNACIONAL", "LICITACION PUBLICA NACIONAL", "OTROS"]

    for proc in procs:

        pesos = [float(r[6]) for r in data if r[4] == proc]
        w.writerow([proc, len(pesos), median(pesos), numpy.average(pesos)])


# median & average costs of contracts per procedure per year
with open("stats_pesos_per_proc_per_year.csv", "w") as spy:
    w = csv.writer(spy)
    header = ["year", "proc", "contracts", "median", "average"]
    w.writerow(header)

    procs = ["ADJUDICACION DIRECTA", "CONTRATOS ENTRE ENTIDADES", "INVITACION A TRES PERSONAS", "LICITACION PUBLICA INTERNACIONAL", "LICITACION PUBLICA NACIONAL", "OTROS"]

    for proc in procs:
        for year in range(2003,2015):

            pesos = [float(r[6]) for r in data if r[4] == proc and r[1] == str(year)]
            w.writerow([year, proc, len(pesos), median(pesos), numpy.average(pesos)])

# duration & costs
with open("stats_pesos_per_duration.csv", "w") as spy:
    w = csv.writer(spy)
    header = ["duration", "contracts", "median", "average"]
    w.writerow(header)

    for duration in range(0,35):

        pesos = [float(r[6]) for r in data if r[10] == str(duration)]
        w.writerow([duration, len(pesos), median(pesos), numpy.average(pesos)])
