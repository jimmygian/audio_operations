# Channel Layout that corresponds to/ works with ffmpeg commands
CH_LAYOUT = [
    'FL',
    'FR',
    'FC',
    'LFE',
    'BL',
    'BR',
    'FLC',
    'FRC',
    'BC',
    'SL',
    'SR',
    'TC',
    'TFL',
    'TFC',
    'TFR',
    'TBL',
    'TBC',
    'TBR',
    'DL',
    'DR',
    'WL',
    'WR',
    'SDL',
    'SDR',
    'LFE2'
]

# Channel Layout that corresponds to multi-mono track extension names
CH_SMPTE = [
    'L',
    'R',
    'C',
    'LFE',
    'Ls',
    'Rs',
    'FLC',
    'FRC',
    'BC',
    'Lsr',
    'Rsr',
    'TC',
    'Ltf',
    'TFC',
    'Rtf',
    'Ltb',
    'TBC',
    'Rtb',
    'DL',
    'DR',
    'WL',
    'WR',
    'SDL',
    'SDR',
    'LFE2'
]



# Channel Layout Composition
def get_layout(list, *channels):
    """
    Generate a custom channel layout based on the given list and channel indices.

    This function creates a new list of channel layout codes by selecting channels
    from the provided list based on the specified channel indices. It allows you to
    create custom channel layouts for audio processing operations.

    Parameters
    ----------
    list : List[str]
        The list of available channel layout codes.
    *channels : int
        The indices of the channels to be included in the custom layout.

    Returns
    -------
    List[str]
        A list of channel layout codes representing the custom layout.

    Examples
    --------
    Assume you have a channel layout list as follows:

    >>> layout_list = ['FL', 'FR', 'C', 'LFE', 'BL', 'BR']

    To create a custom layout consisting of the front left and front right channels:

    >>> custom_layout = get_layout(layout_list, 0, 1)
    >>> print(custom_layout)
    ['FL', 'FR']

    To create a custom layout consisting of the center and LFE channels:

    >>> custom_layout = get_layout(layout_list, 2, 3)
    >>> print(custom_layout)
    ['C', 'LFE']
    """
    return [list[channel] for channel in channels]

CH_LAYOUT_COMP = {
    # This composition is used for the channel_layout in ffmpeg commands
    'mono': get_layout(CH_LAYOUT, 2),
    'stereo': get_layout(CH_LAYOUT, 0, 1),
    '2.1': get_layout(CH_LAYOUT, 0, 1, 3),
    '3.0': get_layout(CH_LAYOUT, 0, 1, 2),
    '3.0(back)': get_layout(CH_LAYOUT, 0, 1, 8),
    '4.0': get_layout(CH_LAYOUT, 0, 1, 2, 8),
    'quad': get_layout(CH_LAYOUT, 0, 1, 4, 5),
    'quad(side)': get_layout(CH_LAYOUT, 0, 1, 9, 10),
    '3.1': get_layout(CH_LAYOUT, 0, 1, 2, 3, 8),
    '5.0': get_layout(CH_LAYOUT, 0, 1, 2, 4, 5),
    '5.0(side)': get_layout(CH_LAYOUT, 0, 1, 2, 9, 10),
    '4.1': get_layout(CH_LAYOUT, 0, 1, 2, 3, 8, 5),
    '5.1': get_layout(CH_LAYOUT, 0, 1, 2, 3, 4, 5),
    '5.1(side)': get_layout(CH_LAYOUT, 0, 1, 2, 3, 9, 10),
    '6.0': get_layout(CH_LAYOUT, 0, 1, 2, 8, 9, 10),
    '6.0(front)': get_layout(CH_LAYOUT, 0, 1, 6, 7, 9, 10),
    'hexagonal': get_layout(CH_LAYOUT, 0, 1, 2, 4, 5, 8),
    '6.1': get_layout(CH_LAYOUT, 0, 1, 2, 3, 8, 9, 10),
    '6.1(front)': get_layout(CH_LAYOUT, 0, 1, 3, 6, 7, 9, 10),
    '7.0': get_layout(CH_LAYOUT, 0, 1, 2, 4, 5, 9, 10),
    '7.0(front)': get_layout(CH_LAYOUT, 0, 1, 2, 6, 7, 9, 10),
    '7.1': get_layout(CH_LAYOUT, 0, 1, 2, 3, 4, 5, 9, 10),
    '7.1(wide)': get_layout(CH_LAYOUT, 0, 1, 2, 3, 4, 5, 6, 7),
    '7.1(wide-side)': get_layout(CH_LAYOUT, 0, 1, 2, 3, 6, 7, 9, 10),
    'octagonal': get_layout(CH_LAYOUT, 0, 1, 2, 4, 5, 8, 9, 10),
    'downmix': get_layout(CH_LAYOUT, 18, 19)
}

CH_SMPTE_COMP = {
    # This composition is used for when naming multi-mono tracks
    'mono': get_layout(CH_SMPTE, 2),
    'stereo': get_layout(CH_SMPTE, 0, 1),
    '2.1': get_layout(CH_SMPTE, 0, 1, 3),
    '3.0': get_layout(CH_SMPTE, 0, 1, 2),
    '3.0(back)': get_layout(CH_SMPTE, 0, 1, 8),
    '4.0': get_layout(CH_SMPTE, 0, 1, 2, 8),
    'quad': get_layout(CH_SMPTE, 0, 1, 4, 5),
    'quad(side)': get_layout(CH_SMPTE, 0, 1, 9, 10),
    '3.1': get_layout(CH_SMPTE, 0, 1, 2, 3, 8),
    '5.0': get_layout(CH_SMPTE, 0, 1, 2, 4, 5),
    '5.0(side)': get_layout(CH_SMPTE, 0, 1, 2, 9, 10),
    '4.1': get_layout(CH_SMPTE, 0, 1, 2, 3, 8, 5),
    '5.1': get_layout(CH_SMPTE, 0, 1, 2, 3, 4, 5),
    '5.1(side)': get_layout(CH_SMPTE, 0, 1, 2, 3, 9, 10),
    '6.0': get_layout(CH_SMPTE, 0, 1, 2, 8, 9, 10),
    '6.0(front)': get_layout(CH_SMPTE, 0, 1, 6, 7, 9, 10),
    'hexagonal': get_layout(CH_SMPTE, 0, 1, 2, 4, 5, 8),
    '6.1': get_layout(CH_SMPTE, 0, 1, 2, 3, 8, 9, 10),
    '6.1(front)': get_layout(CH_SMPTE, 0, 1, 3, 6, 7, 9, 10),
    '7.0': get_layout(CH_SMPTE, 0, 1, 2, 4, 5, 9, 10),
    '7.0(front)': get_layout(CH_SMPTE, 0, 1, 2, 6, 7, 9, 10),
    '7.1': get_layout(CH_SMPTE, 0, 1, 2, 3, 4, 5, 9, 10),
    '7.1(wide)': get_layout(CH_SMPTE, 0, 1, 2, 3, 4, 5, 6, 7),
    '7.1(wide-side)': get_layout(CH_SMPTE, 0, 1, 2, 3, 6, 7, 9, 10),
    'octagonal': get_layout(CH_SMPTE, 0, 1, 2, 4, 5, 8, 9, 10),
    'downmix': get_layout(CH_SMPTE, 18, 19)
}



# # Accepted formats of files that can be analyzed by ffprobe - UNUSED but good to keep -
# AUDIO_FORMATS = ['wav', 'flac', 'ogg', 'aiff', 'aif', 'aifc', 'mp3', 'aac', 'm4a', 'mp4', '3gp', 'caf']

# Accepted formats of files that can be analyzed by soundfile (and ffprobe)
AUDIO_FORMATS = ['wav', 'flac', 'ogg', 'aiff', 'aifc', 'mp3', 'aac']


# All the possible channel extensions I could possibly think of - used when searching for multi-mono tracks
CHANNEL_NAMES = (
    "LT",
    "RT",
    "L",
    "R",
    "C",
    "Ls",
    "Rs",
    "LFE",
    "Lss",
    "Rss",
    "Lrs",
    "Lsr",
    "Rrs",
    "Rsr",
    "Ltf",
    "Rtf",
    "Ltr",
    "Rtr",
    "Lts",
    "Rts",
    "FL",
    "F.L",
    "T.L",
    "FR",
    "F.R",
    "T.R",
    "FC",
    "F.C",
    "SL",
    "SR",
    "SBL",
    "SB.L",
    "SBR",
    "SB.R",
    "TFL",
    "TF.L",
    "FHL",
    "FH.L",
    "TFR",
    "TF.R",
    "FHR",
    "FH.R",
    "TBL",
    "TB.L",
    "RHL",
    "RH.L",
    "TBR",
    "TB.R",
    "RHR",
    "RH.R",
    "Vhl",
    "Vhr",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "BL",
    "BR",
    "FLC",
    "FRC",
    "FL.C",
    "FR.C",
    "BC",
    "TC",
    "T.C",
    "TFC",
    "TF.C",
    "TBC",
    "TB.C",
    "DL",
    "DR",
    "WL",
    "WR",
    "SDL",
    "SD.L",
    "SDR",
    "SD.R",
    "LFE2",
)


SMPTE_ORDER = {
    "1": ["L", "LT"],
    "2": ["R", "RT"],
    "3": ["C"],
    "4": ["Lfe"],
    "5": ["Ls", "Lss"],
    "6": ["Rs", "Rss"],
    "7": ["Lsr", "Lrs"],
    "8": ["Rsr", "Rrs"],
    "9": ["Lts", "Ltf", "Vhl"],
    "10": ["Rts", "Rtf", "Vhr"],
    "11": ["Ltr", "Ltb"],
    "12": ["Rtr", "Rtb"],
}






















