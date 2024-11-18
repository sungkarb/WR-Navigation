import logdata as logdata
for resolution in range(6_000, 4_500-1, -500):
    for subsets in range(500, resolution+1, 250):
        logdata.main(subsets, resolution)