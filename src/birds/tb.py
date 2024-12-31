

from birds.tb_utils import get_tb_goldens 
import pandas as pd

# logic is:

# One time per location:
# 	get_hotspots (or get from cache)
# 	get_taxonomy (or get from cache)

# 	narrow down hotspots to a reasonable amount based on all time amounts and distance - perhaps latest 250 (or get from cache)
# 	find driving distance for each of them (cache this)


# For each run
# 	retrieve last two weeks for each of these 250 spots - add or update column
# 	filter out ducks and pigeons - add or update column
	
# Display result


def get_goldens(name, lat, long, max_num):
    df = get_tb_goldens(name, lat, long, max_num)
    return df

#get_goldens("Hoboken",40.745255,-74.034775,5)





