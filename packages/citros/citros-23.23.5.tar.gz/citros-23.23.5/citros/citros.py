import os

from decouple import config
import traceback
import jwt
import json
import traceback

## graphQL
from gql import Client, gql
from gql.transport.exceptions import TransportQueryError
from gql.transport.requests import RequestsHTTPTransport

import requests 

from .citros_events import citros_events
from .citros_integration import citros_integration
from .citros_utils import citros_utils
from .citros_batch import citros_batch
from .citros_bag import citros_bag
from .parsers import parser_ros2
from .citros_params import citros_params
from .logger import get_logger


class Citros:
    """
    The Citros class implements the frontend of the Citros CLI.
    It must instantiated within a `with` block in order to prevent 
    resource leaks and unexpected behavior.
    """
    def __init__(self, batch_run_id=None, simulation_run_id=None):    
        """
        Initialize Citros instance.

        Args:
        batch_run_id: An optional ID for a batch run.
        simulation_run_id: An optional ID for a simulation run.
        """
        
        self.CONFIG_DIR = ".citros"
                    
        self._user = None
        # do not access directly, only via get/set token.
        self._jwt_token = None
        
        # GQL
        self._gql_client = None
        self._token_changed = False
        
        # for logger
        self.batch_run_id = batch_run_id
        self.simulation_run_id = simulation_run_id    
        
        self.CITROS_DOMAIN = config("CITROS_DOMAIN", "https://citros.io")
        # print(f"--- using self.CITROS_DOMAIN = {self.CITROS_DOMAIN}")
        
        self.CITROS_ENTRYPOINT = f"{self.CITROS_DOMAIN}/api/graphql"
        self.CITROS_LOGS = f"{self.CITROS_DOMAIN}/api/logs"        
        self.CITROS_GTOKEN = f"{self.CITROS_DOMAIN}/api/gtoken" 
        self.CITROS_HEALTH_CHECK = f"{self.CITROS_DOMAIN}/api/check" 
          
        self.log = None
        self.listener = None
        self.log, self.listener = get_logger(__name__, self.sync_logs, self.batch_run_id, self.simulation_run_id)
        
        self._init_components()
    

    def _init_components(self):
        self.events = citros_events(self)        
        self.parser_ros2 = parser_ros2(self.log)
        self.integration = citros_integration(self)        
        self.params = citros_params(self)
        self.utils = citros_utils(self)
        self.bag = citros_bag(self)
        self.batch = citros_batch(self)


    def handle_exceptions(self, e):
        """
        Handles exceptions and logs them.

        Args:
        e: Exception to handle.
        """
        stack_trace = traceback.format_exception(type(e), e, e.__traceback__)
        stack_trace_str = "".join(stack_trace)
        self.log.exception(stack_trace_str)


    def __enter__(self):
        """
        Returns the Citros instance. This allows the class to be used in a `with` statement.
        """
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Stops the log listener and handles exceptions.

        Args:
        exc_type: The type of exception.
        exc_val: The exception instance.
        exc_tb: A traceback object encapsulating the call stack at the point 
                where the exception originally occurred.
        """
        if exc_type is not None:
            self.handle_exceptions(exc_val)

        # Stop the log listener in order to flush the queue.
        # If you don't call this before your application exits, there may 
        # be some records still left on the queue, which won't be processed.
        if self.listener:     
            self.listener.stop()


    def _remove_token(self):
        """
        Removes the JWT token.
        """
        self._set_token(None)


    def _validate_token(self, token):
        """
        Validates the JWT token.

        Args:
        token: JWT token to validate.

        Returns:
        Boolean indicating if the token is valid.
        """
        # TODO: Implement token validation (may be None!)
        return True


    def _set_token(self, jwt_token):
        """
        Sets the JWT token.

        Args:
        jwt_token: JWT token to set.
        """
        if not self._validate_token(jwt_token):
            self.log.error("Invalid JWT token.")
            return

        if not jwt_token or jwt_token.strip() == '':
            self._jwt_token = None
            self._token_changed = True
            try:
                os.remove(f"{self.CONFIG_DIR}/auth")
            except FileNotFoundError as e:
                pass # its ok that there is no file.                
            except Exception as e:
                self.handle_exceptions(e)
            return    
            
        if not os.path.isdir(self.CONFIG_DIR):
            os.makedirs(self.CONFIG_DIR)
            
        try:
            with open(f"{self.CONFIG_DIR}/auth", mode='w') as file:            
                file.write(jwt_token)      
        except Exception as e:
            self.handle_exceptions(e)
        finally:
            self._jwt_token = jwt_token
            self._token_changed = True                        
        
        return self._jwt_token


    def _get_token(self):
        """
        Gets the JWT token.
        """
        try:
            if self._jwt_token:
                return self._jwt_token
            
            with open(f"{self.CONFIG_DIR}/auth", mode='r') as file:            
                self._jwt_token = file.read()
                self._token_changed = True
        except FileNotFoundError as e:
            # Key file wasn't found. assuming the user is not logged in...
            self._jwt_token = None
            return None
        except Exception as e:
            self.handle_exceptions(e)
        
        if not self._validate_token(self._jwt_token):
            self.log.error("JWT token is invalid, removing.")
            self._remove_token()

        return self._jwt_token
    
    ################################# Public #################################
    
    def logout(self):
        """
        Logs out of CiTROS
        """
        self._remove_token()
        self._user = None
        
    
    def isAuthenticated(self):
        """
        returns the authentication status

        Returns:
            boolean: True if the user is logged in. 
        """        
        return self._get_token() is not None


    def checkStatus(self):
        """
        Checks the current status of the user authentication

        Returns:
            boolean: True if the user is authenticated and health check passes. 
        """ 
        if not self.isAuthenticated():
            print("User is not logged in. please log in first.")
            return False
     
        try:
            resp = requests.post(self.CITROS_HEALTH_CHECK, headers={
                "Authorization": f"Bearer {self._get_token()}"
            })                
            if resp.status_code == 200 and resp.text == "OK":
                return True
            else:
                self.log.error(f"Health check failed with status code {resp.status_code} and response {resp.text}")
        except requests.exceptions.RequestException as err:
            print("Can't get access token at this moment...")
            self.handle_exceptions(err)
            
        return False


    def authenticate_with_key(self, key):
        """
        Login to CiTROS using a key.

        Args:
            key (str): a key generated by CiTROS system.

        Returns:
            bool: True if the login attempt was successful, False otherwise.
        """   
        self.logout()
        
        query = """
            mutation auth($key: AuthenticateKeyInput!){
                authenticateKey(input: $key){
                    results {
                    _role
                    fail
                    message
                    }
                }
            }
            """
        try:  
            result = self.gql_execute(query, variable_values={ "key": {"jwtToken": key}})
            
            if result is None or "authenticateKey" not in result:
                self.log.error("Error during authentication: No response from server.")
                return False

            if not result["authenticateKey"]["results"][0]["fail"]:
                token = key
            else:
                self.log.error("ERROR during authentication: unrecognized authentication key.")
                token = None
                return False
            
            self._set_token(token)
            self.log.info("User authenticated.")
            return True
        
        except Exception as ex:
            self.log.error("Authentication failed - exception was thrown.")
            token = None
            self.handle_exceptions(ex)
            return False


    def login(self, email, password):
        """
        Login to CiTROS using an email and password

        Args:
            email (str): the user email 
            password (str): the user's password

        Returns:
            bool: True if the login attempt was successful, False otherwise.
        """                  
        if self.isAuthenticated():
            return True
        
        query = """
            mutation AuthenticateUser($email: String!, $password: String!) {
                authenticate(input: {
                    email: $email, 
                    password: $password
                }) {
                    jwt
                }
            }
            """        
        result = self.gql_execute(query, variable_values={
            "email": email,
            "password": password
        })

        if result is None or 'authenticate' not in result or 'jwt' not in result['authenticate']:
            self.log.error("Failed to log in. Response: " + result)
            return False

        token = result["authenticate"]["jwt"]
        
        try:
            # bug fix. added audience as it didn't work in some cases. 
            decoded = jwt.decode(token, options={"verify_signature": False}, audience="postgraphile")
        except jwt.exceptions.DecodeError as err:
            self.log.error("Failed to log in. token: " + token) 
            self.handle_exceptions(err)
            return False
        
        if token and decoded["role"] != "citros_anonymous":
            self._set_token(token)
            self.log.info("User authenticated.")
            return True
        else:
            self.log.error(f"Authentication attempt failed: wrong username or password for [{email}]")
            return False


    def getUser(self):
        """
        Returns the currently logged in user with all their data from CiTROS.

        This includes their ID, username, role ID and name, and their
        organization's ID, name, and domain prefix.

        Returns:
            dict: The user data, or None if the user is not logged in or an
                  error occurred.
        """           
        if self._user:
            return self._user
        
        query = """
            query getCurrentUser {
                currentUser {  
                    id        
                    username        
                    role{
                        id
                        role
                    }           
                    organization{
                        id 
                        name
                        domainPrefix
                    }                    
                }
            }  
            """
        
        try:
            result = self.gql_execute(query)
            if result is None or 'currentUser' not in result:
                self.log.error("Error during getUser: No response or unexpected response format from server.")
                self._user = None
            else:
                self._user = result["currentUser"]
        except Exception as e:
            self.handle_exceptions(e)
            self.logout()

        return self._user
    
    ################################# Docker #################################
    
    def get_access_token(self):
        """
        Fetches an access token if the user is authenticated.

        Returns:
            str: The access token, or None if the user is not authenticated or an error occurred.
        """
        if not self.isAuthenticated():
            print("user is not logged in. please log in first.")
            return 
        
        rest_data = None
             
        try:
            resp = requests.post(self.CITROS_GTOKEN, headers={
                "Authorization": f"Bearer {self._get_token()}"
            })
            resp.raise_for_status()     
            rest_data = resp.json()
        except requests.HTTPError as ex:
            self.log.error("HTTP error occurred during get_access_token")
            self.handle_exceptions(ex)
            return
        except requests.RequestException as ex:
            self.log.error("A network error occurred during get_access_token")
            self.handle_exceptions(ex)
            return
        except json.JSONDecodeError as ex:
            self.log.error("Failed to decode JSON response during get_access_token")
            self.handle_exceptions(ex)
            return
        
        try:
            token = rest_data["access_token"]            
            expires_in = rest_data["expires_in"]
            token_type = rest_data["token_type"]
        except KeyError as ex:
            self.log.error("Failed to fetch access token, expected key not found in response.")
            self.handle_exceptions(ex)
            return None
        return token
            
    ################################# GraphQL #################################
       
    def _get_transport(self):
        """
        Obtain transport with authorization if user is authenticated.
        """                      
        transport = RequestsHTTPTransport(
            url=self.CITROS_ENTRYPOINT,
            verify=True,
            retries=3            
        )     
        # create GQL client for user or for anonymous user. 
        if self.isAuthenticated():
            transport.headers = {
                "Authorization": f"Bearer {self._get_token()}"
            }
        return transport


    def _get_gql_client(self):
        """
        Obtain GraphQL client.
        """
        if self._gql_client and not self._token_changed:
            return self._gql_client
        # https://gql.readthedocs.io/en/v3.0.0a6/intro.html
        transport = self._get_transport()
        self._gql_client = Client(transport=transport, fetch_schema_from_transport=False)
        self._token_changed = False
        return self._gql_client


    def gql_execute(self, query, variable_values=None):
        """
        Execute a GraphQL query.

        Args:
            query (gql): gql query
            variable_values (dict, optional): variables for the gql query. Defaults to None.

        Returns:
            dict: Result of the executed query.
        """
        
        gql_query = gql(query)
        try:
            return self._get_gql_client().execute(gql_query, variable_values=variable_values)
        except TransportQueryError as ex:                    
            self.log.error(f"Error while querying: query={query} variable_values={variable_values}")
            self.handle_exceptions(ex)     
            if ex.errors[0].get('errcode', '') == "23503":                
                self.logout()
        except Exception as e:    
            self.log.error(f"Error while querying: query={query} variable_values={variable_values}")
            self.handle_exceptions(ex)
                           
        return None
    
    ############################### CITROS sync ###############################

    def sync_logs(self, log_content):
        """Synchronizes logs with the CiTROS system.

        Args:
            log_content (json): The log data to be synchronized.

        Returns:
            bool: True if the synchronization was successful, False otherwise.
        """
        if not self.isAuthenticated():
            # print("User is unauthenticated. please login first!")
            return
           
        try:           
            resp = requests.post(
                self.CITROS_LOGS, 
                json=log_content, 
                headers={"Authorization": f"Bearer {self._get_token()}"}
            )      

            if resp.status_code != 200:
                self.log.error(f"Error from sync_logs: {resp.status_code}: {resp.reason}")
                return False
        except requests.RequestException as e:
            self.log.error(f"Error from sync_logs. log content = {log_content}")
            self.handle_exceptions(e)
            return False
        
        return True
    
    ############################### CITROS list ###############################
    
    def query_projects(self):
        """
        Queries the names of all projects in the CiTROS system.

        Returns:
            list: A list of project names, or an empty list if no projects are found.
        """
        query = """
            query projects {
                projectsList(orderBy: CREATED_AT_DESC) {
                    name
                    user{
                        id
                        username
                    }
                }
            }
        """
        try:
            data = self.gql_execute(query)
        except Exception as e:
            self.handle_exceptions(e)
            self.logout()
        
        if not data or not data.get("projectsList"):
            self.log.info("No projects found.")
            return []

        return data["projectsList"]

    
    def query_simulations(self, proj_name):
        """Queries the IDs of all simulations in a specified project.

        Args:
            proj_name (str): The name of the project.

        Returns:
            list: A list of simulation IDs, or an empty list if no simulations are found.
        """
        query = """
            query sim_ids($name: String = "", $userID:UUID!) {
                projectsList(orderBy: CREATED_AT_DESC, condition: {name: $name, userId:$userID}) {
                    name
                    simulationsList(orderBy: CREATED_AT_ASC) {
                        id
                        name
                    }
                }
            }
        """
        try:

            data = self.gql_execute(query, variable_values={"name": proj_name, "userID": self.getUser()["id"]})
        except Exception as e:
            self.handle_exceptions(e)
            self.logout()

        if not data or not data.get("projectsList") or not data["projectsList"][0].get("simulationsList"):
            print(f"No simulations found for project {proj_name}.")
            return []

        return data["projectsList"][0]["simulationsList"]