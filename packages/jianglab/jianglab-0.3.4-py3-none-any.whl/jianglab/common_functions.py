import os
from treelib import Tree, Node 
import numpy as np
import McsPy.McsCMOSMEA as McsCMOSMEA
from tqdm import tqdm
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import scipy.signal as signal
from tqdm import tqdm
import pickle


def frame_ref_to_onset(frame_ref, first_onset_index = 184, visualize_window = (250_000,350_000), stimulus_interval = 60, on_duration = 30, sampling_rate = 20000,overlay_split_num = 5):
    '''
        Convert frame_ref to onset_index
        input:
            frame_ref: 2d array, first row is the light, second row is the frame
            first_onset_index: the index of the first onset, it needs to be manually adjusted
            stimulus_interval: the interval between two stimulus in a unit of frame number
            sampling_rate: the sampling rate of the frame_ref
        output:
            It plots the frame_ref and the onset_index with index number
        return: 
            onset_index: the index of all onsets in a unit of sampling number according to sampling_rate
            off_set_index: the index of all offsets in a unit of sampling number according to sampling_rate
            peaks: the index of all frames in a unit of sampling number according to sampling_rate
            first_onset_index: the index of the first onset
        '''
    plt.rcParams['figure.figsize'] = [30, 5]
    def frame_ref_to_onset_plot(frame_ref = frame_ref, first_onset_index = first_onset_index, stimulus_interval = stimulus_interval, on_duration = on_duration, sampling_rate = sampling_rate, overlay_split_num = overlay_split_num, find_first_onset = True, visualize_window = visualize_window):
        
        prominence = 0.5 * max(frame_ref[1])
        distance = sampling_rate / (stimulus_interval + 10)
        peaks, _ = find_peaks(frame_ref[1], prominence=prominence,distance=distance)
        onset_index = peaks[first_onset_index:][::stimulus_interval] # the index of all onsets in a unit of sampling number according to sampling_rate
        offset_index = peaks[first_onset_index + on_duration:][::stimulus_interval]
        
        # lable the peaks with index number
        scale_factor = max(frame_ref[1])/max(frame_ref[0])
        overlay_factor = 0.03 * max(frame_ref[1]) # to avoid overlap of labels

        if find_first_onset:
            for i, peak in enumerate(peaks):
                if i > 2:
                    plt.text(peak, frame_ref[1][peak]+ i % overlay_split_num * overlay_factor, str(i), fontsize=6)
        
        plt.plot(frame_ref[1])
        plt.plot(frame_ref[0]*scale_factor)
        plt.plot(peaks, frame_ref[1][peaks], "x")
        
        if not find_first_onset:
            plt.plot(onset_index, frame_ref[0][onset_index]*scale_factor, "x")
            plt.plot(offset_index, frame_ref[0][offset_index]*scale_factor, "x")

            for i, onset in enumerate(onset_index):
                if i > 1:
                    plt.text(onset, frame_ref[0][onset]*scale_factor+ i % overlay_split_num * overlay_factor, str(i), fontsize=6)
        if visualize_window[1] != 0:
            plt.xlim(visualize_window)
        plt.show()
        return onset_index, offset_index, peaks, first_onset_index
    
    test_light_ref = frame_ref[:,0:visualize_window[1]]
    frame_ref_to_onset_plot(test_light_ref, first_onset_index=0) # find the first onset index by showing the plot indexed frames from 0
    frame_ref_to_onset_plot(test_light_ref, first_onset_index=first_onset_index, find_first_onset=False) # validate the position of the first onset index by showing the plot indexed frames from first_onset_index
    onset_index, offset_index, peaks, first_onset_index = frame_ref_to_onset_plot(frame_ref, first_onset_index=first_onset_index, find_first_onset=False, visualize_window= (0,0))
    plt.rcdefaults()
    return onset_index, offset_index, peaks, first_onset_index



def load_light_ref(filepath, sampling_rate=2000):
    ''' load light reference from .cmcr file
    filepath: path to the .cmcr or .cmtr file
    sampling_rate: sampling rate of the light reference
    '''
    raw_data = McsCMOSMEA.McsData(filepath)
    light_ref = raw_data.Acquisition.Analog_Data.ChannelData_1[:,::sampling_rate]
    return light_ref

def load_raw_data(filepath):
    ''' load raw data from .cmcr or .cmtr file
    filepath: path to the .cmcr or .cmtr file'''
    raw_data = McsCMOSMEA.McsData(filepath)
    return raw_data

def get_acquisition_rate(filepath):
    raw_data = McsCMOSMEA.McsData(filepath)
    return 1/(float(raw_data.Acquisition.Sensor_Data.SensorMeta["Tick"])*1e-6) # in Hz

def cmcr_to_nparray(filepath):
    data = McsCMOSMEA.McsData(filepath)
    data = np.array(data.Acquisition.Sensor_Data.SensorData_1_1)
    return data

def import_cmtr_firing_rate(filename, bin_size = 100): 
    """Import a .cmtr file and return a dictionary of units holding the timestamps and waveforms.
    :param filename: The path to the .cmtr file.
    :return: A dictionary of units holding the timestamps and waveforms.

    Note: 
    1. This function is used for GUI, where is named as import_cmtr_gui
    2. interval is set to 100ms, which is 10Hz
    3. Time scale of timestamps is in nanoseconds and bin_size is defined in milliseconds
    """
    all_units = {}
    processed = McsCMOSMEA.McsData(filename)

    def event_rate_in_interval(timestamps, length, interval):
        bins = np.arange(0, length, interval)
        hist, _ = np.histogram(timestamps, bins=bins)
        event_rate = hist / interval *1_000_000
        return event_rate

    for unit in tqdm(range(processed.Spike_Sorter.Units.shape[0])):
        data = eval("np.array(processed.Spike_Sorter.Unit_" + str(unit+1)+".get_peaks_timestamps())")
        data = event_rate_in_interval(data, length = processed.attributes["LB.RecordingDuration"], interval=bin_size * 1000) # 100ms interval, 10 hz
        col = eval("processed.Spike_Sorter.Unit_" + str(unit+1) + ".attributes['Column']")
        row = eval("processed.Spike_Sorter.Unit_" + str(unit+1) + ".attributes['Row']")
        waveform = eval("processed.Spike_Sorter.Unit_" + str(unit+1) + ".get_peaks_cutouts().T.mean(axis=1)")
        all_units[str(unit+1)] = {"unitID": unit+1, "data": data, "col": col, "row": row, \
            "waveform": waveform, "filename": filename, "globalID": -1}
    return all_units


def import_cmtr_raw(filename):
    """Import a .cmtr file and return a list of units holding the timestamps and waveforms.
    :param filename: The path to the .cmtr file.
    :return: A list of units holding the timestamps and waveforms.
    """
    all_units = {"units_data":[], "meta_data":[]}
    processed = McsCMOSMEA.McsData(filename)
    for unit in tqdm(range(processed.Spike_Sorter.Units.shape[0])):
        data = eval("np.array(processed.Spike_Sorter.Unit_" + str(unit+1)+".get_peaks_timestamps())")
        col = eval("processed.Spike_Sorter.Unit_" + str(unit+1) + ".attributes['Column']")
        row = eval("processed.Spike_Sorter.Unit_" + str(unit+1) + ".attributes['Row']")
        waveform = eval("processed.Spike_Sorter.Unit_" + str(unit+1) + ".get_peaks_cutouts().T.mean(axis=1)")
        all_units["units_data"].append({"unitID": unit+1, "data": data, "col": col, "row": row, \
            "waveform": waveform, "filename": filename, "globalID": -1})
    all_units["meta_data"].append({"analog":None})
    return all_units


def get_file_list(directory, file_extension=".pkl"):
    """
    Get the list of files with a specific extension in a directory and its subdirectories.
    :param directory: The directory to search for files.
    :param file_extension: The file extension to search for.
    :return: A list of file names with their absolute paths.
    """

    # Create an empty list to store the file names and their absolute paths
    file_list = []
    # Walk through the directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Get the absolute path of the file
            abs_path = os.path.abspath(os.path.join(root, file))
            
            # Add the file name and its absolute path to the list
            if file.endswith(file_extension):
                file_list.append( abs_path)

    return file_list

def dict_to_tree(data, parent_id=None, tree=None):
    """
    Convert a dictionary to a tree.
    :param data: The dictionary to convert.
    :param parent_id: The parent node id.
    :param tree: The tree object.
    :return: The tree object.

    # Convert the nested dictionary to a tree structure diagram
    tree = dict_to_tree(nested_dict)

    # Display the tree structure diagram
    tree.show()
    """

    if tree is None:
        tree = Tree()
        root_id = "root"
        tree.create_node(tag="Root", identifier=root_id)
        return dict_to_tree(data, parent_id=root_id, tree=tree)

    for key, value in data.items():
        node_id = f"{parent_id}.{key}" if parent_id else key
        tag = f"{key} ({type(value).__name__}"
        
        if isinstance(value, (list, tuple, np.ndarray)):
            tag += f", length: {len(value)}"
        elif isinstance(value, dict):
            tag += f", length: {len(value)}"
        elif isinstance(value, str):
            tag += f", length: {len(value)}"
            tag += f", value: {value}"
        elif isinstance(value, (int, float)):
            tag += f", value: {value}"
        
        tag += ")"
        
        tree.create_node(tag=tag, identifier=node_id, parent=parent_id)
        
        if isinstance(value, dict):
            dict_to_tree(value, parent_id=node_id, tree=tree)

    return tree

def import_gsheet(sheet_name = "MEA dashboard",
                cred = "./credentials/vibrant-epsilon-169702-467fddc26dfc.json"
                ):

    for i in range(3):# search parent folder
        if not os.path.exists(cred): 
            cred = "." + cred

    scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
    ]
    creds_obj = ServiceAccountCredentials.from_json_keyfile_name(cred, scope)
    client = gspread.authorize(creds_obj)
    sheet = client.open(sheet_name).sheet1.get_all_records()
    df = pd.DataFrame.from_dict(sheet)
    df.to_csv("../gsheet_table.csv", index = False)
    return df

def resample_med(np_array, kernel_size = 101, resample_rate =10): # med filter through first axis
    counter = 0
    out_array = np.zeros_like(np_array)
    for i in tqdm(range(np_array.shape[1])):
        for j in range(np_array.shape[2]):
            counter += 1
            # if counter % 100 == 0:
            #     print(counter, " out of 4225")
            out_array[:,i,j] = signal.medfilt(np_array[:,i,j], kernel_size=kernel_size)
    return out_array[::resample_rate]

def get_lowpass_data(raw_cmcr_data, 
                pre_resample_rate = 100,
                post_resample_rate = 10, 
                kernel_size = 51):
        # total resample 1000 result in 20 Hz acq rate
        # 30 mins processing time for 10 mins data
    np_array = raw_cmcr_data.Acquisition.Sensor_Data.SensorData_1_1
    images = np_array[::pre_resample_rate]
    images = resample_med(images, kernel_size= kernel_size, resample_rate = post_resample_rate) 
    return images


def remove_bad_lanes(data, bad_lanes): # for low pass filtered data
    if bad_lanes != []:
        data = np.delete(data, [int(lane)-1 for lane in bad_lanes], axis= 2)
    else:
        pass
    return data

def save_instance(filename, instance):
    with open(filename, "wb") as file_:
        pickle.dump(instance, file_, -1)

def load_instance(filename):
    return pickle.load(open(filename, "rb", -1))

def get_bad_lanes(cmcr_file_path):
    gsheet = import_gsheet()
    bad_lanes = cmcr_file_path.split("\\")[-1].replace("-",".").split(".")[:6]
    bad_lanes = ".".join(bad_lanes)
    bad_lanes = gsheet[gsheet.File_name.str.contains(bad_lanes)]["Bad_lanes"]
    if len(bad_lanes) != 0:                                 
        bad_lanes = [int(x) for x in list(bad_lanes)[0].split(",")]
    else:
        bad_lanes = []
        print("No bad lanes found")
    return bad_lanes

def clean_centers_all_process(arr, neighbour_size = (6,6,6)):
    def find_3d_local_min_general(arr, neighbor_size = (6,6,6)):
        if arr.shape[0] != 0:
            counter = 0
            neighbor_size = np.array(neighbor_size)
            pad =  (neighbor_size/2).astype(np.int32)
            arr_pad = np.pad(arr, ((pad[0],pad[0]), (pad[1],pad[1]), (pad[2],pad[2])), 'constant', constant_values = arr.max())
            arr_pad = arr_pad.astype(np.int32)
            center_list = []
            i_range, j_range, k_range = (arr_pad.shape[0]-pad[0]),(arr_pad.shape[1]-pad[1]),(arr_pad.shape[2]-pad[2])
            #surround_varience = []
            for i in tqdm(range(0, i_range,1), desc="Roughly find 3d local minimal"):
                for j in range(j_range):
                    for k in range(k_range):
                        m,n,p = neighbor_size
                        try:
                            if i >= pad[0] and j >= pad[1] and k >= pad[2]:
                                surround = arr_pad[i+pad[0]-m:i+pad[0]+m,j+pad[1]-n:j+pad[1]+n,k+pad[2]-p:k+pad[2]+p]
                                surround[m, n, p] = surround[m, n, p]+1
                                if np.all(arr_pad[i,j,k] <= surround):
                                    center_list.append([i-pad[0],j-pad[1],k-pad[2]])
                                    counter+=1
                                    # if counter % 100 ==0:
                                    #     print(i-pad[0],j-pad[1],k-pad[2])
                                    #     print(counter)
                                else:
                                    pass
                        except OSError as e:
                            print(e)
            return np.array(center_list)
        else:
            print("Empty input. Detection failed.")
            return np.array([0,0,0])
        
    def remove_close_centers(center_list):
            new_centers = []
            for center in tqdm(center_list, desc="Remove close centers "):
                center_check = True
                for new_center in new_centers[-1000:]:
                    try:
                        if np.abs(new_center[0]-center[0]) <50:
                            distance = np.linalg.norm(center - new_center)
                            if distance > np.sqrt(12) and distance != 0:
                                center_check = center_check and True
                            else:
                                center_check = False
                    except:
                        print("Fail to reduce center counts")
                    
                if center_check == True:
                    new_centers.append(center)
            return np.array(new_centers)

    def remove_centers_close_to_edges(center_list):
        clean_centers = []
        for center in center_list:
            if center.shape != ():
                if center[1] > 2 and center[1] <63 and center [2]>2 and center[2]<63:
                    clean_centers.append(center)
        return np.array(clean_centers)

    def remove_isolated_centers(center_list, lp_data):
            all_check = []
            clean_centers_2 = []
            data_mean, data_std = lp_data.mean(), lp_data.std()
            for center in tqdm(center_list, desc="Remove isolated events "):
                if center[0] > 12:
                    surround = lp_data[center[0]-2:center[0]+3,center[1]-1:center[1]+2, center[2]-1:center[2]+2].copy()
                    surround[:,1,1] = 0
                    presurround = lp_data[center[0]-12:center[0]-7,center[1]-1:center[1]+2, center[2]-1:center[2]+2].copy()
                    presurround[:,1,1] = 0
                    check_surround = (surround.sum()-presurround.sum())/40
                    all_check.append(check_surround)
                    if check_surround < data_mean - 2*data_std: #this is an arbitrary number
                        clean_centers_2.append(center)
            return np.array(clean_centers_2)

    center_list = find_3d_local_min_general(arr, neighbor_size = neighbour_size)
    center_list = remove_close_centers(center_list)
    center_list = remove_centers_close_to_edges(center_list)
    center_list = remove_isolated_centers(center_list, arr)
    return center_list

def clean_cmcr_data(cmcr_file_path,
                    kernel_size = 51,
                    pre_resample_rate = 100,
                    post_resample_rate = 10, neighbour_size = (6,6,6)):
    raw_cmcr_data = load_raw_data(cmcr_file_path)
    acq_rate = get_acquisition_rate(cmcr_file_path)
    pre_resample_rate = int(acq_rate/20_000 * pre_resample_rate)
    post_resample_rate = int(acq_rate/20_000 * post_resample_rate)
    kernel_size = int(acq_rate/20_000 * kernel_size)
    if kernel_size % 2 == 0:
        kernel_size += 1

    lowpass_data = get_lowpass_data(raw_cmcr_data, 
                                    pre_resample_rate=pre_resample_rate, 
                                    post_resample_rate=post_resample_rate, 
                                    kernel_size=kernel_size
                                    )
    bad_lanes = get_bad_lanes(cmcr_file_path)
    clean_data = remove_bad_lanes(lowpass_data, bad_lanes)
    clean_centers = clean_centers_all_process(clean_data, 
                                              neighbour_size = neighbour_size)

    return clean_centers, clean_data


    

def func3():
    pass
