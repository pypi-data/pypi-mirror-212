class citros_batch():
    def __init__(self, citros):
        self.citros = citros      
        self.log = citros.log
                        
    def get_batch(self, batch_run_id):
        query = """
        query getData($batchRunId: UUID!) {
            batchRun(id: $batchRunId) {
                id                
                completions
                parallelism                
                simulation {
                    id
                    timeout
                    launch {
                        id
                        name
                        package {
                            id
                            name
                        }
                    }
                }
            }            
        }
        """
        result = self.citros.gql_execute(query, variable_values={"batchRunId": batch_run_id})
        return result
    
    def create_manual_batch(self, simulation_id, completions, isManual):
        query = """
        mutation createBatch($simulationId: UUID!, $completions: Int, $isManual: Boolean = true, $trigger: TriggerType = MANUAL) {
                      createBatchRun(
                        input: {
                            batchRun: {
                                simulationId: $simulationId, 
                                completions: $completions, 
                                parallelism: 0, 
                                trigger: $trigger, 
                                isManual: $isManual}}
                      ) {
                        batchRun {
                          id
                        }
                      }
                    }

        """ 
        trigger = "MANUAL" if isManual else "CLI"
        result = self.citros.gql_execute(query, variable_values={"simulationId": simulation_id, 
                                                                 "completions": int(completions),
                                                                 "isManual" : isManual,
                                                                 "trigger" : trigger})
        return result["createBatchRun"]["batchRun"]["id"]    
        
   
   