"""
MIT License

Copyright (c) 2020 Open Ephys

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from abc import ABC, abstractmethod
import warnings
    
class Recording(ABC):
    """ Abstract class representing data from a single Recording
    
    Classes for different data formats should inherit from this class.
    
    Recording objects contain three properties:
        - continuous
        - events
        - spikes
        - messages
    
    which load the underlying data upon access.
    
    continuous is a list of data streams
        - samples (memory-mapped array of dimensions samples x channels)
        - sample_numbers (array of length samples)
        - timestamps (array of length samples)
        - metadata (contains information about the data source)
            - channel_names
            - bit_volts
            - source_node_id
            - stream_name
        
    spikes is a list of spike sources
        - waveforms (spikes x channels x samples)
        - sample_numbers (one per sample)
        - timestamps (one per sample)
        - electrodes (index of electrode from which each spike originated)
        - metadata (contains information about each electrode)
            - electrode_names
            - bit_volts
            - source_node_id
            - stream_name
        
    events is a pandas DataFrame containing six columns:
        - timestamp
        - sample_number
        - line
        - state (1 or 0)
        - processor_id
        - stream_index

    messages is a pandas DataFrame containing three columns:
        - timestamp
        - sample_number
        - message
    
    """
    
    @property
    def continuous(self):
        if self._continuous is None:
            self.load_continuous()
        return self._continuous

    @property
    def events(self):
        if self._events is None:
            self.load_events()
        return self._events

    @property
    def spikes(self):
        if self._spikes is None:
            self.load_spikes()
        return self._spikes

    @property
    def messages(self):
        if self._messages is None:
            self.load_messages()
        return self._messages
    
    @property
    def format(self):
        return self._format
    
    def __init__(self, directory, experiment_index=0, recording_index=0):
        """ Construct a Recording object, which provides access to
        data from one recording (start/stop acquisition or start/stop recording)

        Parameters
        ----------
        directory : string
            path to Record Node directory (e.g. 'Record Node 108')
        experiment_index : int
            0-based index of experiment
            defaults to 0
        recording_index : int
            0-based index of recording
            defaults to 0
        
        """
        
        self.directory = directory
        self.experiment_index = experiment_index
        self.recording_index = recording_index
        
        self._continuous = None
        self._events = None
        self._spikes = None
        self._messages = None
        
        self.sync_lines = []
        
    @abstractmethod
    def load_spikes(self):
        pass
    
    @abstractmethod
    def load_events(self):
        pass
    
    @abstractmethod
    def load_continuous(self):
        pass

    @abstractmethod
    def load_messages(self):
        pass
    
    @abstractmethod
    def detect_format(directory):
        """Return True if the format matches the Record Node directory contents"""
        pass
    
    @abstractmethod
    def detect_recordings(directory):
        """Finds Recordings within a Record Node directory"""
        pass
    
    @abstractmethod
    def __str__(self):
        """Returns a string with information about the Recording"""
        pass
    
    def add_sync_line(self, line, processor_id, stream_name=None, main=False):
        """Specifies an event channel to use for timestamp synchronization. Each 
        sync line in a recording should receive its input from the same 
        physical digital input line.
        
        For synchronization to work, there must be one (and only one) 'main' 
        sync line, to which all timestamps will be aligned.
        
        Parameters
        ----------
        channel : int
            event channel number
        processor_id : int
            ID for the processor receiving sync events (eg 101)
        stream_name : str
            name of the stream receiving sync events (eg 'Probe-A-AP')
            default = None
        main : bool
            if True, this stream's timestamps will be treated as the 
            main clock
        
        """
        
        if main:
            existing_main = [sync for sync in self.sync_lines 
                             if sync['main']]
            
            if len(existing_main) > 0:
                raise Exception('Another main sync line already exists. ' + 
                                'To override, add it again with main=False.')
                
        matching_node = [sync for sync in self.sync_lines 
                         if sync['processor_id'] == processor_id and
                            sync['stream_name'] == stream_name]
        
        if len(matching_node) == 1:
            self.sync_lines.remove(matching_node[0])
            warnings.warn('Another sync line exists for this node, overwriting.')
        
        self.sync_lines.append({'line' : line,
                                'processor_id' : processor_id,
                                'stream_name' : stream_name,
                                'main' : main})
        
    def compute_global_timestamps(self):
        """After sync channels have been added, this function computes the
        global timestamps for all processors with a shared sync line.
        
        """
        
        if len(self.sync_lines) == 0:
            raise Exception('At least two sync lines must be specified ' + 
                            'using `add_sync_line` before global timestamps ' + 
                            'can be computed.')

        main = [sync for sync in self.sync_lines 
                             if sync['main']]
        
        aux_channels = [sync for sync in self.sync_lines 
                             if not sync['main']]
            
        if len(main) == 0 or len(aux_channels) == 0:
            raise Exception('Computing global timestamps requires one ' + 
                            'main sync channel and at least one auxiliary ' +
                            'sync channel.')
            
        main = main[0]

        main_events = self.events[(self.events.line == main['line']) & 
                   (self.events.processor_id == main['processor_id']) & 
                   (self.events.stream_name == main['stream_name']) &
                   (self.events.state == 1)]
        
        main_start_sample = main_events.iloc[0].sample_number
        main_total_samples = main_events.iloc[-1].sample_number - main_start_sample
        main['start'] = main_start_sample
        main['scaling'] = 1
        main['offset'] = main_start_sample
        
        for continuous in self.continuous:

            if (continuous.metadata['source_node_id'] == main['processor_id']) and \
               (continuous.metadata['stream_name'] == main['stream_name']):
               main['sample_rate'] = continuous.metadata['sample_rate']
        
        for aux in aux_channels:
            
            aux_events = self.events[(self.events.line == aux['line']) &
                   (self.events.processor_id == aux['processor_id']) &
                   (self.events.stream_name == aux['stream_name']) &
                   (self.events.state == 1)]
            
            aux_start_sample = aux_events.iloc[0].sample_number
            aux_total_samples = aux_events.iloc[-1].sample_number - aux_start_sample
            
            aux['start'] = aux_start_sample
            aux['scaling'] = main_total_samples / aux_total_samples
            aux['offset'] = main_start_sample
            aux['sample_rate'] = main['sample_rate']

        for sync in self.sync_lines:
            
            for continuous in self.continuous:

                if (continuous.metadata['source_node_id'] == sync['processor_id']) and \
                   (continuous.metadata['stream_name'] == main['stream_name']):
                       
                    continuous.global_timestamps = \
                        ((continuous.sample_numbers - sync['start']) * sync['scaling'] \
                            + sync['offset']) 
                            
                    continuous.global_timestamps = continuous.global_timestamps / sync['sample_rate'] / sync['scaling']
                            
            event_inds = self.events[(self.events.processor_id == sync['processor_id']) & 
                   (self.events.stream_name == sync['stream_name'])].index.values

            global_timestamps = (self.events.loc[event_inds].sample_number - sync['start']) \
                                  * sync['scaling'] \
                                   + sync['offset']
                                   
            global_timestamps = global_timestamps / sync['sample_rate']
            
            for ind, ts in zip(event_inds, global_timestamps):
                self.events.at[ind, 'global_timestamp'] = ts
            
            
                            
                                              
        
        
    
        
    
