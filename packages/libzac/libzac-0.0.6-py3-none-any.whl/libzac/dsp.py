import numpy as np
from packaging import version

def rolling_window(array:np.ndarray, window:int, step:int=1):
    """ return rolling window matrix of input `array` with `step`, 
        drop tails that not enough for one window. NOTE: THIS FUNCTION
        RETURN A "VIEW" OF `array`, THEY POINT TO SAME OBJECT IN MEMORY!
            Example:
            >> rolling_window([0,1,2,3,4,5,6,7,8,9], 5, 2) =  
            [[0, 1, 2, 3, 4],
             [2, 3, 4, 5, 6],
             [4, 5, 6, 7, 8]]
    """
    if version.parse(np.version.version) < version.parse('1.20.0'):
        # before numpy 1.20.0
        shape = array.shape[:-1] + (array.shape[-1] - window + 1, window)
        strides = array.strides + (array.strides[-1],)
        return np.lib.stride_tricks.as_strided(array, shape=shape, strides=strides)[::step]
    else:
        # sliding_window_view() added after numpy 1.20.0
        return np.lib.stride_tricks.sliding_window_view(array, window)[::step]

def sig2frames(array:np.ndarray, window:int, overlap:int=0, padding:bool=True):
    """ similiar to `rolling_window()`, where `overlap = window - step`, 
        and if `padding` is True, pad zeros to tails to fill up a window.
        NOTE: THIS FUNCTION RETURN A "COPY" of `array`, THEY POINT TO DIFFERENT OBJECT"""
    assert 0 <= overlap < window
    step = window - overlap
    slice_window = rolling_window(array, window, step).copy()

    # NOTE: if you do statistic on each window, result is inaccurate 
    # for last window if there is padding because of the padding zeros.
    #   if the array already ends with zeros, it may be difficult to 
    # distinguish the newly appended zeros from the existing ones.
    if padding: 
        remain_data = array[slice_window.shape[0]*step:]
        last_frame = np.pad(remain_data, (0, window-remain_data.size))
        slice_window = np.vstack([slice_window, last_frame])
    return slice_window