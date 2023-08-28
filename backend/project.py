import os
import sys
import shutil
from core_functions import split_multi_sf, mono_to_multi, sf_to_mov, repeat_operation, convert_to_audio
from helpers import create_outfldr
from pathlib import Path
from typing import Callable, Optional, List, Dict, Tuple, Union



def main() -> None:
    """Main entry point of the audio processing tool.

    This script performs various audio processing operations based on user-provided input arguments.
    Supported operations include splitting multi-channel audio files, merging mono files to multi-channel,
    converting audio formats, and more.

    Usage:
    python main.py [input_path] [output_path] [operation_type]

    NOTE: This program is made to be used with electron's child process. If you want to use it elsewhere,
    make sure you have changed the sys.executable in get_root_folder() with the appropriate path to the bin files.

    Parameters
    ----------
    None - But arguments must be given:
    - input_path: Path to a file or folder that includes audio files
    - output_path: Path to an output directory that processed files will be stored
    - operation_type: str, the type of operation the program will execute (check the keys of FUNC_TYPE)

    Returns
    -------
    None
        The script executes the specified audio processing operation and provides terminal output.

    Notes
    -----
    - This script relies on core_functions and helpers modules for operation implementations.
    - The operation type should be one of: "split", "merge", "conform", or "convert".
    - Refer to the core_functions module for specific operation details.

    Examples
    --------
    Command line usage:
    python main.py input_audio.wav output_dir split
    """

    FUNC_TYPE = {
    "split": [split_multi_sf, True, 'multi'],
    "merge": [mono_to_multi, False, 'mono'],
    "conform": [sf_to_mov, True, 'multi'],
    "convert": [convert_to_audio, True, 'all'],
    }


    # ARGS: Get input / output absolute paths
    num_args = len(sys.argv) - 1
    if not num_args == 3:
        print("User did not provide necessary args. Usage: [inPath] [outPath] [operationType]")
        sys.exit(3)    
    else:
         in_path: Path = os.path.normpath(os.path.abspath(sys.argv[1]))
         out_dir: Path = os.path.normpath(os.path.abspath(sys.argv[2]))
         operation: str = sys.argv[3]

    # Print out that operation has started
    print(f"{operation.upper()} OPERATION STARTED...\n")


    # OPERATION INITIALIZATION

    # Declare variables depending on FUNC_TYPE
    op_type = operation
    try:
        func1 = FUNC_TYPE[operation][0]
        repeat = FUNC_TYPE[operation][1]
        list_type = FUNC_TYPE[operation][2]
    except Exception as e:
        print(f"Operation Type incorrect: '{operation}'")
        print(e)
        sys.exit(2)

    # Check if op needs repeating
    if repeat == True:
        repeat: Callable = repeat_operation

    # Run operation and print message
    try:
        output = run_operation(func1, in_path, out_dir, out_name=op_type, list_type=list_type, repeat_func=repeat)
        success_message = f"\n{op_type.upper()} OPERATION FINISHED. \n -> Output folder: {output}"
        print(success_message)
        sys.exit(0)

    except Exception as e:
        error_message = f"Failed to execute {op_type} operation."
        print(error_message)
        print(e)
        sys.exit(1)



# **MAIN'S HELPER FUNCTIONS**

def run_operation(func: Callable, in_path: Path, out_path: Optional[Path] = None, *,
                  out_name: str = 'files', list_type: str = 'all',
                  repeat_func: Callable = repeat_operation) -> Optional[Path]:
    """Run the specified audio processing operation on input files.

    Parameters
    ----------
    func : Callable
        The audio processing function to run.
    in_path : Path
        The path to the input audio file or directory of files.
    out_path : Path, optional
        The path to the output directory where processed files will be saved.
    out_name : str, optional
        The name to use for the output folder.
    list_type : str, optional
        The type of list to pass to the operation function ('all', 'multi', 'mono').
    repeat_func : Callable, optional
        The function to use for repeating the operation on multiple files.

    Returns
    -------
    Path or None
        The path to the output directory if successful, None if operation failed.

    Notes
    -----
    - This function creates an output folder for processed files.
    - Depending on the operation and list_type, it repeats the operation on multiple files if needed.
    - Errors during the operation lead to folder deletion and None return value.
    """
    # Create out folder and store its absolute path
    try:
        out_dir = create_outfldr(out_name, out_dir=out_path)
    except Exception:
        raise OSError("Could not create out_folder.")

    if repeat_func == False:
        try:
            func(in_path, out_dir)
            return out_dir
        except Exception as e:
            shutil.rmtree(out_dir, ignore_errors=True) # Deletes folder
            print(str(e))       
    else:
        # Check if path is dir or file    
        if os.path.isdir(in_path):
            try:
                repeat_func(in_path, out_dir, list_type=list_type, func=func)
                return out_dir
            except Exception as e:
                shutil.rmtree(out_dir, ignore_errors=True) # Deletes folder
                print(str(e))
        else:      
            try:
                func(in_path, out_dir)
                return out_dir
            except Exception as e:
                shutil.rmtree(out_dir, ignore_errors=True) # Deletes folder
                print(str(e))




if __name__ == "__main__":
    main()


# FUTURE OPERATIONS:
# QC video (Takes 1 mov and 1 audio file and combines them)
# Convert to DX... / mp4.. (converts videos to ProTools/QC likeable formats)
# Put files in .mov container as separate streams (digital team)
# Remap (5.1) files (problem when time stretching 5.1 files - they get unmapped and need remapping)