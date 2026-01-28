# This code is used to analyse and obtain the results for the fish stock section.
import os
from sdm_analysis import SDMFileManager, compute_presence_absence, create_presence_absence_table

# Results working directory. Parent directory where all results of SDMs are and where all output will be saved:
results_dir = r"C:\Users\beñat.egidazu\Desktop\NAS\PhD\Papers\Fisheries_2\Results"

# SDMs working directory. Working directory where all SDM files are:
sdms_dir = os.path.join(results_dir, "SDMs")

# Presence/Absence output directory (it is created if it does not exist):
presence_absence_dir = os.path.join(results_dir, "presence_absence")

# Initialize the SDM file manager
sdm_manager = SDMFileManager(sdms_dir)


# Run presence/absence maps:
compute_presence_absence(
    sdm_manager,
    presence_absence_dir,
    taxon_ids=['126421', '126426', '126822'],
    methods=['ensemble'],
    scenarios=['2000_2010', '2010_2020'],
    thresholds=['max_spec_sens']
)

# Create presence/absence table:
extent_table = create_presence_absence_table()

# Save table to csv:
extent_table.to_csv(os.path.join(results_dir, "extents_table.csv"))
