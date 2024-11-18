import logdata as logdata
for resolution in range(10_000, 1_000, -500):
    for subsets in range(250, resolution+1, 250):
        logdata.main(subsets, resolution)