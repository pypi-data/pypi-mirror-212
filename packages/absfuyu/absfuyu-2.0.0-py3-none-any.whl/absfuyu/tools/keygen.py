# -*- coding: utf-8 -*-
"""
Mod7 product key generator (90's)

This is for educational and informative purposes only.
"""

# Library
##############################################################
import random as __random

from absfuyu import core as __core



# Function
##############################################################
def __add_char_to_fixed_str_length(
        text: str,
        desired_length: int,
        filled_text: str = "0",
        align: __core.AlignPosition = "left",
    ) -> str:
    """
    This function add a specified character into a string with fixed length

    For example:
    - str = "2" 
    - desired length = 3
     -> new_str = "002"
    
    Parameters:
    ---
    text : str
        Text
    
    desired_length : int
        Length of new text
    
    filled_text : str
        Fill the blank with `filled_text`
    
    align : AlignPosition
        "left"
        "right"
        "center"
    
    Return:
    ---
    str:
        Filled string
    """
    
    # Check conditions
    text = str(text) # Convert again to make sure
    len_different = desired_length - len(text)
    if len_different < 0: # Small length
        raise ValueError("Desired length smaller than string length.")
    if align not in ["left", "right"]: # Invalid option
        align = "left" # Default value
    
    # Start
    if align.startswith("left"):
        return f"{filled_text*len_different}{text}"
    elif align.startswith("right"):
        return f"{text}{filled_text*len_different}"
    else: # Center alignment
        return f"{filled_text*int(len_different/2)}{text}{filled_text*int(len_different/2)}"

def __is_mod7(text: str) -> bool:
    """Check if sum of elements in a string is divisible by 7"""
    text = str(text) # Safety convert
    try:
        return sum([int(x) for x in text]) % 7 == 0
    except:
        raise ValueError("Invalid string")

def __mod7_gen(num_of_digits: int) -> str:
    """
    Generate a number with desired length that is divisible by 7

    Parameters:
    ---
    num_of_digits : int
        Length of number

    Return:
    ---
    str:
        Mod7 number
    """
    
    # Init
    mod7_num: int = 0
    
    # Conditions
    max_value = 10**num_of_digits-1
    mod7_valid = False
    invalid_digits = [0,8,9] # Invalid last digit
    
    # Loop
    while not mod7_valid:
        # Gen num
        mod7_num = __random.randint(0,max_value)
        
        # Check last digit
        if int(str(mod7_num)[-1]) in invalid_digits:
            continue
        
        # Check divide by 7
        if __is_mod7(mod7_num):
            mod7_valid = True
    
    # Output
    return __add_char_to_fixed_str_length(
        text=mod7_num,
        desired_length=num_of_digits)


def mod7_cd_key(fast: bool = False) -> str:
    r"""
    CD Key generator

    Format: XXX-XXXXXXX                               \
    Rules:
    - Last seven digits must add to be divisible by 7
    - First 3 digits cannot be 333, 444,..., 999
    - Last digit of last seven digits cannot be 0, 8 or 9
    
    Parameters:
    ---
    fast : bool
        Use pre-generated key
        [Default: False]
    
    Return:
    ---
    str:
        Mod7 Key
    """

    # Fast mode: pre-generated key
    if fast:
        return "111-1111111"

    # PART 01
    part1_valid = False
    part1_not_valid_digits = [333, 444, 555, 666, 777, 888]
    part1: str = ""
    while not part1_valid: # Loop check
        part1_num = __random.randint(0,998) # Gen random int from 0 to 998
        # part1_num = __random.randint(100,300) # or just use this
        if part1_num not in part1_not_valid_digits:
            part1 = __add_char_to_fixed_str_length(
                text=str(part1_num), desired_length=3) # Convert into string
            part1_valid = True # Break loop

    # PART 02
    part2 = __mod7_gen(num_of_digits=7)

    # OUTPUT
    return f"{part1}-{part2}"


def mod7_11_digit_key(fast: bool = False) -> str:
    """
    11-digit CD Key generator

    Format: XXXX-XXXXXXX
    - XXXX: Can be anything from 0001 to 9991.
    The last digit must be 3rd digit + 1 or 2.
    When the result is > 9, it overflows to 0 or 1.
    - XXXXXXX: Same as CD Key
    
    Parameters:
    ---
    fast : bool
        Use pre-generated key
        [Default: False]
    
    Return:
    ---
    str:
        Mod7 Key
    """
    
    # Fast mode: pre-generated key
    if fast:
        return "0001-0000007"
    
    # PART 01
    part1_valid = False
    part1: str = ""
    while not part1_valid:
        part1_1_num = __random.randint(0,999) # Random 3-digit number
        last_digit_choice = [1, 2] # Choice for last digit
        part1_2_num = int(str(part1_1_num)[-1]) + __random.choice(last_digit_choice) # Make last digit
        if part1_2_num > 9: # Check condition then overflow
            part1_2_num = int(str(part1_2_num)[-1])
        part1_str = str(part1_1_num) + str(part1_2_num) # Concat string
        if int(part1_str) > 9991: # Check if < 9991
            continue
        else:
            part1 = __add_char_to_fixed_str_length(text=part1_str, desired_length=4)
            part1_valid = True

    # PART 02
    part2 = __mod7_gen(num_of_digits=7)

    # OUTPUT
    return f"{part1}-{part2}"
    

def mod7_oem_key(fast: bool = False) -> str:
    """
    OEM Key generator

    Format: ABCYY-OEM-0XXXXXX-XXXXX
    - ABC: The day of the year. It can be any value from 001 to 366
    - YY: The last two digits of the year. It can be anything from 95 to 03
    - 0XXXXXX: A random number that has a sum that is divisible by 7 and does not end with 0, 8 or 3.
    - XXXXX: A random 5-digit number

    Parameters:
    ---
    fast : bool
        Use pre-generated key
        [Default: False]
    
    Return:
    ---
    str:
        Mod7 Key
    """
    
    # Fast mode: pre-generated key
    if fast:
        return "00100-OEM-0000007-00000"
    
    # PART ABC
    abc_num = str(__random.randint(1,365))
    # abc_num = str(__random.randint(1,366))
    abc_part = __add_char_to_fixed_str_length(text=abc_num, desired_length=3)

    # PART YY
    year_choice = ["95", "96", "97", "98", "99", "00", "01", "02"]
    # isleap = [False, True, False, False, False, True, False, False]
    # year_choice = ["95", "96", "97", "98", "99", "00", "01", "02", "03"] # "03" not wotk on win95
    y_part = __random.choice(year_choice)

    # NUM PART
    num_part = __mod7_gen(num_of_digits=6)

    # NUM PART 02
    num_2 = str(__random.randint(0,99999))
    num_part_2 = __add_char_to_fixed_str_length(text=num_2, desired_length=5)

    # OUTPUT
    return f"{abc_part}{y_part}-OEM-0{num_part}-{num_part_2}"


def mod7_combo(fast: bool = False):
    """
    A combo that consist of CD, 11-digit, and OEM Key

    Parameters:
    ---
    fast : bool
        Use pre-generated key
        [Default: False]
    
    Return:
    ---
    dict:
        Mod7 Key combo
    """
    out = {
        "CD Key": mod7_cd_key(fast=fast),
        "OEM Key": mod7_oem_key(fast=fast),
        "11-digit Key": mod7_11_digit_key(fast=fast)
    }
    return out


def __xp_gen(show_all: bool = False) -> str:
    """
    XP Gen

    Unused

    and

    **SHOULD NOT BE USED!**
    """
    
    # Library
    import base64
    import json

    # Data
    data1='ewogICAgIk1haW4gWFAiOiBbCiAgICAgICAgIkpEM1QyLVFIMzZSLVg'
    data2='3VzJXLTdSM1hULURWUlBRIgogICAgXSwKICAgICJXaW5kb3dzIFhQIF'
    data3='NQMiI6IFsKICAgICAgICAiUVc5QjgtM1RKWFctWDM2SEYtUVQ5NFgtO'
    data4='FJYR0QiLAogICAgICAgICJKVkJGUS1LREI4Sy1GOTdNUi1LNEdUSC1E'
    data5='VDRXNiIsCiAgICAgICAgIkZWN1hNLUM0UVdDLTlSS1Q5LVg3MldZLU0'
    data6='zRlc4IiwKICAgICAgICAiRzlEMlQtTUg5QkYtSEs3NjQtUUpSN1gtTU'
    data7='pLR00iLAogICAgICAgICJUSDdUTS1CQkhZSi03N0cyNi1NMlcyVC1DS'
    data8='kJDMyIsCiAgICAgICAgIlZDRlFELVY5Rlg5LTQ2V1ZILUszQ0Q0LTRK'
    data9='M0pNIiwKICAgICAgICAiRFEzUEctMlBUR0otNDNGUDItUlBSS0ItUUJ'
    data10='ZUlkiLAogICAgICAgICJCNjZWWS00RDk0VC1UUFBENC00M0Y3Mi04WD'
    data11='RGWSIKICAgIF0sCiAgICAiV2luZG93cyBYUCBTUDMiOiBbCiAgICAgI'
    data12='CAgIkpEM1QyLVFIMzZSLVg3VzJXLTdSM1hULURWUlBRIiwKICAgICAg'
    data13='ICAiWE1EQ1YtMlRKTVItN0pENjYtWVRWTUstVjdQQkQiLAogICAgICA'
    data14='gICJYNk1ZWS02QkgzVC1ZUkJUOC1IOFlQSC1SRzY4VCIsCiAgICAgIC'
    data15='AgIk1ZSFZULVdRNDlNLVFSUFZGLVY4NkZDLVAzUjhZIiwKICAgICAgI'
    data16='CAiUlQzUUQtVjhQNFAtQzczRFktUkNHNFItUU02WUQiLAogICAgICAg'
    data17='ICJNUjQ5Ui1EUkpYWC1NNlBYMi1WOTZCRi04Q0tCSiIsCiAgICAgICA'
    data18='gIk1WRjRELVc3NzRLLU1DNFZNLVFZNlhZLVIzOFRCIgogICAgXQp9'
    data98=data1+data2+data3+data4+data5+data6+data7+data8+data9+data10
    data99=data11+data12+data13+data14+data15+data16+data17+data18
    data=data98+data99

    # Convert data
    decoded_data = base64.b64decode(data.encode("utf-8")).decode("utf-8")
    real_data = json.loads(decoded_data)
    
    # Output
    if show_all:
        return real_data
    else:
        return real_data['Main XP'][0]