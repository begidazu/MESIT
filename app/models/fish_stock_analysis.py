# This code is used to analyse and obtain the results for the fish stock section.

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

resp_curve = r"C:\Users\beñat.egidazu\Desktop\NAS\PhD\Papers\Fisheries_2\Results\SDMs\taxonid=126426\model=mpaeu\metrics\taxonid=126426_model=mpaeu_method=ensemble_what=respcurves.parquet"
var_import = r"C:\Users\beñat.egidazu\Desktop\NAS\PhD\Papers\Fisheries_2\Results\SDMs\taxonid=126822\model=mpaeu\metrics\taxonid=126822_model=mpaeu_method=ensemble_what=varimportance.parquet"
thresholds = r"C:\Users\beñat.egidazu\Desktop\NAS\PhD\Papers\Fisheries_2\Results\SDMs\taxonid=126421\model=mpaeu\metrics\taxonid=126421_model=mpaeu_what=thresholds.parquet"

resp_curve_pq = pd.read_parquet(resp_curve)
var_import_pq = pd.read_parquet(var_import)
thresholds_pq = pd.read_parquet(thresholds)

# Lista de variables
variables = ['thetao_max', 'thetao_range', 'o2_min', 'so_min', 'sws_max','bathymetry_mean', 'rugosity']

# Bucle para generar plots para cada variable
# for variable in variables:
#     data_filtered = resp_curve_pq[resp_curve_pq['variable'] == variable]
    
#     if not data_filtered.empty:
#         plot = data_filtered.plot(x='base', y='response', kind='line', 
#                                    title=f'Response Curve for {variable}', 
#                                    xlabel='Variable Value', 
#                                    ylabel='Response',
#                                    figsize=(10, 6))
#         plt.tight_layout()
#         plt.show()
#     else:
#         print(f"No data found for variable: {variable}")

# Mostrar importancia de variables:
print(var_import_pq)

# Mostrar thresholds:
print(thresholds_pq)
