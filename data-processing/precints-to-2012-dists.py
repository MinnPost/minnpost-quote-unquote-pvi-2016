import csv

#take an input pre-2012 precinct file and kick out 2012 district results

with open('../data/2010_general_results_final.csv','r') as f:
    elex_data = csv.DictReader(f)

    precinct_results = []

    for row in elex_data:

        if row['Precinct Name'] == "TOTALS":
            continue

        county = row['CountyID']
        precinct = row['Precinct Code']

        county_code = int(county) * 2 - 1

        precinct_code = "27{:0>3}{:0>4}".format(county_code, precinct)

        senate_dfl = int(row['MNSENDFL'])
        senate_gop = int(row['MNSENR'])
        senate_tot = int(row['MNSENTOT'])

        house_dfl = int(row['MNSENDFL'])
        house_gop = int(row['MNLEGR'])
        house_tot = int(row['MNLEGTOT'])

        precinct_results.append(
                                {
                                    "precinct": precinct_code,
                                    "senate_dfl": senate_dfl,
                                    "senate_gop": senate_gop,
                                    "senate_tot": senate_tot,

                                    "house_dfl": house_dfl,
                                    "house_gop": house_gop,
                                    "house_tot": house_tot,
                                }
                               )
