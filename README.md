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

<b> PYTHON FUNCTIONALITY (BACKEND)</b>

- [Backend Implementation (python)](#backend-implementation-(python))



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
<br>
<br>



# Backend Implementation (python) 

The backend of the Audio Operations tool is implemented in Python and consists of several important files and functions that enable the execution of audio processing operations. This section provides an overview of the key files and their functionalities within the backend.



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

### File's Functions
The `project.py` script includes certain functions to run the audio processing operations efficiently.

- `run_operation(func, in_path, out_path=None, *, out_name='files', list_type='all', repeat_func=repeat_operation)`: 

    This function handles the execution of audio processing operations.
    func is the audio processing function to run.

    - `in_path`: The path to the input audio file or directory.
    - `out_path`: The output directory for processed files (default is None).
    - `out_name`: The name used for the output folder (default is 'files').
    - `list_type`: Determines the type of list passed to the operation function ('all', 'multi', 'mono', default is 'all').
    - `repeat_func`: Specifies whether the operation should be repeated for multiple files (default is repeat_operation).

    Refer to the `core_functions.py` module for the implementation details of individual audio processing functions used in the backend.



## `core_functions.py`

The `core_functions.py` module contains essential audio processing functions used by the backend of the Audio Operations tool. These functions perform specific operations such as splitting multi-channel audio, converting mono to multi-channel, converting audio formats, and more.

### `repeat_operation`

The `repeat_operation` function is used to perform a specified audio processing operation for each sound file in the provided input directory. It iterates through the input directory and applies the operation function to each sound file, saving the results in the specified output directory.

**Parameters:**
- `in_dir` (Path): The path to the input directory containing sound files.
- `out_dir` (Path, optional): The path to the output directory where the results will be saved (default is None, which uses `in_dir`).
- `list_type` (str, optional): The type of sound files to operate on ('all', 'multi', or 'mono') (default is 'all').
- `func` (Callable[[Path, Path], None]): The operation function to be applied to each sound file.



### `mono_to_multi`

The `mono_to_multi` function converts mono audio files representing different channels of a multi-mono track to a multi-channel format. The resulting multi-channel files are saved in the specified or default output directory.

**Parameters:**
- `inpt` (Path): The path to the input directory containing mono audio files.
- `outpt` (Path, optional): The path to the output directory where the converted files will be saved (default is None, which uses `inpt`).

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




### `split_multi_sf`

The `split_multi_sf` function splits a multi-channel audio file into separate mono files, preserving each channel as a separate file. The resulting files are saved in the specified or default output directory inside a folder named after the input file's base name.

**Parameters:**
- `inpt` (Path): The path to the multi-channel audio file to be split.
- `outpt` (Path, optional): The directory path where the output files will be saved (default is None, which uses the input directory).

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





### `sf_to_mov`

The `sf_to_mov` function converts multi-channel audio files to MOV format while preserving the original channel layout. The resulting MOV file is saved in the specified or default output directory.

The .mov file works as a container that contains all the separate channels of that multi-track. Each file begins at the same timecode and is sent to each respective channel. Moreover, the metadata namings of each file include their channel extension (similar to the `split_multi_sf` funciton)

**Parameters:**
- `inpt` (Path): The path to the multi-channel audio file to be converted.
- `outpt` (Path, optional): The directory path where the converted MOV file will be saved (default is None, which uses the input directory).

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





### `convert_to_audio`

The `convert_to_audio` function converts audio files to a specified audio format. The resulting audio file is saved in the specified or default output directory.

**Parameters:**
- `inpt` (Path): The path to the input audio file to be converted.
- `outpt` (Path, optional): The directory path where the converted audio file will be saved (default is None, which uses the input directory).
- `conversion` (str, optional): The target audio format to convert to (default is "wav").
- `sample_rate` (str, optional): The sample rate of the output audio (default is "48000").
- `bit_rate` (str, optional): The bit rate of the output audio (default is "pcm_s24le").




### Integration with the Backend

These core functions are integral to the operation of the audio processing tool's backend. They are called within the `project.py` script to perform various audio processing operations based on user input.

Please refer to the source code of the `core_functions.py` module for more detailed implementation details and function behavior.
