# pypl2api_enhanced.py - High level functions for accessing
# .pl2 files. This API is designed around Python's capabilities,
# and does not mimic APIs written in any other languages
#
# (c) 2016 Plexon, Inc., Dallas, Texas
# www.plexon.com
#
# This software is provided as-is, without any warranty.
# You are free to modify or share this file, provided that the above
# copyright notice is kept intact.

import re
from collections import namedtuple
import numpy as np
try:
    from .pypl2lib import *
except ImportError:
    from pypl2lib import *
from enum import Enum
from ctypes import *

# declare an Enum for source names
class SOURCES(Enum):
    WB = 1
    SPKC = 2
    SPK = 3
    FP = 4
    AIF = 5

# declare named tuples
AnalogChannelTuple = namedtuple("AnalogChannelTuple", "num_fragments_returned num_data_points_returned fragment_timestamps fragment_counts values")
SpikeChannelTuple = namedtuple("SpikeChannelTuple", "num_spikes_returned spike_timestamps units waveforms")
EventChannelTuple = namedtuple("EventChannelTuple", "num_events_returned, event_timestamps, event_values")
CommentsTuple = namedtuple("CommentsTuple", "timestamps comments")

# create reader class that contains all file reading operations
class PL2EnhancedReader(object):
    """
    Class for reading PL2 files
    """

    # constructor
    def __init__(self, filename):
        self.__filename = filename                  # make private with associated property getter to avoid editing
        self.__file_reader = PyPL2FileReader()      # make private
        self.__file_handle = self.__open_file(self.__filename)           # declares self.__file_handle
        self.__file_info = self.get_file_info()
        self.__source_names, \
            self.__MAP_source_names_to_ids, \
            self.__MAP_source_names_to_channels, \
            self.__MAP_channel_names_to_zero_based_channel_indexes, \
            self.__MAP_source_name_and_one_based_channel_index_to_zero_based_channel_index = self.__analyze_sources_and_channels()

    # getters / setters
    @property
    def filename(self):
        return self.__filename
    
    @property
    def source_names(self):
        return self.__source_names
    
    @property
    def channel_names_for_source(self):
        """
        Dictionary keyed on source name with channel lists as values

        Usage:
            channel_list = self.channel_names_for_source["WB"]
        """
        return self.__MAP_source_names_to_channels
    

    ###############################################################################
    # public functions
    ###############################################################################

    # file info
    def get_file_info(self):
        """
        Returns PL2 file info

        Usage:
            file_info = self.get_file_info()
        
        Args:
            None
        
        Returns:
            file_info - Object containing information about the PL2 file
        """
        file_info = PL2FileInfo()
        result = self.__file_reader.pl2_get_file_info(self.__file_handle, file_info)

        if result == 0:
            self.__print_error()
            return 0
        
        return file_info

    # analog channels
    def get_analog_channel_info(self, zero_based_channel_index:int=None, channel_name:str=None, source_name:str=None, one_based_channel_index:int=None):
        """
        Returns info for analog channel

        Usage:
            analog_channel_info = self.get_analog_channel_info(zero_based_channel_index=0)

            -or-

            analog_channel_info = self.get_analog_channel_info(channel_name="WB01")

            -or-

            analog_channel_info = self.get_analog_channel_info(source_name="WB", one_based_channel_index=1)

        Args:
            zero_based_channel_index - zero-based channel index
            channel_name - name of channel (e.g., "WB01", "SPKC03")
            source_name - name of source (e.g., "WB", "SPKC", "FP", "SPK")
            one_based_channel_index - one-based channel index

            Note - the following combinations of arguments are allowed:
                1. zero_based_channel_index
                2. channel_name
                3. source_name + one_based_channel_index
        Returns:
            analog_channel_info - Object containing information about analog channel
        """
        zero_based_channel_index = self.__get_zero_based_channel_index(zero_based_channel_index=zero_based_channel_index, channel_name=channel_name, source_name=source_name, one_based_channel_index=one_based_channel_index)
        analog_channel_info = PL2AnalogChannelInfo()
        result = self.__file_reader.pl2_get_analog_channel_info(self.__file_handle, zero_based_channel_index, analog_channel_info)

        if result == 0:
            self.__print_error()
            return 0
        
        return analog_channel_info
    
    def get_analog_channel_data(self, zero_based_channel_index:int=None, channel_name:str=None, source_name:str=None, one_based_channel_index:int=None):
        """
        Returns all data for analog channel

        Usage:
            analog_channel_tuple = self.get_analog_channel_data(zero_based_channel_index=0)

            -or-

            analog_channel_tuple = self.get_analog_channel_data(channel_name="WB01")

            -or-

            analog_channel_tuple = self.get_analog_channel_data(source_name="WB", one_based_channel_index=1)
        
        Args:
            zero_based_channel_index - zero-based channel index
            channel_name - name of channel (e.g., "WB01", "SPKC03", "FP05")
            source_name - name of source (e.g., "WB", "SPKC", "FP"")
            one_based_channel_index - one-based channel index

            Note - the following combinations of arguments are allowed:
                1. zero_based_channel_index
                2. channel_name
                3. source_name + one_based_channel_index

        Returns:
            analog_channel_tuple - NamedTuple containing the following fields:
                                        - num_fragments_returned    -   number of fragments returned
                                        - num_data_points_returned  -   number of data points returned
                                        - fragment_timestamps       -   numpy array containing starting time stamps (in ticks) of each fragment. Array may have more elements than there are fragments - extra elements have value 0.
                                        - fragment_counts           -   numpy array containing number of values in each fragment. Array may have more elements than there are fragments - extra elements have value 0.
                                        - values                    -   numpy array containing scaled signal for analog channel
        """
        zero_based_channel_index = self.__get_zero_based_channel_index(zero_based_channel_index=zero_based_channel_index, channel_name=channel_name, source_name=source_name, one_based_channel_index=one_based_channel_index)
        analog_channel_info = self.get_analog_channel_info(zero_based_channel_index=zero_based_channel_index)

        # retrieve analog channel data
        num_fragments_returned = c_ulonglong(0)
        num_data_points_returned = c_ulonglong(0)
        fragment_timestamps = (c_longlong * analog_channel_info.m_MaximumNumberOfFragments)()
        fragment_counts = (c_ulonglong * analog_channel_info.m_MaximumNumberOfFragments)()
        values = (c_short * analog_channel_info.m_NumberOfValues)()
        result = self.__file_reader.pl2_get_analog_channel_data(self.__file_handle, zero_based_channel_index, num_fragments_returned, num_data_points_returned, fragment_timestamps, fragment_counts, values)
        
        if result == 0:
            self.__print_error()
            return 0
        
        return AnalogChannelTuple(num_fragments_returned.value, num_data_points_returned.value, np.array(fragment_timestamps, dtype=np.float32), np.array(fragment_counts, dtype=np.float32), np.array(values, dtype=np.float32)*analog_channel_info.m_CoeffToConvertToUnits)


    def get_analog_channel_data_subset(self, start_timestamp, end_timestamp=None, duration=None, zero_based_channel_index:int=None, channel_name:str=None, source_name:str=None, one_based_channel_index:int=None):     # need to add more arguments
        """
        Returns subset of data for analog channel

        Usage:
            analog_channel_tuple = self.get_analog_channel_data_subset(start_timestamp, <end_timestamp OR duration>, zero_based_channel_index=0)

            -or-

            analog_channel_tuple = self.get_analog_channel_data_subset(start_timestamp, <end_timestamp OR duration>, channel_name="WB01")

            -or-

            analog_channel_tuple = self.get_analog_channel_data_subset(start_timestamp, <end_timestamp OR duration>, source_name="WB", one_based_channel_index=1)
        
        Args:
            start_timestamp - timestamp (in seconds) for subset start time
            end_timestamp - timestamp (in seconds) for subset end time
            duration - duration of subset
            zero_based_channel_index - zero-based channel index
            channel_name - name of channel (e.g., "WB01", "SPKC03", "FP05")
            source_name - name of source (e.g., "WB", "SPKC", "FP")
            one_based_channel_index - one-based channel index

            Note - the following combinations of arguments are allowed for subset selection:
                1. start_timestamp + end_timestamp
                2. start_timestamp + duration
            
            Note - the following combinations of arguments are allowed for channel selection:
                1. zero_based_channel_index
                2. channel_name
                3. source_name + one_based_channel_index

        Returns:
            analog_channel_tuple - NamedTuple containing the following fields:
                                        - num_fragments_returned    -   number of fragments returned
                                        - num_data_points_returned  -   number of data points returned
                                        - fragment_timestamps       -   tuple containing starting time stamps (in ticks) of each fragment. Array may have more elements than there are fragments - extra elements have value 0.
                                        - fragment_counts           -   tuple containing number of values in each fragment. Array may have more elements than there are fragments - extra elements have value 0.
                                        - values                    -   numpy array containing scaled signal for analog channel
        """
        # must not pass both end_timestamp and duration
        if not ((end_timestamp==None) ^ (duration==None)):      # ^ is XOR boolean operator
            error_message = "You must only pass *one* of end_timestamp and duration."
            s = f" You passed:\n\t{end_timestamp=}\n\t{duration=}"
            error_message += s
            raise ArgumentError(error_message)
        
        # get analog channel info and calculate starting index, number of values
        zero_based_channel_index = self.__get_zero_based_channel_index(zero_based_channel_index=zero_based_channel_index, channel_name=channel_name, source_name=source_name, one_based_channel_index=one_based_channel_index)
        analog_channel_info = self.get_analog_channel_info(zero_based_channel_index=zero_based_channel_index)
        zero_based_start_value_index = int(start_timestamp * analog_channel_info.m_SamplesPerSecond)

        # calculate the number of values to be pulled
        if end_timestamp != None and duration==None:
            num_subset_values = int(np.floor(end_timestamp*analog_channel_info.m_SamplesPerSecond) - np.floor(start_timestamp*analog_channel_info.m_SamplesPerSecond))
        else:
            num_subset_values = int(duration * analog_channel_info.m_SamplesPerSecond)

        # retrieve subset of analog channel data
        num_fragments_returned = c_ulonglong(0)
        num_data_points_returned = c_ulonglong(0)
        fragment_timestamps = (c_longlong * analog_channel_info.m_MaximumNumberOfFragments)()
        fragment_counts = (c_ulonglong * analog_channel_info.m_MaximumNumberOfFragments)()
        values = (c_short * num_subset_values)()

        result = self.__file_reader.pl2_get_analog_channel_data_subset(self.__file_handle, zero_based_channel_index, zero_based_start_value_index, num_subset_values, num_fragments_returned, num_data_points_returned, fragment_timestamps, fragment_counts, values)
        if result == 0:
            self.__print_error()
            return 0
        
        return AnalogChannelTuple(num_fragments_returned.value, num_data_points_returned.value, tuple(fragment_timestamps), tuple(fragment_counts), np.array(values, dtype=np.float32)*analog_channel_info.m_CoeffToConvertToUnits)


    # spike channels
    def get_spike_channel_info(self, zero_based_channel_index:int=None, channel_name:str=None, source_name:str=None, one_based_channel_index:int=None):
        """
        Returns info for spike channel

        Usage:
            spike_channel_info = self.get_spike_channel_info(zero_based_channel_index=0)

            -or-

            spike_channel_info = self.get_spike_channel_info(channel_name="SPK01")

            -or-

            spike_channel_info = self.get_spike_channel_info(source_name="SPK", one_based_channel_index=1)

        Args:
            zero_based_channel_index - zero-based channel index
            channel_name - name of channel (e.g., "SPK01")
            source_name - name of source (e.g., "SPK")
            one_based_channel_index - one-based channel index

            Note - the following combinations of arguments are allowed:
                1. zero_based_channel_index
                2. channel_name
                3. source_name + one_based_channel_index
        Returns:
            spike_channel_info - Object containing information about spike channel
        """
        zero_based_channel_index = self.__get_zero_based_channel_index(zero_based_channel_index=zero_based_channel_index, channel_name=channel_name, source_name=source_name, one_based_channel_index=one_based_channel_index)
        spike_channel_info = PL2SpikeChannelInfo()
        result = self.__file_reader.pl2_get_spike_channel_info(self.__file_handle, zero_based_channel_index, spike_channel_info)

        if result == 0:
            self.__print_error()
            return 0
        
        return spike_channel_info


    def get_spike_channel_data(self, zero_based_channel_index:int=None, channel_name:str=None, source_name:str=None, one_based_channel_index:int=None):
        """
        Returns all data for spike channel

        Usage:
            spike_channel_tuple = self.get_spike_channel_data(zero_based_channel_index=0)

            -or-

            spike_channel_tuple = self.get_spike_channel_data(channel_name="SPK01")

            -or-

            spike_channel_tuple = self.get_spike_channel_data(source_name="SPK", one_based_channel_index=1)
        
        Args:
            zero_based_channel_index - zero-based channel index
            channel_name - name of channel (e.g., "SPK01")
            source_name - name of source (e.g., "SPK")
            one_based_channel_index - one-based channel index

            Note - the following combinations of arguments are allowed:
                1. zero_based_channel_index
                2. channel_name
                3. source_name + one_based_channel_index

        Returns:
            spike_channel_tuple - NamedTuple containing the following fields:
                                    - num_spikes_returned - total number of spikes returned for the specified channel
                                    - spike_timestamps - tuple containing time stamp (in ticks) for each returned spike
                                    - units - tuple containing unit identity for each returned spike
                                    - waveforms - tuple containing waveform for each returned spike
        """
        zero_based_channel_index = self.__get_zero_based_channel_index(zero_based_channel_index=zero_based_channel_index, channel_name=channel_name, source_name=source_name, one_based_channel_index=one_based_channel_index)
        spike_channel_info = self.get_spike_channel_info(zero_based_channel_index=zero_based_channel_index)
        
        # retrieve spike channel data
        num_spikes_returned = c_ulonglong(0)
        spike_timestamps = (c_ulonglong * spike_channel_info.m_NumberOfSpikes)()
        units = (c_ushort * spike_channel_info.m_NumberOfSpikes)()
        values = (c_short * (spike_channel_info.m_NumberOfSpikes * spike_channel_info.m_SamplesPerSpike))()
        result = self.__file_reader.pl2_get_spike_channel_data(self.__file_handle, zero_based_channel_index, num_spikes_returned, spike_timestamps, units, values)
        if result == 0:
            self.__print_error()
            return 0

        # extract the scaled waveforms from "values" into a multi-dimensional
        # Python tuple. The following code block is copied directly from 
        # the original pypl2api.py.
        waveforms = []
        current_location = 0
        breadth = spike_channel_info.m_SamplesPerSpike
        for i in range(num_spikes_returned.value):
            temp = values[current_location : current_location + breadth]
            waveforms.append(temp)
            current_location += breadth
        
        return SpikeChannelTuple(num_spikes_returned.value, tuple(spike_timestamps), tuple(units), tuple(waveforms))

    
    # event channels
    def get_event_channel_info(self, zero_based_channel_index:int=None, channel_name:str=None, source_name:str=None, one_based_channel_index:int=None):
        """
        Returns info for event channel

        Usage:
            event_channel_info = self.get_event_channel_info(zero_based_channel_index=0)

            -or-

            event_channel_info = self.get_event_channel_info(channel_name="EVT01")

            -or-

            event_channel_info = self.get_event_channel_info(source_name="KBD", one_based_channel_index=1)

        Args:
            zero_based_channel_index - zero-based channel index
            channel_name - name of channel (e.g., "EVT01")
            source_name - name of source (e.g., "EVT")
            one_based_channel_index - one-based channel index

            Note - the following combinations of arguments are allowed:
                1. zero_based_channel_index
                2. channel_name
                3. source_name + one_based_channel_index
        
        Returns:
            event_channel_info - Object containing information about event channel
        """
        zero_based_channel_index = self.__get_zero_based_channel_index(zero_based_channel_index=zero_based_channel_index, channel_name=channel_name, source_name=source_name, one_based_channel_index=one_based_channel_index)
        event_channel_info = PL2DigitalChannelInfo()
        result = self.__file_reader.pl2_get_digital_channel_info(self.__file_handle, zero_based_channel_index, event_channel_info)

        if result == 0:
            self.__print_error()
            return 0
        
        return event_channel_info
    
    
    def get_event_channel_data(self, zero_based_channel_index:int=None, channel_name:str=None, source_name:str=None, one_based_channel_index:int=None):
        """
        Returns data for an event channel

        Usage:
            event_channel_tuple = self.get_event_channel_data(zero_based_channel_index=0)

            -or-

            event_channel_tuple = self.get_event_channel_data(channel_name="EVT01")

            -or-

            event_channel_tuple = self.get_event_channel_data(source_name="EVT", one_based_channel_index=1)
        
        Args:
            zero_based_channel_index - zero-based channel index
            channel_name - name of channel (e.g., "SPK01")
            source_name - name of source (e.g., "SPK")
            one_based_channel_index - one-based channel index

            Note - the following combinations of arguments are allowed:
                1. zero_based_channel_index
                2. channel_name
                3. source_name + one_based_channel_index
            
        Returns:
            event_channel_tuple - NamedTuple containing the following fields:
                                    - num_events_returned
                                    - event_timestamps
                                    - event_values

        """
        zero_based_channel_index = self.__get_zero_based_channel_index(zero_based_channel_index=zero_based_channel_index, channel_name=channel_name, source_name=source_name, one_based_channel_index=one_based_channel_index)
        event_channel_info = self.get_event_channel_info(zero_based_channel_index=zero_based_channel_index)

        # retrieve event channel data
        num_events_returned = c_ulonglong()
        event_timestamps = (c_longlong * event_channel_info.m_NumberOfEvents)()
        event_values = (c_ushort * event_channel_info.m_NumberOfEvents)()

        result = self.__file_reader.pl2_get_digital_channel_data(self.__file_handle, zero_based_channel_index, num_events_returned, event_timestamps, event_values)
        if result == 0:
            self.__print_error()
            return 0
        
        return EventChannelTuple(num_events_returned.value, tuple(event_timestamps), tuple(event_values))
        


    def get_comments(self):
        """
        Returns comments in PL2 file

        Usage:
            comments_tuple = self.get_comments()
        
        Args:
            None
        
        Returns:
            comments_tuple - NamedTuple containing the following fields:
                                - timestamps - a tuple containing the timestamps at which comments were issued
                                - comments - a tuple containing comment strings
        """
        num_comments = c_ulonglong()
        total_number_of_comments_bytes = c_ulonglong()

        self.__file_reader.pl2_get_comments_info(self.__file_handle, num_comments, total_number_of_comments_bytes)

        if num_comments.value == 0:
            return CommentsTuple((0), (0))

        timestamps = (c_longlong * num_comments.value)()
        comment_lengths = (c_ulonglong * num_comments.value)()
        comments = (c_char * total_number_of_comments_bytes.value)()

        self.__file_reader.pl2_get_comments(self.__file_handle, timestamps, comment_lengths, comments)

        # convert timestamps from tick units to seconds
        timestamps = np.array(timestamps, dtype=np.float32) / self.__file_info.m_TimestampFrequency

        # extract comments
        offset = 0
        comments_list = []
        for n in range(num_comments.value):
            tmp_comment = comments[offset:offset + comment_lengths[n]]      # should the upper bound be offset + comment_lengths[n]?   or should it be offset + (comment_lengths[n] - 1)
            comments_list.append(tmp_comment.decode("ascii"))
            offset += comment_lengths[n]

        return CommentsTuple(tuple(timestamps), tuple(comments_list))


    def close(self):
        """
        Closes PL2 file referenced by self.__file_handle

        Usage:
            self.close()
        
        Args:
            None
        
        Returns:
            None
        """
        self.__file_reader.pl2_close_file(self.__file_handle)

	###############################################################################
    # print functions
    ###############################################################################    
    def print_file_info(self):
        """
        Prints PL2 file info

        Usage:
            self.print_file_info()
        
        Args:
            None
        
        Returns:
            None
        """
        print(f"FILE INFO")
        m_CreatorComment=self.__file_info.m_CreatorComment.decode("utf-8")
        m_CreatorDateTime=self.__file_info.m_CreatorDateTime
        m_CreatorDateTimeMilliseconds=self.__file_info.m_CreatorDateTimeMilliseconds
        m_CreatorSoftwareName=self.__file_info.m_CreatorSoftwareName.decode("utf-8")
        m_CreatorSoftwareVersion=self.__file_info.m_CreatorSoftwareVersion.decode("utf-8")
        m_DurationOfRecording=self.__file_info.m_DurationOfRecording
        m_MaximumTrodality=self.__file_info.m_MaximumTrodality
        m_MinimumTrodality=self.__file_info.m_MinimumTrodality
        m_NumberOFRecordedAnalogChannels=self.__file_info.m_NumberOFRecordedAnalogChannels
        m_NumberOfChannelHeaders=self.__file_info.m_NumberOfChannelHeaders
        m_NumberOfDigitalChannels=self.__file_info.m_NumberOfDigitalChannels
        m_NumberOfNonOmniPlexSources=self.__file_info.m_NumberOfNonOmniPlexSources
        m_NumberOfRecordedSpikeChannels=self.__file_info.m_NumberOfRecordedSpikeChannels
        m_ReprocessorComment=self.__file_info.m_ReprocessorComment.decode("utf-8")
        m_ReprocessorDateTime=self.__file_info.m_ReprocessorDateTime
        m_ReprocessorDateTimeMilliseconds=self.__file_info.m_ReprocessorDateTimeMilliseconds
        m_ReprocessorSoftwareName=self.__file_info.m_ReprocessorSoftwareName.decode("utf-8")
        m_ReprocessorSoftwareVersion=self.__file_info.m_ReprocessorSoftwareVersion.decode("utf-8")
        m_StartRecordingTime=self.__file_info.m_StartRecordingTime
        m_TimestampFrequency=self.__file_info.m_TimestampFrequency
        m_TotalNumberOfAnalogChannels=self.__file_info.m_TotalNumberOfAnalogChannels
        m_TotalNumberOfSpikeChannels=self.__file_info.m_TotalNumberOfSpikeChannels
        m_Unused=self.__file_info.m_Unused

        # build creator date string
        creator_datetime_string = PL2EnhancedReader.__convert_tm_object_to_date_string(m_CreatorDateTime)
        reprocessor_datetime_string = PL2EnhancedReader.__convert_tm_object_to_date_string(m_ReprocessorDateTime)        

        print(f"{m_CreatorComment=}")
        print(f"m_CreatorDateTime={creator_datetime_string}")
        print(f"{m_CreatorDateTimeMilliseconds=}")
        print(f"{m_CreatorSoftwareName=}")
        print(f"{m_CreatorSoftwareVersion=}")
        print(f"{m_DurationOfRecording=}")
        print(f"{m_MaximumTrodality=}")
        print(f"{m_MinimumTrodality=}")
        print(f"{m_NumberOFRecordedAnalogChannels=}")
        print(f"{m_NumberOfChannelHeaders=}")
        print(f"{m_NumberOfDigitalChannels=}")
        print(f"{m_NumberOfNonOmniPlexSources=}")
        print(f"{m_NumberOfRecordedSpikeChannels=}")
        print(f"{m_ReprocessorComment=}")
        print(f"m_ReprocessorDateTime={reprocessor_datetime_string}")
        print(f"{m_ReprocessorDateTimeMilliseconds=}")
        print(f"{m_ReprocessorSoftwareName=}")
        print(f"{m_ReprocessorSoftwareVersion=}")
        print(f"{m_StartRecordingTime=}")
        print(f"{m_TimestampFrequency=}")
        print(f"{m_TotalNumberOfAnalogChannels=}")
        print(f"{m_TotalNumberOfSpikeChannels=}")
        print(f"{m_Unused=}")
    
    def print_analog_channel_info(self, zero_based_channel_index:int=None, channel_name:str=None, source_name:str=None, one_based_channel_index:int=None):
        """
        Prints info for analog channel

        Usage:
            self.print_analog_channel_info(zero_based_channel_index=0)

            -or-

            self.print_analog_channel_info(channel_name="WB01")

            -or-

            self.print_analog_channel_info(source_name="WB", one_based_channel_index=1)
        
        Args:
            zero_based_channel_index - zero-based channel index
            channel_name - name of channel (e.g., "WB01", "SPKC03")
            source_name - name of source (e.g., "WB", "SPKC", "FP", "SPK")
            one_based_channel_index - one-based channel index

            Note - the following combinations of arguments are allowed:
                1. zero_based_channel_index
                2. channel_name
                3. source_name + one_based_channel_index
            
            Returns:
                None
        """
        analog_channel_info = self.get_analog_channel_info(zero_based_channel_index=zero_based_channel_index, channel_name=channel_name, source_name=source_name, one_based_channel_index=one_based_channel_index)

        m_Channel=analog_channel_info.m_Channel
        m_ChannelEnabled=analog_channel_info.m_ChannelEnabled
        m_ChannelRecordingEnabled=analog_channel_info.m_ChannelRecordingEnabled
        m_CoeffToConvertToUnits=analog_channel_info.m_CoeffToConvertToUnits
        m_MaximumNumberOfFragments=analog_channel_info.m_MaximumNumberOfFragments
        m_Name=analog_channel_info.m_Name.decode("utf-8")
        m_NumberOfValues=analog_channel_info.m_NumberOfValues
        m_OneBasedChannelInTrode=analog_channel_info.m_OneBasedChannelInTrode
        m_OneBasedTrode=analog_channel_info.m_OneBasedTrode
        m_SamplesPerSecond=analog_channel_info.m_SamplesPerSecond
        m_Source=analog_channel_info.m_Source
        m_SourceTrodality=analog_channel_info.m_SourceTrodality
        m_Units=analog_channel_info.m_Units.decode("utf-8")

        print(f"{m_Name} INFO")
        print(f"m_Channel={m_Channel}")
        print(f"m_ChannelEnabled={m_ChannelEnabled}")
        print(f"m_ChannelRecordingEnabled={m_ChannelRecordingEnabled}")
        print(f"m_CoeffToConvertToUnits={m_CoeffToConvertToUnits}")
        print(f"m_MaximumNumberOfFragments={m_MaximumNumberOfFragments}")
        print(f"m_Name={m_Name}")
        print(f"m_NumberOfValues={m_NumberOfValues}")
        print(f"m_OneBasedChannelInTrode={m_OneBasedChannelInTrode}")
        print(f"m_OneBasedTrode={m_OneBasedTrode}")
        print(f"m_SamplesPerSecond={m_SamplesPerSecond}")
        print(f"m_Source={m_Source}")
        print(f"m_SourceTrodality={m_SourceTrodality}")
        print(f"m_Units={m_Units}")

    def print_spike_channel_info(self, zero_based_channel_index:int=None, channel_name:str=None, source_name:str=None, one_based_channel_index:int=None):
        """
        Prints info for spike channel

        Usage:
            self.print_analog_channel_info(zero_based_channel_index=0)

            -or-

            self.print_analog_channel_info(channel_name="SPK01")

            -or-

            self.print_analog_channel_info(source_name="SPK", one_based_channel_index=1)
        
        Args:
            zero_based_channel_index - zero-based channel index
            channel_name - name of channel (e.g., "SPK01")
            source_name - name of source (e.g., "SPK")
            one_based_channel_index - one-based channel index

            Note - the following combinations of arguments are allowed:
                1. zero_based_channel_index
                2. channel_name
                3. source_name + one_based_channel_index
            
            Returns:
                None
        """
        spike_channel_info = self.get_spike_channel_info(zero_based_channel_index=zero_based_channel_index, channel_name=channel_name, source_name=source_name, one_based_channel_index=one_based_channel_index)

        m_Channel=spike_channel_info.m_Channel
        m_ChannelEnabled=spike_channel_info.m_ChannelEnabled
        m_ChannelRecordingEnabled=spike_channel_info.m_ChannelRecordingEnabled
        m_CoeffToConvertToUnits=spike_channel_info.m_CoeffToConvertToUnits
        m_Name=spike_channel_info.m_Name.decode("utf-8")
        m_NumberOfSpikes=spike_channel_info.m_NumberOfSpikes
        m_NumberOfUnits=spike_channel_info.m_NumberOfUnits
        m_OneBasedChannelInTrode=spike_channel_info.m_OneBasedChannelInTrode
        m_OneBasedTrode=spike_channel_info.m_OneBasedTrode
        m_PreThresholdSamples=spike_channel_info.m_PreThresholdSamples
        m_SamplesPerSecond=spike_channel_info.m_SamplesPerSecond
        m_SamplesPerSpike=spike_channel_info.m_SamplesPerSpike
        m_SortEnabled=spike_channel_info.m_SortEnabled
        m_SortMethod=spike_channel_info.m_SortMethod
        m_SortRangeEnd=spike_channel_info.m_SortRangeEnd
        m_SortRangeStart=spike_channel_info.m_SortRangeStart
        m_Source=spike_channel_info.m_Source
        m_SourceTrodality=spike_channel_info.m_SourceTrodality
        m_Threshold=spike_channel_info.m_Threshold
        m_UnitCounts=tuple([x for x in spike_channel_info.m_UnitCounts if x > 0])
        m_Units=spike_channel_info.m_Units.decode("utf-8")

        print(f"{m_Name} INFO")
        print(f"m_Channel={m_Channel}")
        print(f"m_ChannelEnabled={m_ChannelEnabled}")
        print(f"m_ChannelRecordingEnabled={m_ChannelRecordingEnabled}")
        print(f"m_CoeffToConvertToUnits={m_CoeffToConvertToUnits}")
        print(f"m_Name={m_Name}")
        print(f"m_NumberOfSpikes={m_NumberOfSpikes}")
        print(f"m_NumberOfUnits={m_NumberOfUnits}")
        print(f"m_OneBasedChannelInTrode={m_OneBasedChannelInTrode}")
        print(f"m_OneBasedTrode={m_OneBasedTrode}")
        print(f"m_PreThresholdSamples={m_PreThresholdSamples}")
        print(f"m_SamplesPerSecond={m_SamplesPerSecond}")
        print(f"m_SamplesPerSpike={m_SamplesPerSpike}")
        print(f"m_SortEnabled={m_SortEnabled}")
        print(f"m_SortMethod={m_SortMethod}")
        print(f"m_SortRangeEnd={m_SortRangeEnd}")
        print(f"m_SortRangeStart={m_SortRangeStart}")
        print(f"m_Source={m_Source}")
        print(f"m_SourceTrodality={m_SourceTrodality}")
        print(f"m_Threshold={m_Threshold}")
        print(f"m_UnitCounts={m_UnitCounts}")
        print(f"m_Units={m_Units}")


    ###############################################################################
    # private functions
    ###############################################################################
    def __open_file(self, filename):
        """
        Opens PL2 file

        Usage:
            file_handle = self.__open_file(filename)

        Args:
            filename - The name of the file to be opened

        Returns:
            file_handle - Handle to the opened file

        """
        file_handle = self.__file_reader.pl2_open_file(filename)
        if file_handle == 0:
            self.__print_error()
            return 0
        
        return file_handle


    def __analyze_sources_and_channels(self):
        """
        Generates maps between source names, source ids, zero- and one-based channel indexes

        Usage:
            source_names, MAP_source_names_to_ids, MAP_source_names_to_channels, MAP_channel_names_to_zero_based_channel_indexes, MAP_source_name_and_one_based_channel_index_to_zero_based_channel_index = self.__analyze_sources_and_channels()
        
        Args:
            None
        
        Returns:
            source_names - list of source names present in the PL2 file
            MAP_source_names_to_ids - mapping from source names present in the PL2 file to source ids 
            MAP_source_names_to_channels - mapping from source names present in the PL2 file to lists of channel names
            MAP_channel_names_to_zero_based_channel_indexes - mapping from channel names to zero-based channel indexes
            MAP_source_name_and_one_based_channel_index_to_zero_based_channel_index - mapping from source names + one-based channel indexes to zero-based channel indexes
        """
        channel_info = []

        # pull info for all analog channels
        for zero_based_channel_index in range(self.__file_info.m_TotalNumberOfAnalogChannels):
            analog_channel_info = self.get_analog_channel_info(zero_based_channel_index=zero_based_channel_index)
            
            channel_name = analog_channel_info.m_Name.decode("utf-8")
            source_name = re.search("[A-z]+", channel_name).group(0)
            one_based_channel_index = int(re.search("[0-9]+", channel_name).group(0))
            source_id = analog_channel_info.m_Source
            
            if analog_channel_info.m_ChannelEnabled==1 and analog_channel_info.m_ChannelRecordingEnabled==1:
                channel_info.append((channel_name, source_name, source_id, zero_based_channel_index, one_based_channel_index))
        
        # pull info for all spike channels
        for zero_based_channel_index in range(self.__file_info.m_TotalNumberOfSpikeChannels):
            spike_channel_info = self.get_spike_channel_info(zero_based_channel_index=zero_based_channel_index)

            channel_name = spike_channel_info.m_Name.decode("utf-8")
            source_name = re.search("[A-z]+", channel_name).group(0)
            one_based_channel_index = int(re.search("[0-9]+", channel_name).group(0))
            source_id = spike_channel_info.m_Source

            if spike_channel_info.m_ChannelEnabled==1 and spike_channel_info.m_ChannelRecordingEnabled==1:
                channel_info.append((channel_name, source_name, source_id, zero_based_channel_index, one_based_channel_index))
        
        # pull info for all event (digital) channels
        for zero_based_channel_index in range(self.__file_info.m_NumberOfDigitalChannels):
            event_channel_info = self.get_event_channel_info(zero_based_channel_index=zero_based_channel_index)

            channel_name = event_channel_info.m_Name.decode("utf-8")
            source_name = re.search("[A-z]+", channel_name).group(0)
            try:
                one_based_channel_index = int(re.search("[0-9]+", channel_name).group(0))
            except AttributeError:
                one_based_channel_index = None        # some event channels may have non-standard names that fail the above regex lookup (e.g., "Strobed")
            source_id = event_channel_info.m_Source

            if event_channel_info.m_ChannelEnabled==1 and event_channel_info.m_ChannelRecordingEnabled==1:
                channel_info.append((channel_name, source_name, source_id, zero_based_channel_index, one_based_channel_index))
        
        # identify unique sources present
        source_names = set([source_name for channel_name, source_name, source_id, zero_based_channel_index, one_based_channel_index in channel_info])

        # map source names to ids
        MAP_source_names_to_ids = dict(set([(source_name, source_id) for channel_name, source_name, source_id, zero_based_channel_index, one_based_channel_index in channel_info]))

        # map source name to channel names
        MAP_source_names_to_channels = dict()
        for source_name in source_names:
            if source_name not in MAP_source_names_to_channels:
                MAP_source_names_to_channels[source_name] = []
            
            for channel_name, source_name_, source_id, zero_based_channel_index, one_based_channel_index in channel_info:
                if source_name == source_name_:
                    MAP_source_names_to_channels[source_name].append(channel_name)
        
        # map channel name to zero-based channel index
        MAP_channel_names_to_zero_based_channel_indexes = dict([(channel_name, zero_based_channel_index) for channel_name, source_name, source_id, zero_based_channel_index, one_based_channel_index in channel_info])

        # map source name + one-based channel index to zero-based channel index
        MAP_source_name_and_one_based_channel_index_to_zero_based_channel_index = dict([((source_name, one_based_channel_index), zero_based_channel_index) for channel_name, source_name, source_id, zero_based_channel_index, one_based_channel_index in channel_info])

        # return maps
        return source_names, MAP_source_names_to_ids, MAP_source_names_to_channels, MAP_channel_names_to_zero_based_channel_indexes, MAP_source_name_and_one_based_channel_index_to_zero_based_channel_index

    
    def __get_zero_based_channel_index(self, zero_based_channel_index:int=None, channel_name:str=None, source_name:str=None, one_based_channel_index:int=None):
        """
        Returns zero-based channel index

        Arguments:
            zero_based_channel_index - zero-based channel index
            channel_name - name of channel (e.g., "WB01", "SPKC03")
            source_name - name of source (e.g., "WB", "SPKC", "FP", "SPK")
            one_based_channel_index - one-based channel index

            Note: the following combinations of arguments are allowed:
                1. zero_based_channel_index
                2. channel_name
                3. source_name + one_based_channel_index
            
        Returns:
            zero_based_channel_index - zero-based channel index
        """

        if (zero_based_channel_index != None) and (channel_name==None) and (source_name==None and one_based_channel_index==None):
            return zero_based_channel_index
        
        elif (zero_based_channel_index==None) and (channel_name != None) and (source_name==None and one_based_channel_index==None):
            return self.__MAP_channel_names_to_zero_based_channel_indexes[channel_name]
        
        elif (zero_based_channel_index==None) and (channel_name==None) and (source_name != None and one_based_channel_index != None):
            return self.__MAP_source_name_and_one_based_channel_index_to_zero_based_channel_index[(source_name, one_based_channel_index)]
        
        else:
            error_message = "This function accepts zero_based_channel_index alone, channel_name alone, or source_name + one_based_channel_index alone. Any other combination of inputs is invalid."
            s = f" You passed:\n\t{zero_based_channel_index=}\n\t{channel_name=}\n\t{source_name=}\n\t{one_based_channel_index=}"
            error_message += s
            raise ArgumentError(error_message)

    
    def __print_error(self):
        error_message = (c_char * 256)()
        self.__file_reader.pl2_get_last_error(error_message, 256)
        print(error_message.value)

    @classmethod
    def __convert_tm_object_to_date_string(cls, tm_object):
        tm_sec = tm_object.tm_sec
        tm_min = tm_object.tm_min
        tm_hour = tm_object.tm_hour
        tm_mday = tm_object.tm_mday
        tm_mon = tm_object.tm_mon
        tm_year = tm_object.tm_year
        tm_wday = tm_object.tm_wday
        tm_yday = tm_object.tm_yday
        tm_isdst = tm_object.tm_isdst

        if tm_mday==0:
            return "N/A"

        weekday_name = "Sunday" if tm_wday==0 else "Monday" if tm_wday==1 else "Tuesday" if tm_wday==2 else "Wednesday" if tm_wday==3 else "Thursday" if tm_wday==4 else "Friday" if tm_wday==5 else "Saturday"
        month_name = "January" if tm_mon==0 else "February" if tm_mon==1 else "March" if tm_mon==2 else "April" if tm_mon==3 else "May" if tm_mon==4 else "June" if tm_mon==5 else "July" if tm_mon==6 else "August" if tm_mon==7 else "September" if tm_mon==8 else "October" if tm_mon==9 else "November" if tm_mon==10 else "December"
        day_suffix = "st" if tm_mday % 10 == 1 else "nd" if tm_mday % 10 == 2 else "rd" if tm_mday % 10 == 3 else "th"

        hour_string = ("0" if tm_hour < 10 else "") + str(tm_hour)
        minute_string = ("0" if tm_min < 10 else "") + str(tm_min)
        second_string = ("0" if tm_sec < 10 else "") + str(tm_sec)

        return f"{weekday_name}, {month_name} {tm_mday}{day_suffix}, {1900+tm_year} {hour_string}:{minute_string}:{second_string}"