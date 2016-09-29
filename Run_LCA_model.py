from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

from Parameters import *
from logistics_functions import *
from LCA_urine_model import LCA_urine_model, LCA_collection, material_transportation
from logistics_model import logistics_model

def Run_LCA_model(path, n_regen, n_collection, schedule, logistics):

	Logistics = logistics_model(path, n_regen, n_collection, logistics)
	distance_regeneration, distance_collection = Logistics.logistics_distances()

	Total_Energy = pd.DataFrame()
	Total_GHG = pd.DataFrame()
	Total_COST = pd.DataFrame()

	for index, row in distance_regeneration.iterrows():
	    number_of_people_per_facility= row['num_people']
	    distance_regen = row['total_dist_m']
	    truck_num = int(row['trucks_num'])
	    ENERGY, GHG, COST = LCA_urine_model(number_of_people_per_facility, distance_regen, truck_num)
	    Total_Energy = Total_Energy.append(ENERGY)
	    Total_GHG = Total_GHG.append(GHG)
	    Total_COST = Total_COST.append(COST)

	Total_Energy_regen = Total_Energy.sum()
	Total_Energy_regen=pd.DataFrame(Total_Energy_regen).T
	Total_GHG_regen = Total_GHG.sum()
	Total_GHG_regen=pd.DataFrame(Total_GHG_regen).T
	Total_COST_regen = Total_COST.sum()
	Total_COST_regen=pd.DataFrame(Total_COST_regen).T
	Total_people = distance_regeneration['num_people'].sum()

	Total_Energy_collect, Total_GHG_collect, Total_COST_collect = LCA_collection(Total_people, distance_collection)
	Resin_energy_transport, Resin_GHG_transport, Resin_COST_transport = material_transportation(resin_transport, resin_lifetime)
	Cartridge_energy_transport, Cartridge_GHG_transport, Cartridge_COST_transport = material_transportation(km, PVC_lifetime)
	Tank_energy_transport, Tank_GHG_transport, Tank_COST_transport = material_transportation(km, plastic_lifetime)
	Pump_energy_transport, Pump_GHG_transport, Pump_COST_transport = material_transportation(km, pump_lifetime)
	Acid_energy_transport, Acid_GHG_transport, Acid_COST_transport = material_transportation(acid_transport, 1)
	
	Total_Energy_total = Total_Energy_regen
	Total_GHG_total = Total_GHG_regen
	Total_COST_total = Total_COST_regen

	Total_Energy_total['Logistics_collect'] = Total_Energy_collect
	Total_Energy_total['Resin transport'] = Resin_energy_transport
	Total_Energy_total['Catridge transport'] = Cartridge_energy_transport
	Total_Energy_total['Tank transport'] = Tank_energy_transport
	Total_Energy_total['Pump transport'] = Pump_energy_transport
	Total_Energy_total['Acid transport'] = Acid_energy_transport

	Total_GHG_total['Logistics_collect'] = Total_GHG_collect
	Total_GHG_total['Resin transport'] = Resin_GHG_transport
	Total_GHG_total['Catridge transport'] = Cartridge_GHG_transport
	Total_GHG_total['Tank transport'] = Tank_GHG_transport
	Total_GHG_total['Pump transport'] = Pump_GHG_transport
	Total_GHG_total['Acid transport'] = Acid_GHG_transport

	Total_COST_total['Logistics_collect'] = Total_COST_collect
	Total_COST_total['Resin transport'] = Resin_COST_transport
	Total_COST_total['Catridge transport'] = Cartridge_COST_transport
	Total_COST_total['Tank transport'] = Tank_COST_transport
	Total_COST_total['Pump transport'] = Pump_COST_transport
	Total_COST_total['Acid transport'] = Acid_COST_transport

	Total_Energy_m3=Total_Energy_total/(urine_production*365*Total_people/1000)
	Total_Energy_m3['n_facilities'] = n_regen
	Total_GHG_m3 = Total_GHG_total/(urine_production*365*Total_people/1000)
	Total_GHG_m3['n_facilities'] = n_regen
	Total_COST_m3 = Total_COST_total/(urine_production*365*Total_people/1000)
	Total_COST_m3['n_facilities'] = n_regen

	return Total_Energy_m3, Total_GHG_m3, Total_COST_m3
