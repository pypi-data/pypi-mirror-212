# -*- coding: utf-8 -*-
"""
DR Processing Script:
    
    Script for processing Dynamic Routing and Templeton ephys recordings
    
    Add full paths to base experiment session directories in 'mainPaths' list

Created on Fri Jan 13 15:22:03 2023

@author: ethan.mcbride
"""

import numpy as np
import pandas as pd
import pickle
import os
import glob

from .DR_processing_utils import load_behavior_data, load_rf_mapping, sync_data_streams
from .DR_processing_utils import align_trial_times, align_rf_trial_times
from .DR_processing_utils import align_spike_times, load_lick_times, define_RF_first

# only for sound pilot recordings
from .DR_processing_utils import load_sound_pilot_data, sync_data_streams_sound_pilot


EXP_MAP = {
    # sound pilot
    "625820": [
        r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\625820_06222022\2022-06-22_14-25-10",
    ],
    "625821": [
        r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\625821_07112022\2022-07-11_14-42-15",
        r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\625821_07122022\2022-07-12_13-51-39",
    ],
    # opto pilot
    "635891": [
        r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\opto pilot\2022-11-07_12-31-20_635891",
        r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\opto pilot\2022-11-08_11-03-58_635891",
    ],
    "636760": [
        r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\opto pilot\2022-11-14_13-18-05_636760",
        r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\opto pilot\2022-11-15_14-02-31_636760",
    ],
    # #templeton pilot
    "620263": [
        r"\\allen\programs\mindscope\workgroups\templeton\TTOC\pilot recordings\2022-07-26_14-09-36_620263",
        r"\\allen\programs\mindscope\workgroups\templeton\TTOC\pilot recordings\2022-07-27_13-57-17_620263",
    ],
    "620264": [
        r"\\allen\programs\mindscope\workgroups\templeton\TTOC\pilot recordings\2022-08-02_15-40-19_620264",
    ],
    "628801": [
        r"\\allen\programs\mindscope\workgroups\templeton\TTOC\pilot recordings\2022-09-19_13-48-26_628801"
    ],
    "636397": [
        r"\\allen\programs\mindscope\workgroups\templeton\TTOC\pilot recordings\2022-09-26_12-48-09_636397",
        r"\\allen\programs\mindscope\workgroups\templeton\TTOC\pilot recordings\2022-09-27_11-37-08_636397",
    ],
    "644547": [
        r"\\allen\programs\mindscope\workgroups\templeton\TTOC\pilot recordings\2022-12-05_13-08-02_644547",
        r"\\allen\programs\mindscope\workgroups\templeton\TTOC\pilot recordings\2022-12-06_12-35-35_644547",
    ],
    "646318": [
        r"\\allen\programs\mindscope\workgroups\templeton\TTOC\pilot recordings\2023-01-17_11-39-17_646318",
        r"\\allen\programs\mindscope\workgroups\templeton\TTOC\pilot recordings\2023-01-18_10-44-55_646318",
    ],
    "649944": [
        r"Y:\2023-02-27_08-14-30_649944",
        r"Y:\2023-02-28_09-33-43_649944",
    ],
    # DR pilot
    "626791": [
        r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_626791_20220815",
        r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_626791_20220816",
        r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_626791_20220817",
    ],
    "636766": [
        r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_636766_20230123",
        r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_636766_20230124",
        r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_636766_20230125",
        r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_636766_20230126",
    ],
    "644864": [
        r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_644864_20230130",
        r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_644864_20230131",
        r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_644864_20230201",
        r"\\allen\programs\mindscope\workgroups\np-exp\PilotEphys\Task 2 pilot\DRpilot_644864_20230202",
    ],
    "644866": [
        # error when re-running
        r"\\allen\programs\mindscope\workgroups\np-exp\PilotEphys\Task 2 pilot\DRpilot_644866_20230207",
        r"Y:\DRpilot_644866_20230208",
        r"Y:\DRpilot_644866_20230209",
        r"Y:\DRpilot_644866_20230210",
    ],
    "644867": [
        r"Y:\DRpilot_644867_20230220",
        r"Y:\DRpilot_644867_20230221",
        r"Y:\DRpilot_644867_20230222",
        r"Y:\DRpilot_644867_20230223",
    ],
    "649943": [
        r"Y:\DRpilot_649943_20230213",
        r"Y:\DRpilot_649943_20230214",
        r"Y:\DRpilot_649943_20230215",
        r"Y:\DRpilot_649943_20230216",
    ],
}


def get_exp_number(mouse_id: str, session_output_dir: str) -> int:
    """Polyfil for a future better piece of code to get this
    """
    try:
        session_output_dirs = EXP_MAP[mouse_id]
    except KeyError:
        raise Exception("Unsupported. mouse_id=%s" % mouse_id)

    try:
        # downstream expects 1-based
        return session_output_dirs.index(session_output_dir) + 1
    except ValueError:
        raise Exception("Unsupported. session_output_dir=%s" %
                        session_output_dir)


def infer_exp_meta(session_output_dir: str) -> tuple[str, str]:
    """Temp solution for a potentially better solution that doesnt rely
    on the structure of a filename

    Returns
    -------
    tuple
        mouse_id
        session_date: serialized as string in format YYYYMMDD
    """
    mouse_id = [x for x in session_output_dir.split(
        '_') if len(x) == 6 and x.isdigit()][0]
    rem_dashes = session_output_dir.replace('-', '')
    rem_dashes = rem_dashes.replace('\\', '_')
    session_date = [x for x in rem_dashes.split(
        '_') if len(x) == 8 and x.isdigit()]

    if len(session_date) > 0:
        session_date = session_date[0]

    return mouse_id, session_date


def process_ephys_sessions(
        mainPath: str,
        mouseID: str,
        session_date: str,
        metadata_only: bool,
        processedDataPath: str,
):
    exp_num = get_exp_number(mouseID, mainPath)
    # To do: function for automatically detecting whether RF was first or second
    RF_first = define_RF_first(mouseID)

    # set path to look for datajoint output
    datajointPath = r"\\allen\programs\mindscope\workgroups\dynamicrouting\datajoint\inbox\ks_paramset_idx_1"

    if ('625820' in mainPath) | ('625821' in mainPath):
        sound_pilot = True
    else:
        sound_pilot = False

    # Find paths to relevant files
    # assumes that behavior file is the only .hdf5!
    behavPath = glob.glob(os.path.join(mainPath, 'DynamicRouting*.hdf5'))[0]
    rfPath = glob.glob(os.path.join(mainPath, 'RFMapping*.hdf5'))
    ephysPath = glob.glob(os.path.join(
        mainPath, 'Record Node*', 'experiment*', 'recording*', 'continuous', '*-AP'))
    nidaqPath = glob.glob(os.path.join(
        mainPath, 'Record Node*', 'experiment*', 'recording*', 'continuous', 'NI-DAQmx*'))
    if len(ephysPath) == 0:
        ephysPath = glob.glob(os.path.join(mainPath, '*_'+mouseID+'*', 'Record Node*',
                              'experiment*', 'recording*', 'continuous', '*-AP'))  # [0]
        nidaqPath = glob.glob(os.path.join(mainPath, '*_'+mouseID+'*', 'Record Node*',
                              'experiment*', 'recording*', 'continuous', 'NI-DAQmx*'))

    kilosortPath = glob.glob(os.path.join(datajointPath, '*'+mouseID+'_' +
                             session_date, '*probe*_sorted', 'continuous', 'Neuropix-PXI-100.0'))
    if len(kilosortPath) > 0:
        if not os.path.isfile(os.path.join(kilosortPath[0], 'spike_clusters.npy')):
            kilosortPath = glob.glob(os.path.join(
                mainPath, 'Record Node*', 'experiment*', 'recording*', 'continuous', '*-AP'))
    else:
        kilosortPath = glob.glob(os.path.join(
            mainPath, 'Record Node*', 'experiment*', 'recording*', 'continuous', '*-AP'))
    # else:
    #     kilosortPath = glob.glob(os.path.join(datajointPath,'*'+mouseID+'_'+session_date,'*probe*_sorted','continuous','Neuropix-PXI-100.0'))

    # assumes that sync file is the only .h5!
    syncPath = glob.glob(os.path.join(mainPath, '*.h5'))[0]

    if os.path.isdir(processedDataPath) == False:
        os.mkdir(processedDataPath)

    metadata = {}
    metadata['mouseID'] = mouseID
    metadata['ephys_session_num'] = exp_num
    metadata['RF_first'] = RF_first
    metadata['behavPath'] = behavPath
    metadata['rfPath'] = rfPath
    metadata['ephysPath'] = ephysPath
    metadata['kilosortPath'] = kilosortPath
    metadata['datajointPath'] = datajointPath
    metadata['nidaqPath'] = nidaqPath
    metadata['syncPath'] = syncPath
    metadata['processedDataPath'] = processedDataPath
    metadata['session_date'] = session_date
    with open(os.path.join(processedDataPath, 'metadata.pkl'), 'wb') as handle:
        pickle.dump(metadata, handle, protocol=pickle.HIGHEST_PROTOCOL)
    if metadata_only == True:
        return

    if sound_pilot:
        trials_df, trialSoundArray, trialSoundDur, soundSampleRate, deltaWheelPos, startTime \
            = load_sound_pilot_data(behavPath)

        syncData, probeNames, probeDirNames = sync_data_streams_sound_pilot(
            syncPath, ephysPath, nidaqPath)

    else:
        trials_df, trialSoundArray, trialSoundDur, soundSampleRate, deltaWheelPos, startTime \
            = load_behavior_data(behavPath)

        syncData, probeNames, probeDirNames = sync_data_streams(
            syncPath, ephysPath, nidaqPath)

    trials_df, frames_df = align_trial_times(trials_df, syncData, syncPath, nidaqPath, trialSoundArray,
                                             trialSoundDur, soundSampleRate, deltaWheelPos, RF_first)

    unitData_df, spike_times, mean_waveforms = align_spike_times(ephysPath, syncData, probeNames, probeDirNames,
                                                                 kilosortPath, startTime, mouseID, exp_num)

    lick_times = load_lick_times(syncPath)

    # RF mapping
    if len(rfPath) > 0:
        rfPath = rfPath[0]
        rf_df, rf_trialSoundArray, rf_soundDur, rf_deltaWheelPos = load_rf_mapping(
            rfPath)
        rf_df, rf_frames_df = align_rf_trial_times(rf_df, syncData, syncPath, nidaqPath, rf_trialSoundArray,
                                                   rf_soundDur, soundSampleRate, rf_deltaWheelPos, RF_first)

        rf_df.to_csv(os.path.join(processedDataPath, 'rf_mapping_trials.csv'))
        rf_frames_df.to_csv(os.path.join(
            processedDataPath, 'rf_mapping_frames.csv'))

    # Save individual files for each type of data
    np.save(os.path.join(processedDataPath, 'spike_times_aligned.npy'),
            spike_times, allow_pickle=True)
    np.save(os.path.join(processedDataPath, 'mean_waveforms.npy'),
            mean_waveforms, allow_pickle=True)
    np.save(os.path.join(processedDataPath, 'lick_times.npy'),
            lick_times, allow_pickle=True)

    unitData_df.to_csv(os.path.join(processedDataPath, 'unit_table.csv'))
    trials_df.to_csv(os.path.join(processedDataPath, 'trials_table.csv'))
    frames_df.to_csv(os.path.join(processedDataPath, 'frames_table.csv'))


# %% run loop on experiment folders

# option to process and save metadata only
metadata_only = False

mainPaths = [
    # sound pilot
    # r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\625820_06222022\2022-06-22_14-25-10",
    # r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\625821_07112022\2022-07-11_14-42-15",
    # r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\625821_07122022\2022-07-12_13-51-39",

    # opto pilot
    # r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\opto pilot\2022-11-07_12-31-20_635891",
    # r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\opto pilot\2022-11-08_11-03-58_635891",
    # error w/ vsync/photodiode?
    r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\opto pilot\2022-11-14_13-18-05_636760",
    # error w/ vsync/photodiode?
    r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\opto pilot\2022-11-15_14-02-31_636760",

    # #templeton pilot
    # r"\\allen\programs\mindscope\workgroups\templeton\TTOC\pilot recordings\2022-07-26_14-09-36_620263",
    # r"\\allen\programs\mindscope\workgroups\templeton\TTOC\pilot recordings\2022-07-27_13-57-17_620263",
    # r"\\allen\programs\mindscope\workgroups\templeton\TTOC\pilot recordings\2022-08-02_15-40-19_620264",
    # r"\\allen\programs\mindscope\workgroups\templeton\TTOC\pilot recordings\2022-09-19_13-48-26_628801",
    # r"\\allen\programs\mindscope\workgroups\templeton\TTOC\pilot recordings\2022-09-26_12-48-09_636397",
    # r"\\allen\programs\mindscope\workgroups\templeton\TTOC\pilot recordings\2022-09-27_11-37-08_636397",
    # r"\\allen\programs\mindscope\workgroups\templeton\TTOC\pilot recordings\2022-12-05_13-08-02_644547",
    # r"\\allen\programs\mindscope\workgroups\templeton\TTOC\pilot recordings\2022-12-06_12-35-35_644547",
    # r"\\allen\programs\mindscope\workgroups\templeton\TTOC\pilot recordings\2023-01-17_11-39-17_646318",
    # r"\\allen\programs\mindscope\workgroups\templeton\TTOC\pilot recordings\2023-01-18_10-44-55_646318",
    # r"Y:\2023-02-27_08-14-30_649944",
    # r"Y:\2023-02-28_09-33-43_649944",

    # DR pilot
    # r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_626791_20220815", #re-run with new datajoint output
    # r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_626791_20220816", #re-run with new datajoint output
    # r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_626791_20220817", #re-run with new datajoint output

    # r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_636766_20230123",
    # r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_636766_20230124",
    # r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_636766_20230125",
    # r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_636766_20230126",

    # r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_644864_20230130",
    # r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_644864_20230131",
    r"\\allen\programs\mindscope\workgroups\dynamicrouting\PilotEphys\Task 2 pilot\DRpilot_644864_20230201",
    # r"\\allen\programs\mindscope\workgroups\np-exp\PilotEphys\Task 2 pilot\DRpilot_644864_20230202",

    # r"\\allen\programs\mindscope\workgroups\np-exp\PilotEphys\Task 2 pilot\DRpilot_644866_20230207", ##error when re-running
    # r"Y:\DRpilot_644866_20230208",
    # r"Y:\DRpilot_644866_20230209",
    # r"Y:\DRpilot_644866_20230210",

    # r"Y:\DRpilot_644867_20230220",
    # r"Y:\DRpilot_644867_20230221",
    # r"Y:\DRpilot_644867_20230222",
    # r"Y:\DRpilot_644867_20230223",

    # r"Y:\DRpilot_649943_20230213",
    # r"Y:\DRpilot_649943_20230214",
    # r"Y:\DRpilot_649943_20230215",
    # r"Y:\DRpilot_649943_20230216",

]

exp_nums = [
    # sound pilot
    # 1, #625820
    # 1,2, #625821

    # opto pilot
    # 1,2, #635891
    # 1, 2,  # 636760

    # #templeton pilot
    # 1,2, #620263
    # 1, #620264
    # 1, #628801
    # 1,2, #636397
    # 1,2, #644547
    # 1,2, #646318
    # 1,2, #649944

    # DR pilot
    # 1,2,3, #626791
    # 1,2,3,4, #636766
    1, 2, 3, 4,  # 644864
    # 1,2,3,4, #644866
    # 1,2,3,4, #644867
    # 1,2,3,4, #649943
]

# for im, mm in enumerate(mainPaths[:]):
#     mouseID = [x for x in mm.split('_') if len(x) == 6 and x.isdigit()][0]
#     rem_dashes = mm.replace('-', '')
#     rem_dashes = rem_dashes.replace('\\', '_')
#     session_date = [x for x in rem_dashes.split(
#         '_') if len(x) == 8 and x.isdigit()]
#     if len(session_date) > 0:
#         session_date = session_date[0]
#     process_ephys_sessions(
#         mm, mouseID, exp_nums[im], session_date, metadata_only)


def generate_trials(
    mainPath: str,
) -> pd.DataFrame:
    mouseID, session_date = infer_exp_meta(mainPath)
    exp_num = get_exp_number(mouseID, mainPath)
    # To do: function for automatically detecting whether RF was first or second
    RF_first = define_RF_first(mouseID)

    # set path to look for datajoint output
    datajointPath = r"\\allen\programs\mindscope\workgroups\dynamicrouting\datajoint\inbox\ks_paramset_idx_1"

    if ('625820' in mainPath) | ('625821' in mainPath):
        sound_pilot = True
    else:
        sound_pilot = False

    # Find paths to relevant files
    # assumes that behavior file is the only .hdf5!
    behavPath = glob.glob(os.path.join(mainPath, 'DynamicRouting*.hdf5'))[0]
    rfPath = glob.glob(os.path.join(mainPath, 'RFMapping*.hdf5'))
    ephysPath = glob.glob(os.path.join(
        mainPath, 'Record Node*', 'experiment*', 'recording*', 'continuous', '*-AP'))
    nidaqPath = glob.glob(os.path.join(
        mainPath, 'Record Node*', 'experiment*', 'recording*', 'continuous', 'NI-DAQmx*'))
    if len(ephysPath) == 0:
        ephysPath = glob.glob(os.path.join(mainPath, '*_'+mouseID+'*', 'Record Node*',
                              'experiment*', 'recording*', 'continuous', '*-AP'))  # [0]
        nidaqPath = glob.glob(os.path.join(mainPath, '*_'+mouseID+'*', 'Record Node*',
                              'experiment*', 'recording*', 'continuous', 'NI-DAQmx*'))

    kilosortPath = glob.glob(os.path.join(datajointPath, '*'+mouseID+'_' +
                             session_date, '*probe*_sorted', 'continuous', 'Neuropix-PXI-100.0'))
    if len(kilosortPath) > 0:
        if not os.path.isfile(os.path.join(kilosortPath[0], 'spike_clusters.npy')):
            kilosortPath = glob.glob(os.path.join(
                mainPath, 'Record Node*', 'experiment*', 'recording*', 'continuous', '*-AP'))
    else:
        kilosortPath = glob.glob(os.path.join(
            mainPath, 'Record Node*', 'experiment*', 'recording*', 'continuous', '*-AP'))
    # else:
    #     kilosortPath = glob.glob(os.path.join(datajointPath,'*'+mouseID+'_'+session_date,'*probe*_sorted','continuous','Neuropix-PXI-100.0'))

    # assumes that sync file is the only .h5!
    syncPath = glob.glob(os.path.join(mainPath, '*.h5'))[0]

    # if os.path.isdir(processedDataPath) == False:
    #     os.mkdir(processedDataPath)

    # metadata = {}
    # metadata['mouseID'] = mouseID
    # metadata['ephys_session_num'] = exp_num
    # metadata['RF_first'] = RF_first
    # metadata['behavPath'] = behavPath
    # metadata['rfPath'] = rfPath
    # metadata['ephysPath'] = ephysPath
    # metadata['kilosortPath'] = kilosortPath
    # metadata['datajointPath'] = datajointPath
    # metadata['nidaqPath'] = nidaqPath
    # metadata['syncPath'] = syncPath
    # metadata['processedDataPath'] = processedDataPath
    # metadata['session_date'] = session_date
    # with open(os.path.join(processedDataPath, 'metadata.pkl'), 'wb') as handle:
    #     pickle.dump(metadata, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # if metadata_only == True:
    #     return

    if sound_pilot:
        trials_df, trialSoundArray, trialSoundDur, soundSampleRate, deltaWheelPos, startTime \
            = load_sound_pilot_data(behavPath)

        syncData, probeNames, probeDirNames = sync_data_streams_sound_pilot(
            syncPath, ephysPath, nidaqPath)

    else:
        trials_df, trialSoundArray, trialSoundDur, soundSampleRate, deltaWheelPos, startTime \
            = load_behavior_data(behavPath)

        syncData, probeNames, probeDirNames = sync_data_streams(
            syncPath, ephysPath, nidaqPath)

    trials_df, frames_df = align_trial_times(trials_df, syncData, syncPath, nidaqPath, trialSoundArray,
                                             trialSoundDur, soundSampleRate, deltaWheelPos, RF_first)

    unitData_df, spike_times, mean_waveforms = align_spike_times(ephysPath, syncData, probeNames, probeDirNames,
                                                                 kilosortPath, startTime, mouseID, exp_num)

    lick_times = load_lick_times(syncPath)

    # RF mapping
    if len(rfPath) > 0:
        rfPath = rfPath[0]
        rf_df, rf_trialSoundArray, rf_soundDur, rf_deltaWheelPos = load_rf_mapping(
            rfPath)
        rf_df, rf_frames_df = align_rf_trial_times(rf_df, syncData, syncPath, nidaqPath, rf_trialSoundArray,
                                                   rf_soundDur, soundSampleRate, rf_deltaWheelPos, RF_first)

        # rf_df.to_csv(os.path.join(processedDataPath, 'rf_mapping_trials.csv'))
        # rf_frames_df.to_csv(os.path.join(
        #     processedDataPath, 'rf_mapping_frames.csv'))

    # Save individual files for each type of data
    # np.save(os.path.join(processedDataPath, 'spike_times_aligned.npy'),
    #         spike_times, allow_pickle=True)
    # np.save(os.path.join(processedDataPath, 'mean_waveforms.npy'),
    #         mean_waveforms, allow_pickle=True)
    # np.save(os.path.join(processedDataPath, 'lick_times.npy'),
    #         lick_times, allow_pickle=True)

    # unitData_df.to_csv(os.path.join(processedDataPath, 'unit_table.csv'))
    # trials_df.to_csv(os.path.join(processedDataPath, 'trials_table.csv'))
    # frames_df.to_csv(os.path.join(processedDataPath, 'frames_table.csv'))

    # adjust to vync time
    # trials_df[["trialStartFrame"]]
    adjusted_trials = trials_df.merge(
        frames_df,
        left_on="trialStartFrame",
        right_on="frame",
        how="inner,"
    )
    adjusted_trials["is_receptive_mapping"] = False
    # frames_map = frames_df[["vsync_times"]].iterrows().todict()

    # adjusted_trials_df = pd.DataFrame({})
    # adjusted_trials_df["trialStartFrame"] = trials_df["trialStartFrame"]
    # adjusted_trials_df["is_receptive_mapping"] = False
    # adjusted_trials_df["start_time"] = \
    #     adjusted_trials_df["trialStartFrame"].map(frames_map)
    # adjusted_trials_df["stop_time"] = 0

    # adjusted_trials_df["is_receptive_mapping"] = False

    return adjusted_trials