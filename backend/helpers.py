import json
import os
import platform
import re
import soundfile as sf      # needs pip install
import sys
from pathlib import Path
from plumbum import local   # needs pip install
from typing import Optional, List, Dict, Tuple, Union
# Custom modules
from constants import (
    AUDIO_FORMATS,
    CHANNEL_NAMES,
    SMPTE_ORDER,
    CH_LAYOUT_COMP
)


# Class for analyzing dirs and getting info about the audio files included within
class SoundFilesUtils:
    """A utility class for managing and categorizing sound files.

    Parameters
    ----------
    user_path : Path
        The absolute path to a sound file or to the directory that contains sound files.

    Attributes
    ----------
    user_path : Path
        The user-specified path.
    file_list : List[str]
        A list of all the files in the user directory.
    sfile_list : List[str]
        A list of all the WAV files in the user directory.
    tuple_monomultisf : Tuple[List[str], List[str]]
        A tuple containing two lists: mono_files_list and multi_files_list.
            Both lists contain the names of the files (and not abs/rel paths).
            To get path, combime them with self.user_path.
    monodict : Dict[str, List[str]]
        Dictionary that maps audio file names to their file paths.
    dict_asf : Dict[str, Union[List[str], Dict[str, List[str]]]]
        Dictionary that maps audio file names to their file paths.
    sf_json : dict
        JSON-ready dictionary representation of the class instance.

    Examples
    --------
    >>> sound_files_utils = SoundFilesUtils(user_path="/path/to/sound/files")
    >>> sound_files_utils.file_list
    ["file1.wav", "file2.wav", "file3.wav"]
    >>> sound_files_utils.sfile_list
    ["file1.wav", "file2.wav"]
    >>> sound_files_utils.tuple_monomultisf
    (("file1.wav", "file2.wav"), ("file3.wav",))
    >>> sound_files_utils.monodict
    {"wav": ["file1.wav", "file2.wav"]}
    >>> sound_files_utils.dict_asf
    {"multi": ["file3.wav"], "mono": {"wav": ["file1.wav", "file2.wav"]}}
    """

    # INIT:

    def __init__(self, user_path: Path) -> None:
        """Initialize the SoundFilesUtils instance.

        Parameters
        ----------
        user_path : Path
            The absolute path to a sound file or directory containing sound files.
        """
        self._user_path = user_path  # Absolute path
        self._user_dir = self.user_dir
        self._file_list = self.file_list
        self._sfile_list = self.sfile_list
        self.tuple_monomultisf = self.gettuple_monomultisf()
        self.list_monosf = self.tuple_monomultisf[0]
        self.list_multisf = self.tuple_monomultisf[1]
        self.monodict = self.get_monodict(self.list_monosf)
        self.dict_asf = self.getdict_asf()
        self.sf_json = self.to_json()

    
    # PROPERTIES: 

    @property # Getter (a function that gets some attributes)
    def user_path(self) -> Path:
        """Path: Get the user path (dir or file)."""
        return self._user_path
    
    @user_path.setter # Setter
    def user_path(self, new_user_path: Path) -> None:
        """Set the path to the user directory.

        Parameters
        ----------
        new_user_path : Path
            The new path to the user directory.

        Raises
        ------
        ValueError
            If the new user directory does not exist.
        """
        if not os.path.exists(new_user_path):
            raise ValueError("The provided user directory does not exist.")
        
        self._user_path = os.path.abspath(new_user_path)

    @property
    def user_dir(self):
        """Path: Get directory from user_path (dir)."""
        # If Path is file, get file's absolute dir path
        if os.path.isfile(self.user_path):
            return os.path.abspath(os.path.dirname)
        else: 
            return self.user_path

    @property
    def file_list(self)  -> List[str]:
        """List[str]: Get the list of all files in the directory."""
        if os.path.isdir(self.user_path):
            return os.listdir(self.user_path)
        elif os.path.isfile(self.user_path):
            return [os.path.basename(self.user_path)]
        else:
            raise FileNotFoundError("Incorrect path. Please provide a valid path to a file or folder.")
            
    @property
    def sfile_list(self):
        """List[str]: Get the list of all supported AUDIO files in the directory."""
        
        # Check if dir is valid 
        if not os.path.isdir(self.user_path):  
            if not os.path.isfile(self.user_path):
                raise ValueError(f"'{self.user_path}' is not a valid path.")
        
        # Get audio files only, using the AUDIO_FORMATS constant
        sfiles = [
            file for file in self.file_list if file.lower().endswith(tuple(AUDIO_FORMATS))
        ]

        if len(sfiles) == 0:
            return []
        return sfiles


    # FUNCTIONS

    def gettuple_monomultisf(self) -> Tuple[List[str], List[str]]:
        """Categorize sound files as mono or multi-channel files.

        Returns
        -------
        tuple
            A tuple containing two lists: mono_files_list and multi_files_list.
            Both lists contain the names of the files (and not abs/rel paths).
            To get path, combime them with self.user_path.
        """

        # Create empty lists
        mono_files_list = []
        multi_files_list = []
        corrupted = []

        # Get File Path for each list element
        for file in self.sfile_list:

            # Handle both file and dir paths accordingly
            if os.path.isdir(self.user_path):
                sf_path = Path(self.user_path, file)
            else:
                sf_path = self.user_path

            # Separate mono and multi files
            try:
                info = sf.info(sf_path)
                if info.channels > 1:
                    multi_files_list.append(file)
                else:
                    mono_files_list.append(file)
            except Exception:
                corrupted.append(file)
                print(f"NOTE: File '{file}' is invalid and will not be processed.")

        # Remove corrupted file from sfile_list
        for file in corrupted:
                self.sfile_list.remove(file)

        return (mono_files_list, multi_files_list)


    def get_monodict(self, mono_files_list: List[str]) -> Dict[str, List[str]]:
        """Create a dictionary that maps audio file names to their file paths.

        Parameters
        ----------
        mono_files_list : List[str]
            List of mono audio file names.

        Returns
        -------
        Dict[str, List[str]]
            Dictionary that maps audio file names to their file paths.
        """        
        # Initiate empty dict/list. 
        monodict = {}   # will store final structure. 
        solonames = []  # will store list of names without channel extention (e.g 'example.wav')

        # For each file in list
        for file in mono_files_list:
            # Extract file's base name (= name excluding channel_names + extension)
            pattern = rf"(.+)([-._ ](?:{'|'.join(CHANNEL_NAMES)})\.({'|'.join(AUDIO_FORMATS)}))$"

            matches = re.search(pattern, file, flags=re.IGNORECASE)

            if matches:
                # Get the base name (group 1), channel name (group 2), and extension (group 3) from the match
                base_name, channel_name, extension = matches.groups()
                # print(base_name, channel_name, extension)

                new_name = f"{base_name}.{extension}"

                if extension not in monodict:
                    monodict[extension] = {}
                    monodict[extension][base_name] = [file]
                    solonames.append(new_name)
                else:
                    if new_name not in solonames:
                        solonames.append(new_name)
                        monodict[extension][base_name] = [file]
                    else:
                        monodict[extension][base_name].append(file)
        return monodict


    def getdict_asf(self) -> Dict[str, Union[List[str], Dict[str, List[str]]]]:
        """Get a dictionary of all the sound files.

        Returns
        -------
        Dict[str, Union[List[str], Dict[str, List[str]]]]
            A dictionary with the following keys:

            * `multi`: A list of all the multi-channel sound files.
            * `mono`: A dictionary of all the mono sound files, where the keys are the file extensions and the values are lists of file names.
        """
        return {"multi": self.list_multisf, "mono": self.monodict}

    def to_json(self):
        """Convert the SoundFilesUtils instance to a JSON-ready dictionary.

        Returns
        -------
        dict
            JSON-ready dictionary representation of the class instance.
        """
        data = {
            "user_path": str(self.user_path),
            "user_dir": str(self.user_dir),
            "file_list": self.file_list,
            "mono_sound_files": self.list_monosf,
            "multi_sound_files": self.list_multisf,
            "mono_dict": self.monodict,
            "sound_files_dict": self.dict_asf
        }
        return data

    def __str__(self):
        """Convert the SoundFilesUtils instance to a formatted JSON string.

        Returns
        -------
        str
            Formatted JSON representation of the class instance.
        """
        data = self.to_json()
        return json.dumps(data, indent=4)
    



# HELPER FUNCTIONS

# Gets this file's (or the executable's) directory's absolute path
def get_root_dir() -> Path:
    """Get the absolute path of this file's directory.

    Returns
    -------
    Path
        The absolute path of the root directory.

    Notes
    -----
    This function returns the absolute path of the directory containing the script or module where
    the function is called. This is typically the directory where the main Python script is located.
    When packaging with pyinstaller, we need to use sys.executable if we use the '--onefile' argument.
    If we use the '--onedir' arguments, we can use __file__ instead.
    """
    # rootDir = os.path.dirname(sys.executable)
    rootDir = os.path.dirname(__file__)
    return rootDir

# Get's path of pltform-specific bin executables
def get_bin_path(file: str = "ffmpeg") -> Path:
    """Get the path of platform-specific bin executables.

    Parameters
    ----------
    file : str, optional
        The name of the executable file (default is "ffmpeg").

    Returns
    -------
    str
        The path to the specified executable for the current platform.

    Raises
    ------
    OSError
        If the operating system is not recognized or the bin path does not exist.

    Notes
    -----
    This function constructs and returns the path to the platform-specific executable binary file,
    such as "ffmpeg", based on the current operating system. It determines the system and appends
    the appropriate directory structure to locate the binary file.
    """    
    # Get system
    system_name = platform.system()

    if system_name == 'Windows':
        bin_path = os.path.join("bin", "bin_win", f"{file}.exe")
    elif system_name == 'Darwin':
        bin_path = os.path.join("bin", "bin_mac", file)
    elif system_name == 'Linux':
        bin_path = os.path.join("bin", "bin_lin", file)
    else:
        raise OSError("Unknown operating system")

    # Join root with path
    path = os.path.join(get_root_dir(), bin_path)

    # Check if bin file exists in path
    if os.path.exists(path):
        return path
    else:
        print(f"Bin path doesn't exist. '{file}' program will try to run through local app.")
        raise OSError(f"Bin path does not exist in given dir. Cannot run {file} program.")
    

# Get audio file's info
def get_audio_info(file_path: str) -> Dict[str, Union[str, int]]:
    """Get audio file information using 'ffprobe' or 'soundfile'.

    Parameters
    ----------
    file_path : str
        The path to the audio file.

    Returns
    -------
    Dict[str, Union[str, int]]
        A dictionary containing audio information, including:
        - 'channels': Number of audio channels (int)
        - 'channel_layout': Channel layout description (str)
        - 'codec_name': Audio codec name (str)
        - 'bit_rate': Audio bit rate or subtype (str)
        - 'sample_rate': Audio sample rate (int)

    Raises
    ------
    ValueError
        If the file information cannot be read due to data inconsistencies or corruption.
    KeyError
        If the 'channels' key is not found in the audio information.
    OSError
        If analysis with 'ffprobe' fails.

    Notes
    -----
    This function attempts to retrieve audio information using 'ffprobe' command-line tool first. 
    If 'ffprobe' analysis fails, the function falls back to using 'soundfile' library. 
    The function returns a dictionary with audio information extracted from the chosen analysis method. 
    If the audio channel layout is not recognized, 
    the function attempts to infer it based on the number of channels. 
    If all attempts to gather information fail, 
    a ValueError is raised indicating possible file corruption.
    
    Example
    -------
    Get information about an audio file "sample.wav"
    
    >>> file_path = "path/to/sample.wav"
    >>> audio_info = get_audio_info(file_path)
    >>> print(audio_info)
    {
        'channels': 2,
        'channel_layout': 'stereo',
        'codec_name': 'pcm_s16le',
        'bit_rate': 's16',
        'sample_rate': 44100
    }
    """
    # Try analyzing with 'ffprobe'
    try:
        try:
            # Try bin's ffprobe
            ffprobe_path = get_bin_path(file="ffprobe")
            ffprobe_cmd = local[ffprobe_path]
        except Exception:
            # Try local ffprobe
            ffprobe_cmd = local['ffprobe']

        # ffprobe terminal command
        ffprobe_args = [
            "-v", "error",
            "-show_entries",
            "stream=channels,channel_layout,codec_name,bit_rate,sample_rate:format=filename",
            "-of", "default=noprint_wrappers=1",
            file_path,
        ]

        # Try to parse data gathered
        try:
            result = ffprobe_cmd[ffprobe_args]()
            lines = result.splitlines()

            audio_info = {}
            for line in lines:
                key, value = line.split("=", 1)
                audio_info[key] = value


            # HANDLE ERRORS:

            # If length of dictionary is incorrect
            if not len(audio_info) == 6:
                raise ValueError("Cannot read file info.")

            # If 'channels' key doesn't exist
            if not 'channels' in audio_info:
                raise KeyError("Cannot read file info. 'channels' key not found")

            # If audio_info['channels'] is not an int
            try:
                num_channels = int(audio_info['channels'])
            except ValueError:
                raise ValueError("Cannot read file info. 'channels' is not a valid integer value.")

            # If audio_info['channels'] is not between 1 and 8
            if not 0 < num_channels < 9:
                raise ValueError("Cannot read file info.")
        except Exception:
            raise OSError("Could not analyze with ffprobe.")
    
    # If ffprobe goes wrong, try analyzing with soundfile
    except Exception:

        try:
            print("File analysis done with soundFile")
            info = sf.info(file_path)
            audio_info = {
                'channels': int(info.channels),
                'channel_layout': 'unknown',
                'codec_name': info.format,
                'bit_rate': info.subtype,
                'sample_rate': int(info.samplerate)
            }
        # If this goes wrong too, raise ValueError
        except Exception:
            raise ValueError("Cannot read file info. File possibly corrupted.")
  
    # Assign values from parsed information 
    num_channels = int(audio_info['channels'])
    ch_layout = audio_info['channel_layout']
    
    # Figure out channel_layout value, if current value is not correct
    if any(ch_layout in layout for layout in CH_LAYOUT_COMP):
        pass
    else:
        if num_channels == 1:
            audio_info['channel_layout'] = 'mono'
        elif num_channels == 2:
            audio_info['channel_layout'] = 'stereo'
        elif num_channels == 6:
            audio_info['channel_layout'] = '5.1'
        elif num_channels == 7:
            audio_info['channel_layout'] = '7.0'
        elif num_channels == 8:
            audio_info['channel_layout'] = '7.1'
        else:
            raise ValueError("Invalid channel_layout")
        
    # Return if no errors found
    return audio_info


# Validate in/out paths
def validate_paths(input: str, out_dir: str = None, *, isdir: bool = False) -> Tuple[str, str, str]:
    """Validate input and output paths for files or directories.

    This function validates the provided input and output paths and ensures they are valid
    absolute paths. It can be used to validate both input files and directories, and optionally,
    output directories.

    Parameters
    ----------
    input : str
        The path to the input file or directory.
    out_dir : str, optional
        The path to the output directory (default is None).
    isdir : bool, optional
        If True, treats the input as a directory path; otherwise, treats it as a file path (default is False).

    Returns
    -------
    Tuple[str, str, str]
        A tuple containing the validated input path (dir or file), input directory, and output directory.

    Raises
    ------
    OSError
        If any of the paths is not a valid absolute path or if any of the validations fail.

    Notes
    -----
    This function validates the provided input and output paths by ensuring they are valid
    absolute paths and meeting the specified criteria. The input path can represent either a file
    or a directory. If the `out_dir` is not provided or is None, it defaults to using the input
    directory as the output directory. If `isdir` is set to True, the function treats the input as a directory path.
    """
    try:
        # Ensure you have absolute path
        input = os.path.abspath(input)

        if not isdir:
            in_dir = os.path.dirname(os.path.abspath(input))

            if not os.path.isfile(input):
                raise OSError(f"'{input}' is not a path to a file.")
        else:
            in_dir = input

            if not os.path.isdir(input):
                raise OSError(f"'{input}' is not a path to a directory.")

        if not out_dir is None and not os.path.isdir(out_dir):
            raise OSError(f"'{out_dir}' is not a valid path.")
        else:
            if out_dir is None:
                out_dir = in_dir
            else:
                out_dir = os.path.abspath(out_dir)
    except OSError as e:
        raise e

    return input, in_dir, out_dir


# Create out_folder
def create_outfldr(suffix: str, *, prefix: str = "out_", out_dir: str) -> str:
    """Create a new output folder with a specified prefix and suffix.

    Parameters
    ----------
    suffix : str
        The suffix to be added to the folder name.
    prefix : str, optional
        The prefix to be added to the folder name (default is "out_").
    out_dir : str
        The path to the directory where the new folder will be created.

    Returns
    -------
    str
        The absolute path to the newly created folder.

    Raises
    ------
    ValueError
        If the specified `out_dir` does not exist or is not a valid directory.

    Notes
    -----
    This function creates a new folder in the specified `out_dir` with the format
    "{prefix}{suffix}" or "{prefix}{suffix}_1", "{prefix}{suffix}_2", and so on
    if the folder already exists. The counter ensures that each folder name is unique.
    """
    # Check if the specified out_dir exists and is a directory
    if not os.path.exists(out_dir):
        raise ValueError(f"The provided out_dir '{out_dir}' does not exist.")
    if not os.path.isdir(out_dir):
        raise ValueError(f"The provided out_dir '{out_dir}' is not a valid directory.")

    # Construct the desired folder name
    folder_name = f"{prefix}{suffix}"
    folder_path = os.path.join(out_dir, folder_name)
    counter = 1

    # Add a counter to the folder name if it already exists
    while os.path.exists(folder_path):
        folder_name = f"{prefix}{suffix}_{counter}"
        folder_path = os.path.join(out_dir, folder_name)
        counter += 1

    # Create the folder
    os.mkdir(folder_path)

    # Return the absolute path to the newly created folder
    return os.path.abspath(folder_path)


# Key for sorted() function based on SMPTE_ORDER
def smpte_order_key(sfilename, *, smpte=SMPTE_ORDER):
    """NEEDS FIXING!!! Key function for sorting sound files based on SMPTE order.

    Parameters
    ----------
    sfilename : str
        The filename of the sound file.
    smpte : dict, optional
        The SMPTE order dictionary mapping order to channel extensions, by default SMPTE_ORDER.

        .. note:: This should not be changed, as it follows a specific convention.
        In the future other channel orderings could be added here such as 'film', 'protools'

    Returns
    -------
    int
        The order value of the sound file, or float('inf') if not found in SMPTE order.

    Notes
    -----
    This helper function is used in the core function `merge_nisfs()`.
    SMPTE_ORDER dict can be found in `constants.py`.

    """

    for order, ch_ext in smpte.items():
        if isinstance(ch_ext, list):
            for ext in ch_ext:
                pattern = rf"\b{ext}\.wav"
                if re.search(pattern, sfilename, flags=re.IGNORECASE):
                    return int(order)
        else:
            pattern = rf"\b{ch_ext}\.wav$"
            if re.search(pattern, sfilename):
                return int(order)
    return float('inf')