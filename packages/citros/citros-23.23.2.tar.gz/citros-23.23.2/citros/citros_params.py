import yaml
import json
import os
import numpy as np
from pathlib import Path
from decouple import config


class citros_params():
    def __init__(self, citros):
        self.citros = citros
        self.log = citros.log
        self.CONFIG_FOLDER = config("CONFIG_FOLDER", 'tmp/config')
    
    
    def _get_params(self, batch_run_id, sid=""):
        query = """
        query getParametersFromBatchRun($batchRunId: UUID!, $sid: String!){
            batchRun(id:$batchRunId){
                id                
                simulation {
                project {
                    rosPackagesList {
                        id
                        name
                        rosNodesByPackageIdList {
                        id
                        name
                        rosNodeParametersList {
                            id
                            name
                            value
                            parameterType
                        }
                        }
                    }
                }
                parameterSetup{
                    id
                    name
                    parameterSettingsList {
                            param1
                            param1Type
                            param2
                            param2Type
                            distType
                            id
                            nodeParameterId
                        }          
                    }
                }                
            }
            simulationEventsList(
                condition: {sid: $sid, batchRunId: $batchRunId, event: STARTING, tag: "CONFIG"}
            ) {                
                metadata
            }
        }
        """
        result = self.citros.gql_execute(query, variable_values={"batchRunId": batch_run_id, "sid": sid})        
        return result
   

    def _coercion(self, value, type):
        if type == "FLOAT":
            return float(value)
        if type == "INT":
            return int(float(value))
        return value
        
    
    def _eval_distribution(self, parameter_setting):
        distribution_type = parameter_setting["distType"]
        param1 = self._coercion(parameter_setting["param1"], parameter_setting["param1Type"])
        param2 = self._coercion(parameter_setting["param2"], parameter_setting["param2Type"])

        distribution_mapping = {
                "NORMAL": lambda: np.random.normal(param1, param2),
                "EXPONENTIAL": lambda: np.random.exponential(param1),
                "LAPLACE": lambda: np.random.laplace(param1, param2),
                "POISSON": lambda: np.random.poisson(param1),
                "POWER": lambda: np.random.power(param1),
                "UNIFORM": lambda: np.random.uniform(param1, param2),
                "ZIPF": lambda: np.random.zipf(param1),
                "VONMISES": lambda: np.random.vonmises(param1, param2),
                "RAYLEIGH": lambda: np.random.rayleigh(param1),
                "FLOAT": lambda: self._coercion(param1, parameter_setting["param1Type"]),
                "STRING": lambda: param1,
        }
        try:
                return distribution_mapping[distribution_type]()
        except KeyError:
                self.log.error(f"Error: {distribution_type} is not supported.")   
        
    
    def get_config(self, batch_run_id, sid=""):
        data = self._get_params(batch_run_id, sid)
        if not data:
            self.log.error("Did not get any data from GQL.")
            return 
        
        # in case sid is provided, and there was already a run with this sid. 
        # load original config to run it again.
        reloaded_parameters = None
        if data["simulationEventsList"]:
            reloaded_parameters = json.loads(data["simulationEventsList"][0]["metadata"])
            self.log.info(f"Reloaded config from already used [batch_run_id-sid] [{batch_run_id}-{sid}]")
            return reloaded_parameters
            
        if data["batchRun"]["simulation"] is None:
            self.log.error("ERROR! Cant get parameters from CiTROS. There is no simulation attached to batch.")  
            return     
              
        # users parameter setup
        parameter_settings_list = data["batchRun"]["simulation"]["parameterSetup"]["parameterSettingsList"]
        try:
            paramValues = {str(ps["nodeParameterId"]): self._eval_distribution(ps) for ps in parameter_settings_list}
        except Exception as e:
            self.log.error(f"Error in _eval_distribution, parameter_settings_list")
            raise e
        
        # load defaults from ros nodes. 
        ros_packages_list = data["batchRun"]["simulation"]["project"]["rosPackagesList"]
        config = {}   
        for package in ros_packages_list:
            config[package["name"]] = {}
            for node in package["rosNodesByPackageIdList"]:                
                config[package["name"]][node["name"]] = {
                    "ros__parameters": {}
                }
                for parameter in node["rosNodeParametersList"]:                    
                    value = self._coercion(parameter['value'], parameter['parameterType'])
                    paramValue = paramValues.get(str(parameter["id"]))
                    if paramValue:
                        value = paramValue
                    config[package["name"]][node["name"]]["ros__parameters"][parameter['name']] = value                                                             
        return config   
    

    def save_config(self, config):  
        # callback running inside ROS workspace context.   
        from ament_index_python.packages import get_package_share_directory

        Path(self.CONFIG_FOLDER).mkdir(exist_ok=True, parents=True)
                
        for package_name, citros_config in config.items():     
            self.log.debug(f"Saving config for [{package_name}]")

            # TODO: add other method to get the package path
            path_to_package = None
            try:
                # get the path to the package install directory - the project must be sourced for it to work 
                path_to_package = get_package_share_directory(package_name)            
            except Exception as e:
                self.log.exception(e)
                continue                

            if not path_to_package:
                continue
                
            path = f"{path_to_package}/config/"    
            
            # check if folder exists
            if not Path(path).exists():
                self.log.debug(f"No config file {path} exits for pack:{package_name}. passing.") 
                continue
                                                
            Path(path).mkdir(parents=True, exist_ok=True)
            path = path + "params.yaml"
            
            # check if file exists
            if not Path(path).exists():
                self.log.debug(f"No config file {path} exits for package: {package_name}. passing.") 
                continue
            
            with open(path, "r") as stream:
                try:    
                    default_config = yaml.safe_load(stream)
                except yaml.YAMLError as exc:
                    self.log.exception(exc)
            
            merged_config = {**default_config, **citros_config}
            self.log.debug(json.dumps(merged_config, indent=4))
            
            with open(path, 'w') as file:
                yaml.dump(merged_config, file)  
                
            # save for metadata
            with open(f"{self.CONFIG_FOLDER}/{package_name}.yaml", 'w') as file:                                     
                yaml.dump(merged_config, file)         
    

    def init_params(self, batch_run_id, sid):
        """
        Fetches parameters from CITROS, saves them to files, and returns the config.
        """          
        self.log.info("Getting parameters from CITROS.") 
        config = self.get_config(batch_run_id, sid)
        if not config:
            self.log.warning("There is no config, can't init anything...") 
            return
        
        self.log.debug("Saving parameters to files. ")        
        self.save_config(config)     
        self.log.debug("Done saving config files.")                    
        return config
        