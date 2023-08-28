import os
import shutil
from plumbum import local
from constants import CH_LAYOUT_COMP, CH_SMPTE_COMP
from helpers import get_bin_path, smpte_order_key, SoundFilesUtils, get_audio_info, validate_paths
from pathlib import Path
from typing import Callable, Optional, List, Dict, Tuple, Union

# REPEAT OPERATION FUNCTION
def repeat_operation(in_dir: Path, 
                     out_dir: Optional[Path] = None, 
                     *, 
                     list_type: str = 'all', 
                     func: Callable[[Path, Path], None]
                     ):
    """Repeat an operation for each sound file in the input directory.

    This function performs a specified operation for each sound file in the provided input directory.
    The operation function is applied to each sound file in the directory, and the results are saved
    in the specified output directory. By default, the operation is applied to all sound files,
    but you can specify whether to operate on multi-channel ('multi') or mono-channel ('mono') files.

    Parameters
    ----------
    in_dir : Path
        The path to the input directory containing sound files.
    out_dir : Path, optional
        The path to the output directory where the results will be saved (default is None, which uses in_dir).
    list_type : str, optional
        The type of sound files to operate on ('all', 'multi', or 'mono') (default is 'all').
    func : Callable(inPath, outPath)
        The operation function to be applied to each sound file. It takes an input file path and an output directory path.

    Raises
    ------
    FileNotFoundError
        If no appropriate sound files are found in the input directory.
    """
    # Set out_dir to in_dir if not specified by the user
    if out_dir is None:
        out_dir = in_dir

    # Create SFU object to get in_dir's list of multitracks
    sfu = SoundFilesUtils(user_path=in_dir)

    # Choose appropriate file type based on list_type
    if list_type == 'multi':
        sfiles = sfu.list_multisf
    elif list_type == 'mono':
        sfiles = sfu.list_monosf
    else:
        sfiles = sfu.sfile_list

    # If no sfiles found, raise Error
    if len(sfiles) == 0:
        raise FileNotFoundError("No appropriate sound files found in dir.")

    # For each list element, try to split
    for input_file in sfiles:
        try:
            sf_path = os.path.join(sfu.user_dir, input_file) 
            func(sf_path, out_dir)
        except Exception as e:
            print(f"Error processing file '{input_file}': Corrupted file or extention not supported.")
            continue



# MONO TO MULTI FUNCTION
def mono_to_multi(inpt: Path, outpt: Optional[Path] = None):
    """Convert mono audio files (of the same name and different channel extensions) to multi-channel format.

    This function takes a directory containing mono audio files that are part of a multi-mono track 
    and converts them to multi-channel format using the specified channel layout. 
    The resulting multi-channel files are saved in the specified or default output directory.

    NOTE: `Multi-mono tracks` are essentially a group of mono tracks with the `same name but different channel extensions`,
    each representing a specific channel of the same track, and combined together they create one multi-track.

    Parameters
    ----------
    inpt : Path
        The path to the input directory containing mono audio files.
    outpt : Path, optional
        The path to the output directory where the converted files will be saved (default is None, which uses inpt).

    Raises
    ------
    ValueError
        If the channel layout of the mono audio file is not recognized or supported.
    FileNotFoundError
        If no multi-mono tracks are found in the input directory
        or if number of multi-mono tracks cannot lead to a supported mutlitrack format (stereo, 5.1, 7.0, 7.1).
    
    Example
    -------
    Assume we have multi-mono audio files in a path, all named "track.L.wav", "track.R.wav", etc..
    >>> input_file = Path("path/to/dir_that_includes_multimono_tracks")
    >>> out_dir = Path("path/to/output_dir")
    >>> mono_to_multi(input_file, out_dir)

    After running the function, the output directory will contain a converted
    multi-channel audio file:
    - "mono_track.wav"
    """

    # Validate paths
    try:
        input_file, in_dir, out_dir = validate_paths(inpt, outpt, isdir=True)
    except OSError as e:
        print("Error:", e)

    # Create SFU object
    sfu = SoundFilesUtils(user_path=in_dir)

    if len(sfu.list_monosf) == 0:
        raise FileNotFoundError("No multi-mono tracks found")

    for ext in sfu.monodict:
        num_channels = 0
        for sfilename in sfu.monodict[ext]:
            try:
                # Sort input files as per SMPTE Order
                input_files = sorted(sfu.monodict[ext][sfilename], key=smpte_order_key)

                # Check channel length
                num_channels = len(input_files)

                # Initialize channel_layout based on number of files in 'input_files' list
                if num_channels == 2:
                    channel_layout = 'stereo'
                elif num_channels == 6:
                    channel_layout = '5.1'
                elif num_channels == 7:
                    channel_layout = '7.0'
                elif num_channels == 8:
                    channel_layout = '7.1'
                else:
                    raise ValueError("Invalid channel_layout")

                # Create command-line argument strings for command
                ch_list1 = [f"[{i}:a]" for i in range(num_channels)]
                ch_list2 = [f"{i}.0" for i in range(num_channels)]

                # Create string from ch_list1
                inp_str = ''.join(ch_list1)

                # Create string from ch_list2
                map_list = []
                incr = 0
                for ch in CH_LAYOUT_COMP[channel_layout]:
                    map_list.append(f"{ch_list2[incr]}-{ch}")
                    incr += 1
                map_str = '|'.join(map_list)


                # Create output_path
                output_filename = f'{sfilename}.{ext}'
                output_path = os.path.join(out_dir, output_filename)


                # PLUMBUM COMMAND
                try:
                    ffmpeg_path = get_bin_path()
                    ffmpeg = local[ffmpeg_path]
                except Exception:
                    ffmpeg = local['ffmpeg']

                # Construct the command using plumbum syntax & list comprehension
                cmd = ffmpeg[sum([['-i', os.path.join(in_dir, infile)] for infile in input_files], [])]

                # Overwrite if file is present
                cmd = cmd['-y']

                # Filter complex
                cmd = cmd['-filter_complex',
                    f'{inp_str}\
                    join=inputs={num_channels}:\
                    channel_layout={channel_layout}:\
                    map={map_str}[a]']

                # Map [a] to output
                cmd = cmd['-map', '[a]']
                cmd = cmd[output_path]

                # Run the command
                cmd()

                # PRINT SUCCESS MESSAGE
                print(f"'{sfilename}' files were successfully merged.")

            except ValueError:
                print(f"NOTE: '{sfilename}' multi-mono track not processed. Incorrect number of channels ({num_channels}).")
                pass

# MULTI TO MULTI-MONO FUNCTION
def split_multi_sf(inpt: Path, outpt: Optional[Path] = None):
    """Split a multi-channel audio file into separate mono files.

    This function takes a multi-channel audio file and splits it into separate mono files,
    preserving each channel and adding it before the file's extension. The resulting files
    will be saved in the specified or default output directory inside a folder named as
    the input_file's base name.

    .. note:: This function currently works correctly with stereo, 5.1, 7.0, 7.1 files.
    .. note:: Accepted audio files: 'wav', 'flac', 'ogg', 'aiff', 'aifc', 'mp3', 'aac'.

    Parameters
    ----------
    inpt : Path
        The path to the multi-channel audio file to be split.
    outpt : Path, optional
        The directory path where the output files will be saved. If not specified,
        the output files will be saved in the same directory as the input file.

    Raises
    ------
    OSError
        If input_file or outpt is not a valid path.
    ValueError
        If input_file is not a valid file or is a mono track.

    Returns
    -------
    None

    Notes
    -----
    The function performs the following steps:
    
    1. Ensures that input_file and out_dir are both valid paths.
    2. Determines the base name and extension of the input_file.
    3. Creates a directory in out_dir for the output files.
    4. Reads the audio properties of the input_file using get_audio_info.
    5. Checks if the file is multitrack; if not, raises a ValueError.
    6. Constructs a Plumbum command to split the audio channels using ffmpeg.
    7. Iterates through each output channel and maps it to an output file.
    8. Executes the command to split the audio.
    9. Deletes created folder if operation fails.


    Example
    -------
    Assume we have an input file "multitrack_audio.wav"

    >>> input_file = Path("path/to/multitrack_audio.wav")
    >>> out_dir = Path("path/to/output")
    >>> split_multi_sf(input_file, out_dir)

    After running the function, the "output" directory will contain a subdirectory named
    "multitrack_audio" that includes separate mono files for each channel:
    - "multitrack_audio.L.wav" (left channel)
    - "multitrack_audio.R.wav" (right channel)
    - "multitrack_audio.X.wav" (where X = other channels)
    """

    # Ensure 'input_file' and 'out_dir' paths are valid:
    try:
        input_file, in_dir, out_dir = validate_paths(inpt, outpt)
    except OSError as e:
        print("Error:", e)

    # Get filename, base_name, and extension from 'input_file'
    sfilename = os.path.basename(input_file)
    base_name, ext = os.path.splitext(sfilename)

    # Create directory in out_dir
    os.makedirs(os.path.join(out_dir, base_name), exist_ok=True)
    
    # Path of the newly created output folder
    output_path = os.path.join(out_dir, base_name)

    try:

        # Read the multi-channel audio file and get audio properties
        try:
            sf_info = get_audio_info(input_file)
            num_channels = int(sf_info['channels'])
            channel_layout = sf_info['channel_layout']
        except Exception as e:
            raise OSError(f"File '{input_file}' could not be analyzed.", e)

        # If file is 'mono' abort
        if not num_channels > 1:
            raise ValueError(f"File '{input_file}' is not a multitrack.")
        
        # Construct the command using Plumbum
        try:
            ffmpeg_path = get_bin_path()
            ffmpeg = local[ffmpeg_path]
        except Exception:
            try:
                ffmpeg = local['ffmpeg']
            except Exception:
                raise OSError("ffmpeg could not be loaded.")

        # Set in file
        cmd = ffmpeg['-i', input_file]

        # Overwrite file if file is present
        cmd = cmd['-y']

        # Split operation
        cmd = cmd['-filter_complex', f'channelsplit=channel_layout=\
            {channel_layout}\
            {"".join([f"[{i}]" for i in range(num_channels)])}']

        # Loop over the output channels and map them to their respective output files
        for i in range(num_channels):
            ch_ext = CH_SMPTE_COMP[channel_layout][i]

            # Use output_path to create the full path to the output file   
            file_with_ext = f'{base_name}.{ch_ext}{ext}'
            output_file = os.path.join(output_path, file_with_ext)
            cmd = cmd['-map', f'[{i}]', output_file]

        # Run the command for the current input file
        cmd()

        # PRINT SUCCESS MESSAGE
        print(f"'{sfilename}' was successfully split.")

    except Exception as e:
        print(e)
        try:
            shutil.rmtree(output_path)
        except OSError as e:
            print(f"Error: {e}")

# CONFORM FUNCTION
def sf_to_mov(inpt: Path, outpt: Optional[Path] = None):
    """Convert multi-channel audio files to MOV format.

    This function takes a multi-channel audio file and converts it to MOV format while preserving
    the original channel layout. The resulting MOV file will be saved in the specified or default
    output directory.

    Parameters
    ----------
    inpt : Path
        The path to the multi-channel audio file to be converted.
    outpt : Optional[Path], optional
        The directory path where the converted MOV file will be saved. If not specified,
        the converted file will be saved in the same directory as the input file.

    Raises
    ------
    ValueError
        If the input file is already in MOV format or is not a multitrack audio file.
    OSError
        If input_file or outpt is not a valid path.

    Example
    -------
    Assume we have a multi-channel audio file "multichannel_track.wav"
    >>> input_file = Path("path/to/multichannel_track.wav")
    >>> out_dir = Path("path/to/output")
    >>> sf_to_mov(input_file, out_dir)

    After running the function, the output directory will contain a MOV file
    preserving the channel layout:
    - "multichannel_track.mov" (with channels preserved)
    """
    # Validate paths
    try:
        input_file, in_dir, out_dir = validate_paths(inpt, outpt)
    except OSError as e:
        print("Error:", e)


    # Get base_name and extension
    sfilename = os.path.basename(input_file)
    base_name, ext = os.path.splitext(sfilename)

    if ext == '.mov':
        raise ValueError("file is already .mov. Please convert to wav before proceeding")


    # Read the multi-channel audio file and get audio properties
    try:
        sf_info = get_audio_info(input_file)
        num_channels = int(sf_info['channels'])
        channel_layout = sf_info['channel_layout']
    except Exception as e:
        raise OSError(f"File '{input_file}' could not be analyzed.", e)

    # Configure channel layout
    if not num_channels > 1:
        raise ValueError(f"File '{input_file}' is not a multitrack")

    try:
        # Set the path to the ffmpeg executable
        try:
            ffmpeg_path = get_bin_path()
            ffmpeg = local[ffmpeg_path]
        except Exception:
            ffmpeg = local['ffmpeg']

        # Set in file
        cmd = ffmpeg['-i', input_file]

        # Overwrite file if file is present
        cmd = cmd['-y']

        # Split operation
        cmd = cmd['-filter_complex', f'[0:a]channelsplit=channel_layout=\
                {channel_layout}\
                {"".join([f"[{i}]" for i in range(num_channels)])}']

    # map channels
        for i in range(num_channels):
            cmd = cmd['-map', f'[{i}]']

        # Set outfiles' bitrate
        cmd = cmd['-c:a', 'pcm_s24le', '-ar', '48000', '-disposition:a', '+default']

        # Set name metadata for whole file name
        cmd = cmd['-metadata', f'title={base_name}']

        # Set name metadata for each audio stream
        for i in range(num_channels):
            ch_ext = CH_SMPTE_COMP[channel_layout][i]
            cmd = cmd[f'-metadata:s:a:{i}', f'title={base_name}.{ch_ext}']


        output_file = os.path.normpath(os.path.join(out_dir, f'{base_name}.mov'))
        # Set actual file name and type (.mov)
        cmd = cmd[output_file]

        # Run full command
        cmd()

        # PRINT SUCCESS MESSAGE
        print(f"'{sfilename}' was successfully processed.")

    except Exception as e:
        print(f"'{sfilename}' failed to convert to mov.")
        print(e)




# CONVERT FUNCTIONS

def convert_to_audio(inpt: Path, outpt: Optional[Path] = None, *, conversion: str = "wav", sample_rate: str = "48000", bit_rate: str = "pcm_s24le"):
    """NEEDS FIXING!!! Convert audio files to a specified format.

    This function takes an audio file and converts it to the specified audio format. The resulting
    audio file will be saved in the specified or default output directory.

    Parameters
    ----------
    inpt : Path
        The path to the input audio file to be converted.
    outpt : Optional[Path], optional
        The directory path where the converted audio file will be saved. If not specified,
        the converted file will be saved in the same directory as the input file.
    conversion : str, optional
        The target audio format to convert to (default is "wav").
    sample_rate : str, optional
        The sample rate of the output audio (default is "48000").
    bit_rate : str, optional
        The bit rate of the output audio (default is "pcm_s24le").
    """    
    # Validate paths
    try:
        input_file, in_dir, out_dir = validate_paths(inpt, outpt)
    except OSError as e:
        print("Error:", e)

    # Get filename, base_name, and extension from 'input_file'
    sfilename = os.path.basename(input_file)
    base_name, ext = os.path.splitext(sfilename)

    # Path of the newly created output folder
    output_file = f"{base_name}.{conversion}"
    output_path = os.path.join(out_dir, output_file)

    try:
        # Set the path to the ffmpeg executable
        try:
            ffmpeg_path = get_bin_path()
            ffmpeg = local[ffmpeg_path]
        except Exception:
            ffmpeg = local['ffmpeg']

        # Construct the command using Plumbum syntax
        cmd = ffmpeg['-i', input_file]

        cmd = cmd['-y']
        
        cmd = cmd["-ar", sample_rate]

        cmd = cmd['-c:a', bit_rate]  # Use -c:a to specify the audio codec
            
        cmd = cmd[output_path]

        # Run the command
        cmd()

        # PRINT SUCCESS MESSAGE
        print(f"'{sfilename}' converted to {output_file}.")

    except Exception as e:
        print(e)
        try:
            shutil.rmtree(output_path)
        except OSError as e:
            print(f"Error: {e}")




# QC VIDEO FUNCTIONS
def qc_video():
    ...