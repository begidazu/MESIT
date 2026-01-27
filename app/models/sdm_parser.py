# This code is used to analyse and obtain the results for the fish stock section.
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Any


# Set working directory, folder names and paths, etc.
results_wd = r"C:\Users\beñat.egidazu\Desktop\NAS\PhD\Papers\Fisheries_2\Results"

sdms_dict = {
    "sdms": "SDMs",
    "species_folder": os.listdir(os.path.join(results_wd, "SDMs")),
    "model_folder": "model=mpaeu",
    "figures_folder": "figures",
    "metrics_folder": "metrics",
    "models_folder": "models",
    "predictions_folder": "predictions",
}

# Set up class to manage SDM files
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Any

class SDMFileManager:
    """
    Advanced SDM (Species Distribution Models) file manager that parses filenames with key=value format.
    
    This class provides a convenient interface to access SDM result files organized in a hierarchical
    folder structure based on the MPAEU results structure. It automatically indexes all files and allows 
    retrieval based on various parameters such as taxon ID, model type, scenario, metrics, etc.
    
    Folder Structure:
        results_wd/
        └── SDMs/
            ├── taxonid=126421/
            │   └── model=mpaeu/
            │       ├── figures/
            │       ├── metrics/
            │       ├── models/
            │       └── predictions/
            ├── taxonid=126426/
            └── taxonid=126822/
    
    Available Parameters by Folder Type:
    
    'figures':
        - taxonid: Species identifier (e.g., '126421')
        - model: Model type (e.g., 'mpaeu')
        - method: Algorithm (e.g., 'maxent', 'rf', 'xgboost', 'ensemble')
        - what: Type of figure (e.g., 'responsecurves', 'shape')
        - classification_ds_what: Alternative parameter for classification datasets
    
    'metrics':
        - taxonid: Species identifier
        - model: Model type
        - method: Algorithm (e.g., 'ensemble', 'maxent', 'rf', 'xgboost')
        - what: Metric type (e.g., 'cvmetrics', 'fullmetrics', 'respcurves', 'varimportance', 
                  'biasmetrics', 'posteval', 'thresholds')
        - classification_ds_what: Alternative parameter
    
    'models':
        - taxonid: Species identifier
        - model: Model type
        - method: Algorithm
        - what: 'model' (the trained model object)
        - classification_ds_what: Alternative parameter
    
    'predictions':
        - taxonid: Species identifier
        - model: Model type
        - method: Algorithm
        - scen: Scenario or time period (e.g., '1990_2000', '2000_2010', '2010_2020', '2020_2024',
                 'current', 'ssp126_dec50', 'ssp126_dec100', 'ssp245_dec50', 'ssp245_dec100',
                 'ssp370_dec50', 'ssp370_dec100', 'ssp460_dec50', 'ssp460_dec100',
                 'ssp585_dec50', 'ssp585_dec100')
        - what: Prediction type (e.g., 'mess', 'shape')
        - classification_ds_scen: Alternative parameter
    
    Example Usage:
        # Initialize the manager
        manager = SDMFileManager(r'C:\path\to\SDMs')
        
        # Get a specific predictions file
        file_path = manager.get_file(
            taxon_id='126421',
            folder_type='predictions',
            method='ensemble',
            scen='ssp585_dec100'
        )
        
        # Get all metrics for a specific method
        files = manager.get_files(
            taxon_id='126421',
            folder_type='metrics',
            method='ensemble'
        )
        
        # List available parameters for a folder type
        params = manager.list_parameters('126421', 'predictions')
        
        # Print usage examples
        manager.print_usage_examples('126421')
    """
    
    def __init__(self, sdm_root: str):
        """
        Initialize the SDM file manager.
        
        Args:
            sdm_root (str): Path to the 'SDMs' root directory containing all species folders.
                           Example: r'C:\path\to\Results\SDMs'
        
        Raises:
            FileNotFoundError: If the sdm_root directory does not exist.
        """
        self.sdm_root = Path(sdm_root)
        self.file_index = self._build_file_index()
    
    def _build_file_index(self) -> Dict:
        """
        Constructs an index of all files organized by taxon_id, folder_type, and parameters extracted from filenames.
        """
        index = {}
        
        # Iterate over species (e.g., taxonid=126421)
        for species_folder in self.sdm_root.iterdir():
            if not species_folder.is_dir():
                continue
            
            # Extract the taxon_id from the folder (taxonid=126421 -> 126421)
            taxon_id = self._extract_param_value(species_folder.name, 'taxonid')
            index[taxon_id] = {}
            
            # Iterate over model_folders (e.g., model=mpaeu)
            for model_folder in species_folder.iterdir():
                if not model_folder.is_dir():
                    continue
                
                # Iterate over folder types (figures, metrics, model, predictions)
                for type_folder in model_folder.iterdir():
                    if not type_folder.is_dir():
                        continue
                    
                    folder_type = type_folder.name  # 'figures', 'metrics', etc.
                    
                    if folder_type not in index[taxon_id]:
                        index[taxon_id][folder_type] = []
                    
                    # Iterate over files in each type folder
                    for file in type_folder.iterdir():
                        if file.is_file():
                            # Parse the filename
                            params = self._parse_filename(file.name)
                            
                            # Store file information
                            file_info = {
                                'path': str(file),
                                'filename': file.name,
                                'extension': file.suffix,
                                'params': params
                            }
                            
                            index[taxon_id][folder_type].append(file_info)
        
        return index
    
    def _extract_param_value(self, text: str, param_name: str) -> Optional[str]:
        """
        Extracts the value of a specific parameter from a text.
        
        Example: 'taxonid=126421' with param_name='taxonid' -> '126421'
                 'scen=1990_2000' with param_name='scen' -> '1990_2000'
        """
        # Pattern that captures values with underscores (e.g., 1990_2000)
        # Stops before the next parameter (which starts with _[word]=)
        pattern = rf'{param_name}=([0-9a-z_]+?)(?=_[a-z_]+(?:=|$)|$)'
        match = re.search(pattern, text)
        if match:
            value = match.group(1).strip('[]')
            return value
        return None
    
    def _parse_filename(self, filename: str) -> Dict[str, Any]:
        """
        Extracts parameters from the filename.

        Supports formats:
        - taxonid=[12642]_model=mpaeu_method=ensemble_what=cvmetrics.parquet
        - taxonid=[12642]_model=mpaeu_method=ensemble_scen=1990_2000_cog.tif
        
        Returns:
            Dictionary with the extracted parameters
        """
        params = {}
        
        # Remove the extension
        name_without_ext = os.path.splitext(filename)[0]
        
        # Search for all key-value pairs
        # Pattern: _key=value or key=value at the beginning
        # Captures values with underscores (e.g., 1990_2000) and stops before:
        # - The next parameter (_key=)
        # - A suffix (_cog, _tif, etc.)
        # - The end of the string
        pattern = r'(?:^|_)([a-z_]+)=([0-9a-z_]+?)(?=_[a-z_]+(?:=|$)|$)'
        matches = re.findall(pattern, name_without_ext)
        
        for key, value in matches:
            # Remove brackets if they exist (e.g., [12642] -> 12642)
            value = value.strip('[]')
            params[key] = value
        
        return params
    
    def get_file(self, taxon_id: str, folder_type: str, **kwargs) -> Optional[str]:
        """
        Get the path to a specific file based on search parameters.
        
        This method returns the first file matching all provided parameters.
        
        Args:
            taxon_id (str): Species identifier (e.g., '126421', '126426', '126822')
            folder_type (str): Type of folder: 'figures', 'metrics', 'models', or 'predictions'
            **kwargs: Variable parameters depending on folder_type:
                
                For 'figures':
                    method (str): e.g., 'maxent', 'rf', 'xgboost', 'ensemble'
                    what (str): e.g., 'responsecurves', 'shape'
                
                For 'metrics':
                    method (str): e.g., 'ensemble', 'maxent', 'rf', 'xgboost'
                    what (str): e.g., 'cvmetrics', 'fullmetrics', 'varimportance', 'biasmetrics'
                
                For 'models':
                    method (str): e.g., 'maxent', 'rf', 'xgboost'
                    what (str): Usually 'model'
                
                For 'predictions':
                    method (str): e.g., 'ensemble', 'maxent', 'rf', 'xgboost'
                    scen (str): e.g., '1990_2000', 'current', 'ssp585_dec100'
                    what (str): e.g., 'mess', 'shape'
        
        Returns:
            str or None: Full path to the file if found, None otherwise
        
        Example:
            # Get a specific predictions file for a time period
            path = manager.get_file(
                taxon_id='126421',
                folder_type='predictions',
                method='ensemble',
                scen='ssp585_dec100'
            )
            
            # Get metrics for a specific method
            path = manager.get_file(
                taxon_id='126421',
                folder_type='metrics',
                method='ensemble',
                what='cvmetrics'
            )
        """
        try:
            files = self.file_index[taxon_id][folder_type]
        except KeyError:
            return None
        
        # Search for the file matching all parameters
        for file_info in files:
            if self._matches_params(file_info['params'], kwargs):
                return file_info['path']
        
        return None
    
    def get_files(self, taxon_id: str, folder_type: str, **kwargs) -> List[str]:
        """
        Get all file paths matching the search parameters.
        
        This method returns all files that match the provided parameters. If no parameters
        are provided, it returns all files in the specified folder type.
        
        Args:
            taxon_id (str): Species identifier
            folder_type (str): Type of folder: 'figures', 'metrics', 'models', or 'predictions'
            **kwargs: Optional filtering parameters (see get_file for details)
        
        Returns:
            list: List of file paths matching the criteria. Empty list if no matches found.
        
        Example:
            # Get all predictions for a specific method
            files = manager.get_files(
                taxon_id='126421',
                folder_type='predictions',
                method='ensemble'
            )
            
            # Get all files for a scenario
            files = manager.get_files(
                taxon_id='126421',
                folder_type='predictions',
                scen='ssp585_dec100'
            )
            
            # Get all metric files
            files = manager.get_files(
                taxon_id='126421',
                folder_type='metrics'
            )
        """
        try:
            files = self.file_index[taxon_id][folder_type]
        except KeyError:
            return []
        
        matching_files = []
        for file_info in files:
            if self._matches_params(file_info['params'], kwargs):
                matching_files.append(file_info['path'])
        
        return matching_files
    
    def _matches_params(self, file_params: Dict, search_params: Dict) -> bool:
        """
        Check if file parameters match all search parameters.
        
        Args:
            file_params (dict): Parameters extracted from file name
            search_params (dict): Parameters to search for
        
        Returns:
            bool: True if all search parameters match, False otherwise
        """
        for key, value in search_params.items():
            if key not in file_params or file_params[key] != value:
                return False
        return True
    
    def get_file_info(self, taxon_id: str, folder_type: str, **kwargs) -> Optional[Dict]:
        """
        Get complete information about a file including path and extracted parameters.
        
        Args:
            taxon_id (str): Species identifier
            folder_type (str): Type of folder
            **kwargs: Search parameters
        
        Returns:
            dict or None: Dictionary with keys 'path', 'filename', 'extension', 'params'
                         or None if file not found
        """
        try:
            files = self.file_index[taxon_id][folder_type]
        except KeyError:
            return None
        
        for file_info in files:
            if self._matches_params(file_info['params'], kwargs):
                return file_info
        
        return None
    
    def list_taxons(self) -> List[str]:
        """
        Get a list of all available species (taxon IDs).
        
        Returns:
            list: Sorted list of taxon IDs (e.g., ['126421', '126426', '126822'])
        """
        return list(self.file_index.keys())
    
    def list_folder_types(self, taxon_id: str) -> List[str]:
        """
        Get a list of available folder types for a species.
        
        Args:
            taxon_id (str): Species identifier
        
        Returns:
            list: Available folder types (e.g., ['figures', 'metrics', 'models', 'predictions'])
        """
        return list(self.file_index.get(taxon_id, {}).keys())
    
    def list_parameters(self, taxon_id: str, folder_type: str) -> Dict[str, list]:
        """
        Get all unique parameter values available in a specific folder type.
        
        This method is useful for discovering what values are available for each parameter,
        helping you construct valid search queries.
        
        Args:
            taxon_id (str): Species identifier
            folder_type (str): Type of folder ('figures', 'metrics', 'models', 'predictions')
        
        Returns:
            dict: Dictionary where keys are parameter names and values are sorted lists
                  of available values for that parameter.
                  Example: {
                      'taxonid': ['126421'],
                      'model': ['mpaeu'],
                      'method': ['ensemble', 'maxent', 'rf', 'xgboost'],
                      'scen': ['1990_2000', '2000_2010', 'current', 'ssp585_dec100', ...],
                      'what': ['cvmetrics', 'fullmetrics', 'varimportance', ...]
                  }
        
        Example:
            params = manager.list_parameters('126421', 'predictions')
            print(params['scen'])  # ['1990_2000', '2000_2010', ..., 'ssp585_dec100']
        """
        params_dict = {}
        
        try:
            files = self.file_index[taxon_id][folder_type]
        except KeyError:
            return {}
        
        for file_info in files:
            for key, value in file_info['params'].items():
                if key not in params_dict:
                    params_dict[key] = set()
                params_dict[key].add(value)
        
        return {k: sorted(list(v)) for k, v in params_dict.items()}
    
    def print_usage_examples(self, taxon_id: Optional[str] = None):
        """
        Prints usage examples for the file manager.
        
        Args:
            taxon_id: ID of the species (if not provided, uses the first available)
        """
        if taxon_id is None:
            taxons = self.list_taxons()
            if not taxons:
                print("No specie available in the SDM root directory.")
                return
            taxon_id = taxons[0]
        
        print(f"\n{'='*60}")
        print(f"Usage examples for taxon_id={taxon_id}")
        print(f"{'='*60}\n")
        
        folder_types = self.list_folder_types(taxon_id)
        print(f"Available folder types: {folder_types}\n")
        
        for folder_type in folder_types:
            params = self.list_parameters(taxon_id, folder_type)
            if params:
                print(f"-- Folder '{folder_type}' --")
                print(f"Available parameters: {params}\n")
                
                # Generate search examples based on available parameters
                example_kwargs = {}
                
                # Priority of parameters to show
                priority_params = ['method', 'what', 'scen', 'scenario']
                
                for param in priority_params:
                    if param in params and params[param]:
                        example_kwargs[param] = params[param][0]
                        if len(example_kwargs) >= 2: 
                            break
                
                if example_kwargs:
                    print(f"Usage example:")
                    kwargs_str = ", ".join([f"{k}='{v}'" for k, v in example_kwargs.items()])
                    print(f"  manager.get_file(taxon_id='{taxon_id}', folder_type='{folder_type}',")
                    print(f"                   {kwargs_str})")
                else:
                    print(f"Usage example:")
                    print(f"  manager.get_files(taxon_id='{taxon_id}', folder_type='{folder_type}')")
                
                print()