# Dimitris Giannoulis

**Project**: Audio Operations<br>
**Author**: Dimitris Giannoulis<br>
**Location**: London, UK<br>
**Date**: September 13, 2023<br>
<br>
<br>
<br>
<br>

# Audio Operations

Audio Operations is an Electron-based application that allows users to perform various audio processing operations on sound files. The application interfaces with a Python backend to execute the specified audio operations and provides a user-friendly interface for selecting input files, output paths, and operation types.

## Table of Contents
<br>

<b> AUDIO OPERATIONS (PROGRAM)</b>

- [Getting Started](#getting-started) 
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
    - [Starting the Application](#starting-the-application)
    - [Interface Overview](#interface-overview)
    - [Selecting Input Files and Paths](#selecting-input-files-and-paths)
    - [Choosing Operation Type](#choosing-operation-type)
    - [Submitting Operations](#submitting-operations)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)


<br>
<br>

<b> BACKENT IMPLEMENTATION (PYTHON)</b>

- [Backend Implementation (python)](#backend-implementation-python) 
- [project.py](#projectpy)
    - [run_operation](#run_operation)
- [core_functions.py](#core_functionspy)
    - [Imported Modules](#imported-modules)
    - [repeat_operation](#repeat_operation)
    - [mono_to_multi](#mono_to_multi)
    - [split_multi_sf](#split_multi_sf)
    - [sf_to_mov](#sf_to_mov)
    - [convert_to_audio](#convert_to_audio)
- [helpers.py](#helperspy)
    - [Imported Modules](#imported-modules-1)
    - [Class: `SoundFilesUtils`](#class-soundfilesutils)
    - [get_root_dir](#get_root_dir)
    - [get_bin_path](#get_bin_path)
    - [get_audio_info](#get_audio_info)
    - [validate_paths](#validate_paths)
    - [create_outfldr](#create_outfldr)
    - [smpte_order_key](#smpte_order_key)
- [constants.py](#constantspy)
    - [Channel Layouts](#channel-layouts)
    - [get_layout](#get_layout)
    - [Supported Audio Formats](#supported-audio-formats)
    - [SMPTE Extensions](#channel-extensions-and-smpte-order)

<br>
<br>
<br>

## Getting Started


### Prerequisites

Before you begin, ensure you have the following installed:

- [Node.js](https://nodejs.org/) (LTS version recommended)
- [Python](https://www.python.org/) (required for backend processing)

### Installation

#### Installing JavaScript Dependencies
The application uses JavaScript (Node.js) to handle frontend functionality. To install the required JavaScript libraries, follow these steps:

1. Open a terminal or command prompt.
2. Navigate to the root directory of the project where the package.json file is located.
3. Run the following command to install the JavaScript dependencies:
    ```sh
    npm install
    ```
    This will install the required JavaScript libraries listed in the package.json file, including the toastify-js library.


#### Installing Python Dependencies
The backend of the application is powered by Python. To install the necessary Python libraries, follow these steps:

1. Open a terminal or command prompt.
2. Navigate to the `/backend` directory of the project where the `requirements.txt` file is located.
3. Run the following command to install the Python dependencies:
    ```
    pip install -r requirements.txt
    ```
    This will install the required Python libraries listed in the requirements.txt file, including packages like Flask, soundfile, and others.

#### Running the Application
With all the required dependencies installed, you are ready to run the Audio Operations application:

1. Open a terminal or command prompt.
2. Navigate to the root directory of the project.
3. Run the following command to start the application:
    ```sh
    npm start
    ```
    This will launch the Electron application and open the main window of Audio Operations.

#### Troubleshooting
 - If you encounter any issues related to dependencies or running the application, make sure you have followed the installation steps correctly.
- If you encounter any Python-related issues, ensure that your Python version is 3.6 or higher, and that the correct Python executable is in your system's PATH.

#### Feedback and Support
For feedback, questions, or support related to the installation process or the application itself, please reach out to @jimmygian.




## Usage


### Starting the Application

To start the Audio Operations application, run the following command in your terminal:

```sh
npm start
```


### Interface Overview

The Audio Operations application provides a simple user interface for selecting audio files or folders, specifying output paths, and choosing the desired audio processing operation.

### Selecting Input Files and Paths

You can either drag and drop a single audio file or a single folder onto the designated area or click on the "Choose File" / "Choose Folder" buttons to select input files and folders. Selected path will be displayed on the interface.

- If you need to operate on just a single file, you can select or drop a single file.
- If you need to repeat the process in more than 1 files, you must include all the desired files in a folder, and then select that folder. 

NOTE: Optionally, you can select an output folder. If no folder is selected, the output path will be the same as the directory of your input file(s).

### Choosing Operation Type

- Use the dropdown menu to select the audio processing operation you want to perform (e.g., split, merge, conform, convert).
- The selected operation type will be displayed on the interface.

### Submitting Operations

- After selecting input files, output paths, and operation types, click the "Submit" button to initiate the audio processing operation.
- A modal window will display the progress of the operation.
- Once the operation is completed, you'll receive a success or failure message.




## Features

- User-friendly interface for audio processing operations.
- Integration with a Python backend for efficient audio processing.
- Drag and drop functionality for selecting input files.
<!-- - Flexible output path options.
- Real-time progress updates and messages during operations. -->



## Contributing

Contributions to Audio Operations are welcome! Here's how you can contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b feature-name`
3. Make your changes and commit them: `git commit -m "Add new feature"`
4. Push to your branch: `git push origin feature-name`
5. Open a pull request.

Please ensure your code follows the project's coding standards and includes appropriate documentation.



## License

This project is licensed under the MIT License.

<br>
<br>
<br>
<br>




# Backend Implementation (python) 

The backend of the `Audio Operations` tool is implemented in `Python` and consists of several important files and functions that enable the execution of audio processing operations. This section provides an overview of the key files and their functionalities within the backend.

<br>
<br>

## `project.py`

The `project.py` script serves as the main entry point of the audio processing tool. It allows users to specify input arguments such as the input path, output path, and operation type to execute various audio processing operations.

**Usage:**
```sh
python project.py [input_path] [output_path] [operation_type]
```

- `input_path` is the path to a file or folder containing audio files.
- `output_path` is the path where processed files will be stored.
- `operation_type` is the type of operation to be executed (e.g., "split", "merge", "conform", "convert").

The script utilizes the `FUNC_TYPE` dictionary to map operation types to their corresponding functions. The operations supported are:

1. `split`: Splitting multi-channel audio files
2. `merge`: Merging mono (multi-mono) files into multi-channel format
3. `conform`: Converting audio files to MOV format after splitting them, and then mapping each track to its respective channel (this is helpful for conform deliveries.)
4. `convert`: Converting audio files to different formats (still in Beta)

For detailed usage examples and command line execution, refer to the provided main() function in the project.py script.

<br>

### `run_operation`: 

This function handles the execution of audio processing operations.
`func` is the audio processing function to run.

**Parameters:**

- `func` (Callable): The audio processing function to run.
- `in_path` (Path): The path to the input audio file or directory of files.
- `out_path` (Path, optional): The path to the output directory where processed files will be saved.
- `out_name` (str, optional): The name to use for the output folder.
- `list_type` (str, optional): The type of list to pass to the operation function ('all', 'multi', 'mono').
- `repeat_func` (Callable, optional): The function to use for repeating the operation on multiple files.

**Returns:**

- `Path or None`: The path to the output directory if successful, None if operation failed.

**Notes:**

- This function creates an output folder for processed files.
- Depending on the operation and list_type, it repeats the operation on multiple files if needed.
- Errors during the operation lead to folder deletion and `None` return value.

<br>
<br>

## `core_functions.py`

The `core_functions.py` module contains essential audio processing functions used by the backend of the Audio Operations tool. These functions perform specific operations such as splitting multi-channel audio, converting mono to multi-channel, converting audio formats, and more.

<br>

### Imported Modules

```python
import os
import shutil
from plumbum import local   # needs pip install
from constants import CH_LAYOUT_COMP, CH_SMPTE_COMP
from helpers import get_bin_path, smpte_order_key, SoundFilesUtils, get_audio_info, validate_paths              # imported from custom module
from pathlib import Path
from typing import Callable, Optional, List, Dict, Tuple, Union
```
- `pathlib` and `typing` libraries are used for type hints.
- `plumbum` is the way python communicates with the terminal.
- `helpers` and `constants` are custom modules included in the same git.

<br>


### `repeat_operation`

The `repeat_operation` function is used to perform a specified audio processing operation for each sound file in the provided input directory. It iterates through the input directory and applies the operation function to each sound file, saving the results in the specified output directory.

**Parameters:**
- `in_dir` (Path): The path to the input directory containing sound files.
- `out_dir` (Path, optional): The path to the output directory where the results will be saved (default is None, which uses `in_dir`).
- `list_type` (str, optional): The type of sound files to operate on ('all', 'multi', or 'mono') (default is 'all').
- `func` (Callable[[Path, Path], None]): The operation function to be applied to each sound file.

**Raises:**
- `FileNotFoundError`: If no appropriate sound files are found in the input directory.

<br>

### `mono_to_multi`

The `mono_to_multi` function converts mono audio files representing different channels of a multi-mono track to a multi-channel format. The resulting multi-channel files are saved in the specified or default output directory.

**Parameters:**
- `inpt` (Path): The path to the input directory containing mono audio files.
- `outpt` (Path, optional): The path to the output directory where the converted files will be saved (default is None, which uses `inpt`).

**Raises:**

- `ValueError`: If the channel layout of the mono audio file is not recognized or supported.
- `FileNotFoundError`: If no multi-mono tracks are found in the input directory or if the number of multi-mono tracks cannot lead to a supported multitrack format (stereo, 5.1, 7.0, 7.1).

**Example**

Assume we have multi-mono audio files in a directory, all named 
- "track.L.wav", (mono file)
- "track.R.wav", (mono file)
- "track.C.wav", (mono file)
- etc...

```python
from pathlib import Path
from core_functions import mono_to_multi

# Set paths
input_file = Path("path/to/dir_that_includes_multimono_tracks")
out_dir = Path("path/to/output_dir")

# Call the function
mono_to_multi(input_file, out_dir)
```
After running the function, the output directory will contain 1 converted multi-channel audio file:

- "track.wav" (multi-track)

<br>

### `split_multi_sf`

The `split_multi_sf` function splits a multi-channel audio file into separate mono files, preserving each channel as a separate file. The resulting files are saved in the specified or default output directory inside a folder named after the input file's base name.

**Parameters:**
- `inpt` (Path): The path to the multi-channel audio file to be split.
- `outpt` (Path, optional): The directory path where the output files will be saved (default is None, which uses the input directory).

**Raises:**

- `OSError`: If `input_file` or `output` is not a valid path.
- `ValueError`: If `input_file` is not a valid file or is a mono track.


**Example**
Assume we have an input file named "multitrack_audio.wav".

```python
from pathlib import Path
from core_functions import split_multi_sf

# Set paths
input_file = Path("path/to/multitrack_audio.wav")
out_dir = Path("path/to/output")

# Call the function
split_multi_sf(input_file, out_dir)
```

After running the function, the "output" directory will contain a subdirectory named "multitrack_audio" that includes separate mono files for each channel:

- "multitrack_audio.L.wav" (left channel)
- "multitrack_audio.R.wav" (right channel)
- "multitrack_audio.X.wav" (where X = other channels)

<br>

### `sf_to_mov`

The `sf_to_mov` function converts multi-channel audio files to MOV format while preserving the original channel layout. The resulting MOV file is saved in the specified or default output directory.

The .mov file works as a container that contains all the separate channels of that multi-track. Each file begins at the same timecode and is sent to each respective channel. Moreover, the metadata namings of each file include their channel extension (similar to the `split_multi_sf` funciton)

**Parameters:**
- `inpt` (Path): The path to the multi-channel audio file to be converted.
- `outpt` (Path, optional): The directory path where the converted MOV file will be saved (default is None, which uses the input directory).

**Raises:**

- `ValueError`: If the input file is already in MOV format or is not a multitrack audio file.
- `OSError`: If `input_file` or `output` is not a valid path.



**Example**

Assume we have a multi-channel audio file named "multichannel_track.wav".

```python
from pathlib import Path
from core_functions import sf_to_mov

# Set paths
input_file = Path("path/to/multichannel_track.wav")
out_dir = Path("path/to/output")

# Call the function
sf_to_mov(input_file, out_dir)
```
After running the function, the output directory will contain a MOV file preserving the channel layout:

- "multichannel_track.mov" (with channels preserved)

<br>

### `convert_to_audio`

The `convert_to_audio` function converts audio files to a specified audio format. The resulting audio file is saved in the specified or default output directory.

**Parameters:**
- `inpt` (Path): The path to the input audio file to be converted.
- `outpt` (Path, optional): The directory path where the converted audio file will be saved (default is None, which uses the input directory).
- `conversion` (str, optional): The target audio format to convert to (default is "wav").
- `sample_rate` (str, optional): The sample rate of the output audio (default is "48000").
- `bit_rate` (str, optional): The bit rate of the output audio (default is "pcm_s24le").


<br>


### Integration with the Backend

These core functions are integral to the operation of the audio processing tool's backend. They are called within the `project.py` script to perform various audio processing operations based on user input.

Please refer to the source code of the `core_functions.py` module for more detailed implementation details and function behavior.

<br>
<br>



## `helpers.py`

The `helpers.py` module contains a collection of utility functions and a class that assist in various tasks related to managing and processing audio files and directories. These helper functions are designed to enhance the efficiency, effectiveness, and robustness of the project by providing streamlined interactions with external resources and encapsulating complex operations.

By encapsulating intricate operations and enabling seamless interaction with external resources, this module significantly contributes to the seamless execution and robustness of the `core_functions.py` and `project.py` scripts."

### Imported Modules

```python
import json
import os
import platform
import re
import soundfile as sf      # needs pip install
import sys
from pathlib import Path
from plumbum import local   # needs pip install
from typing import Optional, List, Dict, Tuple, Union
```
- `pathlib` and `typing` libraries are used for type hints.
- `soundfile` is a really important module that analyzes audio files and extract   metadata information. This module is used if `ffprobe` fails to load or to extract the necessary information the program needs.
- `platform` is used to get the system information (win, macOS, linux).
- `re` is used to provide complex naming operations and file identifications,
- `plumbum` is the way python communicates with the terminal.

<br>


### Class: `SoundFilesUtils`

#### Description

A utility class for managing and categorizing sound files. This class provides methods to analyze directories, categorize files as mono or multi-channel, create dictionaries of audio file information, and convert class instances to JSON-ready representations.

#### Attributes
- `user_path` (Path): The user-specified path to a sound file or directory.
- `file_list` (List[str]): A list of all the files in the user directory.
- `sfile_list` (List[str]): A list of all the supported audio files in the user directory.
- `tuple_monomultisf (Tuple[List[str], List[str]])`: A tuple containing two lists: mono_files_list and multi_files_list.
- `monodict (Dict[str, List[str]])`: A dictionary that maps audio file names to their file paths.
- `dict_asf (Dict[str, Union[List[str], Dict[str, List[str]]]])`: A dictionary that categorizes audio files as 'multi' or 'mono'.
- `sf_json (dict)`: JSON-ready dictionary representation of the class instance.


#### Methods

- `gettuple_monomultisf(self) -> Tuple[List[str], List[str]]`: Categorizes sound files as mono or multi-channel.
- `get_monodict(self, mono_files_list: List[str])` -> Dict[str, List[str]]: Creates a dictionary mapping audio file names to their file paths.
- `getdict_asf(self) -> Dict[str, Union[List[str], Dict[str, List[str]]]]`: Gets a dictionary of all the sound files.
- `to_json(self)`: Converts the SoundFilesUtils instance to a JSON-ready dictionary.

<br>

### `get_root_dir`

The purpose of this function is to get the absolute path that leads to the current file (`helpers.py`). This is needed because it will be used as a starting point for the creation of the path that will lead to where the `bin` files of ffmpeg and ffprobe are.

It's important to note that if files behave differently when python is packaged with `pyinstaller` or when it's not. This means that this function may need to be modified to lead to a valid path.

As a rule of thump for when packaging the python project:

1. Using the `--onefile` option:
    ```sh
    pyinstaller project.py --onefile
    ```

    If the python project was packaged using the "--onefile" method, this function will need to be modified as follows:

    ```python
    rootDir = os.path.dirname(sys.executable)
    ```
    The `sys.executable` returns the directory of the python interpreter, which, in this case, is bundled into the executable. 
    If we used `__file__` instead of `sys.executable`, the path would lead to a temp folder where the executable is being extracted.

2. Using the `--onedir` option:
    ```sh
    pyinstaller project.py --onedir
    ```
    This option bundles the python project and its dependencies into one folder but not into a single executable. In this case, we must use the following option:
    ```python
    rootDir = os.path.dirname(__file__)
    ```
    The `__file__` returns the path to this file, which in this case is indeed in the correct place.

This function plays a crusial role in locating the `bin` executables for the `ffmpeg` and `ffprobe` libraries. These files are located in `"__file__"/bin/bin_sys/` (where sys == win/lin/mac).

<br>

### `get_bin_path`

This function constructs and returns the path to the platform-specific executable binary file (e.g., "ffmpeg") based on the current operating system. It ensures that the appropriate binary file path is returned based on the system. 

**Parameters:**
- `file` (str, optional): The name of the executable file (default is "ffmpeg").

**Returns:**
- `Path`: The path to the specified executable for the current platform.

**Raises:**
- `OSError`: If the operating system is not recognized or the bin path does not exist.


**NOTE:** 
The Path is being constructed as follows:
```python
path = os.path.join(get_root_dir(), bin_path)
```
The bin folder is located where this file is located. This means that `get_root_dir()` must provide us with a correct starting path to this file, otherwise the path won't be valid. Please check `get_bin_path(file: str = "ffmpeg")` for more info.

<br>

### `get_audio_info`
This function retrieves detailed information about an audio file using either the 'ffprobe' command-line tool or the 'soundfile' library (if 'ffprobe' fails to retrieve information or to run). It returns a dictionary containing audio information such as the number of channels, channel layout, codec name, bit rate, and sample rate.

**Parameters:**

- `file_path` (str): The path to the audio file.

**Returns:**

- `Dict[str, Union[str, int]]`: A dictionary containing audio information, including:
  - `'channels'` (int): Number of audio channels.
  - `'channel_layout'` (str): Channel layout description.
  - `'codec_name'` (str): Audio codec name.
  - `'bit_rate'` (str): Audio bit rate or subtype.
  - `'sample_rate'` (int): Audio sample rate.

**Raises:**

- `ValueError`: If the file information cannot be read due to data inconsistencies or corruption.
- `KeyError`: If the `'channels'` key is not found in the audio information.
- `OSError`: If analysis with 'ffprobe' fails (but it's being excepted).


**Example:**

Get information about an audio file "sample.wav"

```python
file_path = "path/to/sample.wav"
audio_info = get_audio_info(file_path)
print(audio_info)
```

Output:
```python
{
    'channels': 2,
    'channel_layout': 'stereo',
    'codec_name': 'pcm_s16le',
    'bit_rate': 's16',
    'sample_rate': 44100
}
```

<br>

### `validate_paths`

This function validates the provided `input` and `output` paths, ensuring they are valid `absolute` paths. It can validate both input files and directories. If `isdir` is set to True, the function treats the input as a directory path. This means that if input is not dir, the path won't be valid (and vise versa).

Validate input and output paths for files or directories. This function validates the provided input and output paths and ensures they are valid absolute paths. It can be used to validate both input files and directories, and optionally, output directories.

**Parameters:**

- `input` (str): The path to the input file or directory.
- `out_dir` (str, optional): The path to the output directory (default is None).
- `isdir` (bool, optional): If True, treats the input as a directory path; otherwise, treats it as a file path (default is False).

**Returns:**

- `Tuple[str, str, str]`: A tuple containing the validated input path (dir or file), input directory, and output directory.

**Raises:**

- `OSError`: If any of the paths is not a valid absolute path or if any of the validations fail.


### `create_outfldr`

This function creates a new output folder in the specified `out_dir` with the format `"{prefix}{suffix}"` or "{prefix}{suffix}_1", "{prefix}{suffix}_2", and so on if the folder already exists. It ensures that each folder name is unique.


**Parameters:**

- `suffix` (str): The suffix to be added to the folder name.
- `prefix` (str, optional): The prefix to be added to the folder name (default is "out_").
- `out_dir` (str): The path to the directory where the new folder will be created.

**Returns:**

- `str`: The absolute path to the newly created folder.

**Raises:**

- `ValueError`: If the specified `out_dir` does not exist or is not a valid directory.


<br>

### `smpte_order_key`

This helper function is used for sorting sound files based on the SMPTE order. It helps determine the order value of a sound file based on its filename, following the SMPTE channel naming conventions.

**Parameters:**

- `sfilename` (str): The filename of the sound file.
- `smpte` (dict, optional): The SMPTE order dictionary mapping order to channel extensions, by default SMPTE_ORDER.

**Returns:**

- `int`: The order value of the sound file, or `float('inf')` if not found in SMPTE order.

**Notes:**

This helper function is used in the core function `split_multi_sf()`.
The `SMPTE_ORDER` dict can be found in `constants.py`.

**Note:**

- This should not be changed, as it follows a specific convention.
- In the future, other channel orderings could be added here such as 'film', 'protools'.

<br>
<br>

## `constants.py`

This module provides various constants and functions related to audio channel layouts and formats.

<br>

### Channel Layouts


- `CH_LAYOUT`: List of channel layout codes that correspond to or work with ffmpeg commands.

- `CH_SMPTE`: List of channel layout codes that correspond to multi-mono track extension names.

- `CH_LAYOUT_COMP`: A dictionary that defines channel layout compositions for ffmpeg commands.

- `CH_SMPTE_COMP`: A dictionary that defines channel layout compositions for naming multi-mono tracks.


<br>



### `get_layout`:
```python
get_layout(list, *channels)
```

Generates a custom channel layout based on the given list and channel indices.

This function creates a new list of channel layout codes by selecting channels from the provided list based on the specified channel indices. It allows you to create custom channel layouts for audio processing operations.

**Parameters:**

- `list` (List[str]): The list of available channel layout codes.
- `*channels` (int): The indices of the channels to be included in the custom layout.

**Returns:**

- `List[str]`: A list of channel layout codes representing the custom layout.

**Examples:**

Assume you have a channel layout list as follows:

```python
layout_list = ['FL', 'FR', 'C', 'LFE', 'BL', 'BR']
```

To create a custom layout consisting of the front left and front right channels:
```python
custom_layout = get_layout(layout_list, 0, 1)
print(custom_layout)  # Output: ['FL', 'FR']
```
<br>

### Supported Audio Formats

- `AUDIO_FORMATS`: List of accepted audio file formats that can be analyzed by soundfile and ffprobe.

### Channel Extensions and SMPTE Order

- `CHANNEL_NAMES`: Tuple of possible channel extension names used when searching for multi-mono tracks.

- `SMPTE_ORDER`: Dictionary that maps channel indices to their corresponding SMPTE channel extension names.