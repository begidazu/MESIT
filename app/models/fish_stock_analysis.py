# This code is used to analyse and obtain the results for the fish stock section.
import os
from sdm_parser import SDMFileManager

# ----------------------------- EXAMPLE USAGE --------------------------------------:
sdm_root = r"C:\Users\beñat.egidazu\Desktop\NAS\PhD\Papers\Fisheries_2\Results\SDMs"

# All methods properly documented with examples, parameter descriptions, and return types
manager = SDMFileManager(sdm_root)

# Select a taxon ID to use for all examples (change this to test different species)
taxon_id = '126426'

# Example 1: Get a specific prediction file
file_path = manager.get_file(
    taxon_id=taxon_id,
    folder_type='predictions',
    method='ensemble',
    scen='2000_2010'    # To check all available scenarios, use example 3.
)
print(f"File path: {file_path}; Exists: {os.path.exists(file_path) if file_path else False}")

# Example 2: Get all metrics for a method
files = manager.get_files(taxon_id=taxon_id, folder_type='metrics', method='ensemble')
print(f"Metric files found: {files}")

# Example 3: List available scenarios
params = manager.list_parameters(taxon_id, 'predictions')
print(f"Available scenarios: {params.get('scen', [])}")

# Example 4: List available methods
methods = manager.list_parameters(taxon_id, 'predictions')
print(f"Available methods: {methods.get('method', [])}")


