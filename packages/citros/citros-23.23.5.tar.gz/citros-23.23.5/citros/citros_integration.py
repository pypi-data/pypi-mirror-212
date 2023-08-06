from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
import json
import os

class citros_integration():
    """
    citros_integration class has all the functionality to integrate the project to CiTROS
    """
    def __init__(self, citros) -> None:
        """
        :param citros: Citros object
        """     
        self.citros = citros
        self.log = citros.log
        self.proj_jason_path = ".citros/project.json"


    def uploadParam(self, param, node_id):    
        """
        Upload a parameter to Citros.

        :param param: Parameter dictionary
        :param node_id: Node identifier
        :return: Parameter ID
        """   
        query = """
        mutation UpsertRosNodeParameter($node_id: UUID!, $name: String!, $description: String!, $value: String!, $parameterType: ParameterType) {
            upsertRosNodeParameter(
                where: {rosNodeId: $node_id, name: $name }
                input: {rosNodeParameter: {rosNodeId: $node_id, name: $name, description: $description, parameterType: $parameterType, value: $value}}                
            ) {
                rosNodeParameter {                    
                    id
                }               
            }
        }
        """
        
        print(f" - - - Parameter: {param['name']}")
        param["node_id"] = node_id
        param["value"] = str(param["value"])
        param["parameterType"] = param["parameterType"].upper()        
        if param["parameterType"] == 'LIST':
            print('*********************************************************')
            print(f'*** ERROR: parameterType {param["parameterType"]} not supported. passing. ****')
            print('*********************************************************')
            return
        
        result = self.citros.gql_execute(query, variable_values=param)
        param_id = result["upsertRosNodeParameter"]["rosNodeParameter"]["id"]
        print(" - - - param_id", param_id)
        return param_id 
    

    def uploadNode(self, node, package_id):      
        """
        Upload a node to Citros.

        :param node: Node dictionary
        :param package_id: Package identifier
        :return: Node ID
        """
        query = """
        mutation UpsertRosNode($package_id: UUID!, $name: String!, $path: String!) {
            upsertRosNode(
                where: {
                    name: $name,
                }
                input: {rosNode: {packageId: $package_id, name: $name, path: $path}}
            ) {
                rosNode {
                id
                }
            }
        }
        """
        
        node["package_id"] = package_id
        result = self.citros.gql_execute(query, variable_values=node)
        
        node_id = result.get("upsertRosNode", {}).get("rosNode", {}).get("id")
        print(f" - - node: {node['name']} [{node_id}]")
        
        print(" - - - parameters: ")
        for parameter in node.get("parameters", []):
            parameter_id = self.uploadParam(parameter, node_id)            
    
        return node_id  
    

    def uploadLaunch(self, launch, package_id):        
        """
        Upload a launch to Citros.

        :param launch: The launch details.
        :param package_id: The package ID for the launch.
        :return: The launch ID.
        """       
        query = """
        mutation upsertLaunch($data: UpsertLaunchInput!){
            upsertLaunch(input:$data) {
                launch{
                id
                name
                }
            }
        }
        """
        
        print("Launch: ")
        launch["packageId"] = package_id           
        result = self.citros.gql_execute(query, variable_values={
            "data":{
                "launch":launch
            }
        })

        launch_id = result.get("upsertLaunch", {}).get("launch", {}).get("id")
        print(" - launch_id", launch_id)
        return launch_id  
    

    def uploadPackage(self, package, project_id):
        """
        Upload a package to Citros.

        :param package: The package details.
        :param project_id: The project ID for the package.
        :return: The package ID.
        """
        query = """
        mutation UpsertRosPackage(
            $projectId: UUID!, 
            $name: String!,
            $cover: String!,
            $description: String!,
            $git: String!,
            $license: String!,
            $maintainer: String!,
            $maintainer_email: Email!,
            $path: String!,
            $readme: String!,
            $setup_py: String!,
        ) {
        upsertRosPackage(
            where: {
                name: $name,
            }
            input: {rosPackage: {
                projectId: $projectId, 
                name: $name, 
                cover: $cover, 
                description: $description, 
                git: $git,                 
                license: $license, 
                maintainer: $maintainer, 
                maintainerEmail: $maintainer_email, 
                path: $path, 
                readme: $readme, 
                setupPy: $setup_py
            }}) {
                rosPackage {
                    id
                }
            }
        }
        """
        
        package["projectId"] = project_id
        result = self.citros.gql_execute(query, variable_values=package)

        package_id = result.get("upsertRosPackage", {}).get("rosPackage", {}).get("id")
        print(f" - package: {package['name']} [{package_id}]")
                
        for node in package.get("nodes", []):
            node_id = self.uploadNode(node, package_id)            
                                
        for launch in package.get("launches", []):
            launch_id = self.uploadLaunch(launch, package_id)             
            
        return package_id        
    

    def sync_project(self, project):
        """
        Synchronize a project with Citros.

        :param project: The project details.
        :return: The project ID.
        """
        if not self.citros.isAuthenticated():                                
            self.log.error("Cant sync unauthenticated user. please log in first.")
            return
        
        partial_upsert = False
        
        if os.path.exists(self.proj_jason_path):
            with open(self.proj_jason_path, "r") as proj_file:
                # serialize and compare with previous version
                project_str = json.dumps(project, sort_keys=True)
                proj_file_data = json.load(proj_file)
                proj_file_str = json.dumps(proj_file_data, sort_keys=True)
                if project_str == proj_file_str:
                    # project is identical to previous version - 
                    # i.e. it's already synchronized, so there's nothing to do.
                    print("project already synched.")  
                    return
                else:
                    partial_upsert = True

        # if the project json file doesn't exist (or is different then the given project)
        # create it (or override the previous version).
        with open(self.proj_jason_path, "w") as outfile:
            json.dump(project, outfile, sort_keys=True, indent=4)

        if partial_upsert:
            #TODO: only synch the difference, rather then the whole project.
            pass
            
        query = """
            mutation UpsertProject(
                $name: String!, 
                $image: String!,
                $is_active: Boolean!,
                $cover: String!,
                $description: String!,
                $git: String!,
                $license: String!,
                $path: String!, 
                $readme: String!,
                $userId: UUID!
                ) {
            upsertProject(
                where: {
                    name: $name, 
                    userId: $userId
                }
                input: {
                    project: {
                        isActive: $is_active, 
                        name: $name, 
                        image: $image,
                        cover: $cover, 
                        description: $description, 
                        git: $git, 
                        license: $license, 
                        path: $path, 
                        readme: $readme, 
                        userId: $userId
                    }
                }) {
                    project {                                            
                        id
                    }                    
                }
            }
            """
        
        print("-------------------sync_project-------------------")     
        project["userId"] = self.citros.getUser().get("id")
        result = self.citros.gql_execute(query, variable_values=project)

        project_id = result.get("upsertProject", {}).get("project", {}).get("id")
        print(f"project_id: {project['name']} [{project_id}]")         
                
        for package in project.get("packages", []):
            package_id = self.uploadPackage(package, project_id)
        print("----------------------DONE------------------------")               
        
        return project_id        
        