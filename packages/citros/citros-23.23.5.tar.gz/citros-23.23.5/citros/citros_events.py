# from __future__ import absolute_import
import atexit
import json
import threading
import datetime 
import requests

def setInterval(interval):
    """
    :param interval: 
    """
    def decorator(function):
        """
        :param function: 
        """
        def wrapper(*args, **kwargs):
            """
            :param *args: 
            :param **kwargs: 
            """
            stopped = threading.Event()

            def loop():  # executed in another thread
                """ """
                while not stopped.wait(interval):  # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True  # stop if the program exits
            t.start()
            return stopped

        return wrapper

    return decorator


class citros_events():    
    """
    Handles event emission to the CiTROS server. 
    
    This class collects events and periodically sends them to the CiTROS server.
    It supports different types of events representing different stages in the lifecycle
    of a simulation.
    """
    def __init__(self, citros):
        self.citros = citros        
        
        self.timer = None
        self.events = []
        self.timer = self._flushAndRepeatTimer()
        atexit.register(self._stopFlushTimer)
        
        self.CITROS_EVENTS = f"{self.citros.CITROS_DOMAIN}/api/events"    
        
        self.seq = 0
        self._events_lock = threading.Lock()


    @setInterval(5)
    def _flushAndRepeatTimer(self):        
        self.flush()


    def _stopFlushTimer(self):        
        self.timer.set()
        self.flush()   
    

    def flush(self, current_batch=None):   
        """
        Sends all the events in current_batch to the Citros server.
        If current_batch is None, will try to send all the events from self.events

        :param current_batch:  (Default value = None)
        """
        if not self.citros.isAuthenticated():
            return
        
        # protect from the main thread running emit()
        with self._events_lock:
            if current_batch is None:
                self.events, current_batch = [], self.events 
                    
        if len(current_batch) == 0:
            return
        
        request_json = {
            "events": current_batch
        }
        
        resp = self.sync_events(request_json)   
        if not resp and current_batch is not None:
            # retry on fail.
            # protect from the main thread running emit()
            with self._events_lock: 
                self.events = current_batch + self.events
        

    def sync_events(self, request_json):
        """
        Synchronize (upload) the given batch of events with the Citros server.
        """
        if not self.citros.isAuthenticated():
            print("User is unauthenticated. please login first!")
            return
        
        try:  
            resp = requests.post(self.CITROS_EVENTS, 
                                 json=request_json, 
                                 headers={"Authorization": f"Bearer {self.citros._get_token()}"}
                                )              
            if resp.status_code != 200:
                self.citros.log.error(f"sync_events: [{self.CITROS_EVENTS}], {resp.status_code}: {resp.reason} \nresponse: {resp}")
                return False   
        except requests.exceptions.RequestException as e:
            self.citros.log.error(f"Error from sync_events: [{self.CITROS_EVENTS}]")
            self.citros.handle_exceptions(e)
            return False
        
        return True
    
    
    def emit(self, batch_run_id, sid, event_type, tag, message, metadata):
        """
        Appends an event to the event list, to be later synched with Citros.

        :param batch_run_id: batch run id
        :param sid: sequence-id of the simulation 
        :param event: event type
        :param tag: tag - can be any string
        :param message: a message for the event
        :param metadata: some dict object containing metadata.
        """
        try:
            if isinstance(metadata, dict):
                metadata = json.dumps(metadata)
        except Exception as e:
            self.citros.handle_exceptions(e)
                                    
        event = {
            "batch_run_id":batch_run_id, 
            "sid": sid, 
            "event":event_type, 
            "tag":tag, 
            "message":message,
            "metadata":metadata,
            "created": datetime.datetime.now().isoformat(),
            "seq": self.seq
        }

        self.seq = self.seq + 1

        # protect from the thread running flush()
        with self._events_lock:
            self.events.append(event)
    

    def schedule(self, batch_run_id, sid, tag="", message="", metadata=None):
        """
        Sends event of type SCHEDULE to CiTROS

        :param batch_run_id: 
        :param sid: 
        :param tag:  (Default value = "")
        :param message:  (Default value = "")
        :param metadata:  (Default value = None)
        """
        self.emit(batch_run_id, sid, "SCHEDULE", tag, message, metadata)
        

    def creating(self, batch_run_id, sid, tag="", message="", metadata=None):
        """
        Sends event of type CREATING to CiTROS

        :param batch_run_id: batch run id
        :param sid: sequence-id of the simulation         
        :param tag: tag - can be any string
        :param message: a message for the event
        :param metadata: some dict object containing metadata.
        """
        self.emit(batch_run_id, sid, "CREATING", tag, message, metadata)
    

    def init(self, batch_run_id, sid, tag="", message="", metadata=None):
        """
        Sends event of type INIT to CiTROS

        :param batch_run_id: 
        :param sid: 
        :param tag:  (Default value = "")
        :param message:  (Default value = "")
        :param metadata:  (Default value = None)
        """
        self.emit(batch_run_id, sid, "INIT", tag, message, metadata)
          

    def starting(self, batch_run_id, sid, tag="", message="", metadata=None):
        """
        Sends event of type STARTING to CiTROS
        :param batch_run_id: 
        :param sid: 
        :param tag:  (Default value = "")
        :param message:  (Default value = "")
        :param metadata:  (Default value = None)
        """
        self.emit(batch_run_id, sid, "STARTING",tag, message, metadata)
                  

    def running(self, batch_run_id, sid, tag="", message="", metadata=None):
        """
        Sends event of type RUNNING to CiTROS
        
        :param batch_run_id: 
        :param sid: 
        :param tag:  (Default value = "")
        :param message:  (Default value = "")
        :param metadata:  (Default value = None)
        """
        self.emit(batch_run_id, sid, "RUNNING", tag, message, metadata)
    

    def terminating(self, batch_run_id, sid, tag="", message="", metadata=None):
        """
        Sends event of type TERMINATING to CiTROS

        :param batch_run_id: 
        :param sid: 
        :param tag:  (Default value = "")
        :param message:  (Default value = "")
        :param metadata:  (Default value = None)
        """
        self.emit(batch_run_id, sid, "TERMINATING", tag, message, metadata)
    

    def stopping(self, batch_run_id, sid, tag="", message="", metadata=None):
        """
        Sends event of type STOPPING to CiTROS

        :param batch_run_id: 
        :param sid: 
        :param tag:  (Default value = "")
        :param message:  (Default value = "")
        :param metadata:  (Default value = None)
        """
        self.emit(batch_run_id, sid, "STOPPING", tag, message, metadata)        
        

    def done(self, batch_run_id, sid, tag="", message="", metadata=None):
        """
        Sends event of type DONE to CiTROS

        :param batch_run_id: 
        :param sid: 
        :param tag:  (Default value = "")
        :param message:  (Default value = "")
        :param metadata:  (Default value = None)
        """
        self.emit(batch_run_id, sid, "DONE", tag, message, metadata)
    
    
    def error(self, batch_run_id, sid, tag="", message="", metadata=None):
        """
        Sends event of type ERROR to CiTROS

        :param batch_run_id: 
        :param sid: 
        :param tag:  (Default value = "")
        :param message:  (Default value = "")
        :param metadata:  (Default value = None)
        """
        self.emit(batch_run_id, sid, "ERROR", tag, message, metadata)
    
    
    
