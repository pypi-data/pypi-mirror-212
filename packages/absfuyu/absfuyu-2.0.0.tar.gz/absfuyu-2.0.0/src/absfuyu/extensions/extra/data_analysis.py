"""
ABSFUYU-EXTRA: DATA ANALYSIS
-------------
"""



# Library
##############################################################
import random as __random
import itertools as __itertools
__EXTRA_MODE = False
__ERROR_MSG = "This feature is in absfuyu[extra] package"
try:
    import pandas as __pd
    import numpy as __np
    import matplotlib.pyplot as __plt
    from scipy import stats as __stats
except ImportError:
    from absfuyu.config import show_cfg as __aie
    if __aie("auto-install-extra", raw=True):
        __cmd: str = "python -m pip install -U absfuyu[extra]".split()
        from subprocess import run as __run
        __run(__cmd)
    else:
        raise SystemExit(__ERROR_MSG)
else:
    __EXTRA_MODE = True



# Function
##############################################################
def isloaded():
    try:
        if __EXTRA_MODE:
            return True
        else:
            return False
    except:
        return True

def __validate():
    if not __EXTRA_MODE:
        raise SystemExit(__ERROR_MSG)


def summary(data):
    """
    Quick summary of data
    
    data : np.ndarray | list
    """

    __validate()
        
    if not isinstance(data, __np.ndarray):
        data = __np.array(data)

    output = {
        "Observations": len(data),
        "Mean": __np.mean(data),
        "Median": __np.median(data),
        "Mode": __stats.mode(data)[0][0],
        "Standard deviation": __np.std(data),
        "Variance": __np.var(data),
        "Max": max(data),
        "Min": min(data),
        "Percentiles": {
            "1st Quartile": __np.quantile(data, 0.25),
            "2nd Quartile": __np.quantile(data, 0.50),
            "3rd Quartile": __np.quantile(data, 0.75),
            "IQR": __stats.iqr(data),
        },
    }
    return output


def mplt_fmt_str(
        marker = None,
        linestyle = None,
        color = None,
        alt: bool = False,
        random: bool = True,
        raw: bool = False,
    ):
    r"""
    matplotlib format string helper
    ---
    This helper is ripped from the original matplotlib"s documentation

    Init
    ---
    Format string is in the form of: [marker][line][color]
    or [color][marker][line]

    Marker
    ---
    ".":    point marker
    ",":    pixel marker
    "o":    circle marker
    "v":    triangle_down marker
    "^":    triangle_up marker
    "<":    triangle_left marker
    ">":    triangle_right marker
    "1":    tri_down marker
    "2":    tri_up marker
    "3":    tri_left marker
    "4":    tri_right marker
    "8":    octagon marker
    "s":    square marker
    "p":    pentagon marker
    "P":    plus (filled) marker
    "*":    star marker
    "h":    hexagon1 marker
    "H":    hexagon2 marker
    "+":    plus marker
    "x":    x marker
    "X":    x (filled) marker
    "D":    diamond marker
    "d":    thin_diamond marker
    "|":    vline marker
    "_":    hline marker

    Linestyle
    ---
    "-":    solid line style
    "--":   dashed line style
    "-.":   dash-dot line style                     \
    ":":    dotted line style

    Color
    ---
    "b":    blue
    "g":    green
    "r":    red
    "c":    cyan
    "m":    magenta
    "y":    yellow
    "k":    black
    "w":    white

    Parameters
    ---
    alt : bool
        Alternative format string

    random : bool
        Generate random format string, 
        else generate combination
    
    raw : bool
        Return format string in list
    """

    if marker is None:
        marker_list = [
            ".", ",", "o", "v", "^", "<", ">", "1", "2", "3",
            "4", "8", "s", "p", "P", "*", "h", "H", "+", "x",
            "X", "D", "d", "|", "_",
        ]
    else:
        marker_list = marker
    
    if linestyle is None:
        linestyle_list = [
            "-", "--", "-.", ":",
        ]
    else:
        linestyle_list = linestyle
    
    if color is None:
        color_list = [
            "b", "g", "r", "c", "m", "y", "k",
            # "w",
        ]
    else:
        color_list = color
    
    if not random:
        fmt_str = [marker_list, linestyle_list, color_list]
        fmt_str_comb = ["".join(x) for x in list(__itertools.product(*fmt_str))]
        return fmt_str_comb

    format_string = [
        __random.choice(marker_list),
        __random.choice(linestyle_list),
        __random.choice(color_list),
    ]

    if raw:
        return format_string

    if alt:
        return "".join([format_string[2], format_string[0], format_string[1]])
    else:
        return "".join(format_string)

def gen_mptl_fmt_str(num):
    """
    Generate a list of matplotlib format string
    """
    # Init list
    fs = []
    
    # Error loop break
    error_count = 0
    max_error = 20000

    # Main
    while len(fs) < num:
        temp = mplt_fmt_str()
        if temp not in fs:
            fs.append(temp)
        else:
            error_count += 1
            if error_count > max_error:
                break
    
    # Output
    return fs


def divide_dataframe(df: __pd.DataFrame, by: str) -> list:
    """
    Divide df into a list of df
    """
    divided = [y for _, y in df.groupby(by)]
    # divided[0] # this is the first separated df
    # divided[len(divided)-1] # this is the last separated df
    return divided


def delta_date(df: __pd.DataFrame, date_field: str, col_name: str="delta_date"):
    """
    Calculate date interval between row
    """
    dated = df[date_field].to_list()
    cal = []
    for i in range(len(dated)):
        if i==0:
            cal.append(dated[i]-dated[i])
        else:
            cal.append(dated[i]-dated[i-1])
    df[col_name] = [x.days for x in cal]
    return df


def get_unique(df: __pd.DataFrame, col:str):
    """
    Return a list of unique values in a column
    """
    return list(df[col].unique())


def modify_date(df: __pd.DataFrame, date_col: str):
    """
    Add date, week, and year column for date_col
    """
    df["Date"] = __pd.to_datetime(df[date_col])
    df["Week"] = df["Date"].dt.isocalendar().week
    df["Year"] = df["Date"].dt.isocalendar().year
    return df


def equalize_df(data: dict, fillna = __np.nan):
    """
    Make all list in dict have equal length to make pd.DataFrame
    """
    max_len = 0
    for _, v in data.items():
        if len(v) >= max_len:
            max_len = len(v)
    for _, v in data.items():
        if len(v) < max_len:
            missings = max_len-len(v)
            for _ in range(missings):
                v.append(fillna)
    return data