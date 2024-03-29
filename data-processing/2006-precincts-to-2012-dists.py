import csv

#2006 precinct results cast on to 2012 districts (via precinct centroids)

with open('../data/2006_general_results.csv','r') as f:
    elex_data = csv.DictReader(f)

    precinct_results = {}

    for row in elex_data:

        if row['Precinct Name'] == "TOTALS":
            continue

        county = row['County_ID']
        precinct = row['PRCT']

        county_code = int(county) * 2 - 1

        precinct_code = "27{:0>3}{:0>4}".format(county_code, precinct)

        senate_dfl = int(row['StateSenDFL'])
        senate_gop = int(row['StateSenR'])
        senate_tot = int(row['StateSenTOT'])

        house_dfl = int(row['StateHouseDFL'])
        house_gop = int(row['StateHouseR'])
        house_tot = int(row['StateHouseTOT'])

        precinct_results[precinct_code] = {
                                    "precinct": precinct_code,
                                    "senate_dfl": senate_dfl,
                                    "senate_gop": senate_gop,
                                    "senate_tot": senate_tot,

                                    "house_dfl": house_dfl,
                                    "house_gop": house_gop,
                                    "house_tot": house_tot,
                                }
results = {}

with open('2006-precincts-in-2012-districts.csv') as f:
    precincts = csv.reader(f)

    next(precincts) #skip header

    for row in precincts:
        precinct = row[0]

        try:
            test = precinct_results[precinct] #this is dangerous but there are some precincts
        except:                               #that don't have vote data
            print("Found no data for " + precinct)
            continue

        house_district = row[2]
        senate_district = house_district[0:2]

        #add to house
        if house_district in results:
            results[house_district]["gop_total"] += precinct_results[precinct]["house_gop"]
            results[house_district]["dfl_total"] += precinct_results[precinct]["house_dfl"]
            results[house_district]["vot_total"] += precinct_results[precinct]["house_tot"]
            results[house_district]["tot_pcts"] += 1
        else:
            results[house_district] = {
                                        "gop_total": precinct_results[precinct]["house_gop"],
                                        "dfl_total": precinct_results[precinct]["house_dfl"],
                                        "vot_total": precinct_results[precinct]["house_tot"],
                                        "tot_pcts": 1
                                      }

        #add to senate
        if senate_district in results:
            results[senate_district]["gop_total"] += precinct_results[precinct]["senate_gop"]
            results[senate_district]["dfl_total"] += precinct_results[precinct]["senate_dfl"]
            results[senate_district]["vot_total"] += precinct_results[precinct]["senate_tot"]
            results[senate_district]["tot_pcts"] += 1
        else:
            results[senate_district] = {
                                        "gop_total": precinct_results[precinct]["senate_gop"],
                                        "dfl_total": precinct_results[precinct]["senate_dfl"],
                                        "vot_total": precinct_results[precinct]["senate_tot"],
                                        "tot_pcts": 1
                                      }

#save results to file
with open('2006_results_in_2012_districts.csv','w') as of:
    out = csv.writer(of)

    out.writerow(["district", "total_precincts", "gop_votes", "dfl_votes","total_votes", "gop%", "dfl%", "margin"])

    for district in results:

        total_precincts = results[district]["tot_pcts"]
        gop_total = results[district]["gop_total"]
        dfl_total = results[district]["dfl_total"]
        vot_total = results[district]["vot_total"]

        gop_percent = float(gop_total) / float(vot_total)
        dfl_percent = float(dfl_total) / float(vot_total)

        margin = dfl_percent - gop_percent

        out.writerow([
                        district,
                        total_precincts,
                        gop_total,
                        dfl_total,
                        vot_total,
                        gop_percent,
                        dfl_percent,
                        margin
                     ])
