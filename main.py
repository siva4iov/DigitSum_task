from collections import Counter
import scipy.stats as sp


def calculate_ds(value: int) -> int:
    """
    Calculate sum of digits in the number. E.g. "calculate_ds(1111)" will return 4
    value: int - value for which the sum of digits is calculated

    returns digit sum: int

    """

    res = 0  # var that store ds

    # iterate through every base of number and add each digit to var "res"
    while value > 0:
        res += value % 10
        value //= 10

    return res


def count_groups(n_customers: int) -> dict:
    """

    Manually calculate group and num of entries in every group.
    n_customers: int - num of customers for which groups are calculated

    returns groups: dict

    """

    ids = list(range(n_customers))  # array of customer's ids
    # array of groups for every id; array size equal "ids" array size
    groups = list(map(calculate_ds, ids))

    groups = Counter(groups)

    return groups


def max_ds(max_value: int, min_value: int = 0) -> int:
    """
    Calculate max value of group from given max id. E.g. with given "10" will return "9".
    max_value: int - max id 

    returns max_ds:int

    """

    # num of bases in number except first base; e.g "1000" is "3"
    base_num = len(str(max_value)) - 1
    # value of highest base in number + 1; e.g "321" -> "4"
    highest_base = int(str(max_value)[0])+1
    # +1 is needed for cases where given number ends in 9.

    # iterate through possible values with highest ds from highest until it will fit
    for n in range(highest_base, 0, -1):
        res = n * (10**base_num) - 1
        if min_value <= res <= max_value:
            return calculate_ds(res)


def min_ds(min_value: int, max_value: int) -> int:

    if min_value == 0:  # the only way to get 0
        return 0

    # num of bases in minimum number except first base; e.g "1000" is "3"
    base_num_min = len(str(min_value)) - 1
    lowest_base = int(str(min_value)[0])  # value of lowest base in number

    # num of bases in maximum number except first base; e.g "1000" is "3"
    base_num_max = len(str(max_value)) - 1
    if base_num_max > base_num_min:
        # if base of maximum greater than minimum, so it includes 1 * (10**base_num_max)
        return 1
    else:
        # iterate through possible values with lowest ds from lowest until it will fit
        for n in range(lowest_base, 10):
            res = n * (10**base_num_min)
            if min_value <= res <= max_value:
                return calculate_ds(res)


def count_groups_as_normal(n_customers: int) -> dict:
    """
    Calculate group and num of entries in every group by approximation distribution to a normal distribution.

    ### Main idea is that with an increase in the number of customers, as in the Central Limit Theorem, the distribution becomes similar to normal.
    ### Using properties of normal distribution we can roughly estimate the number of entries. It would be helpful with large amount of ids.
    ### For calculating the standard deviation, I assume that 3 sigma includes 100 percent of the entries, so it adds inaccuracies.
    ### This is the first implementation of this idea, with additional research, I think I can make the algorithm more accurate.

    n_customers: int - Num of customers, should be high enough so that the distribution looks like a normal distribution

    returns groups: dict
    """

    assert n_customers >= 500, "This method has no sense with n_customers lower than 500"

    ds_max = max_ds(n_customers-1)  # highest value of groups

    m = ds_max/2  # mode or median or mu for normal distribution
    # standart deviation, assuming in 3*std contains 100% of entries
    std = (ds_max - m)/3
    groups = {}

    rv = sp.norm(m, std)  # normal distribution similar to ours

    # iterating through each group
    for i in range(ds_max+1):
        # apply the density function and convert to int
        groups[i] = int(rv.pdf(i) * n_customers)

    return groups


def count_groups_with_first(n_customers: int, n_first_id: int) -> dict:
    """

    Manually calculate group and num of entries in every group.
    n_customers: int - num of customers for which groups are calculated
    n_first_id: first id of customers


    returns groups: dict

    """

    # array of customer's ids
    ids = list(range(n_first_id, n_first_id+n_customers))
    # array of groups for every id; array size equal "ids" array size
    groups = list(map(calculate_ds, ids))

    groups = Counter(groups)

    return groups


def count_groups_as_normal_with_first(n_customers: int, n_first_id: int) -> dict:
    """
    Calculate group and num of entries in every group by approximation distribution to a normal distribution with given first_id.

    ### Main idea is that with an increase in the number of customers, as in the Central Limit Theorem, the distribution becomes similar to normal.
    ### Using properties of normal distribution we can roughly estimate the number of entries. It would be helpful with large amount of ids.
    ### For calculating the standard deviation, I assume that 3 sigma includes 100 percent of the entries, so it adds inaccuracies.
    ### This is the first implementation of this idea, with additional research, I think I can make the algorithm more accurate.

    n_customers: int - Num of customers, should be high enough so that the distribution looks like a normal distribution
    n_first_id: first id of customers

    returns groups: dict
    """

    ds_max = max_ds(n_customers-1)  # highest value of groups

    ds_min = min_ds(n_first_id, n_customers-1)  # lowest value of groups

    m = (ds_max-ds_min)/2  # mode or median or mu for normal distribution
    # standart deviation, assuming in 3*std contains 100% of entries
    std = (ds_max - m)/3
    groups = {}

    rv = sp.norm(m, std)  # normal distribution similar to ours

    # iterating through each group
    for i in range(ds_min, ds_max+1):
        # apply the density function and convert to int
        groups[i] = int(rv.pdf(i) * n_customers)

    return groups


def concat_dicts(dict1: dict, dict2: dict) -> dict:
    """
    Helper function for adding dicts
    dict1, dict2 : dict - dicts to add

    returns dict
    """


    keys = set(list(dict1.keys()) + list(dict2.keys())) # keys from both dicts

    # iterate through keys and add values by key from both dicts 
    return {key: dict1.get(key, 0) + dict2.get(key, 0) for key in keys}


def sub_dicts(dict1: dict, dict2: dict) -> dict:
    """
    Helper function for subtractiong dicts
    dict1, dict2 : dict - dicts to add

    returns dict
    """
    
    #iterate through keys of dict1
    result = {key: dict1[key] - dict2.get(key, 0) for key in dict1.keys()}

    # removing zero values
    return {key:value for key, value in result.items() if value}


def dict_with_loc(d: dict, loc: int) -> dict:
    """
    Helper function for adding location for dict. E.g. "dict_with_loc({1:1,2:2}, loc=1)" 
    -> "{2:1, 3:2}"
    d: dict - dict which should be located
    loc: int - location value

    returns dict
    """

    return {key+loc: d[key] for key in d.keys()}


def count_groups_analytically(n_customers: int) -> dict:

    """
    New method for calculating groups by precalculating group for each base, e.g for base 1000, 10000 etc.
    After precalculating, adds the groups with respect to loc
    n_customers: int - Num of customers to calculate groups

    returns dict - groups
    """

    # precalculate Digit Sum for tens
    precalculated = {2: Counter(map(calculate_ds, range(10)))}

    # var for results
    res = {}

    # base for n_customers, e.g. "1000" -> "4"
    base = len(str(n_customers))

    # calculate Digit Sum for each base, starting from 3 (because 2 is already calculated)
    for base in range(3, base+1):
        current_calc = {}

        # every base is the sum of 10 previous base with loc
        for n in range(10):

            # loc for every previous base
            dict_to_add = dict_with_loc(precalculated[base-1], n) 
            current_calc = concat_dicts(current_calc, dict_to_add)
        
        # store values
        precalculated[base] = current_calc

    # After precalculations are done, calculate desired value

    # iterate through each base value
    for i in range(len(str(n_customers))):

        # need to remember about internal loc when calculating
        # e.g calculating tens in "350", need to add internal loc 3 besides the main loc
        internal_loc = 0
        if str(n_customers)[:i]:
            internal_loc += int(str(n_customers)[i-1])
        
        # if calculating first base, calculate it manually
        if base-i == 1:
            value = int(str(n_customers)[i])

            calculated = Counter(map(calculate_ds, range(value)))
            dict_to_add = dict_with_loc(calculated, internal_loc)

            res = concat_dicts(res, dict_to_add)
            
            # if calculating first base, then it means that this is the last calculation
            break

        base_value = int(str(n_customers)[i])

        # need to calculate with every loc in [0, base_value] with respect to internal loc
        for loc in range(base_value):
            dict_to_add = dict_with_loc(precalculated[base-i], loc+internal_loc)
            res = concat_dicts(res, dict_to_add)

    return res


def count_groups_analytically_with_first(n_customers: int, n_first_id: int) -> dict:

    """
    Same method as "count_groups_analytically", but with first id of customers given
    n_customers: int - num of customers for which groups are calculated
    n_first_id: first id of customers


    returns dict
    """
    
    # calculations without respecting n_first_id
    full = count_groups_analytically(n_customers+n_first_id)

    # calculations for unnecessary values from 0 to n_first_id-1
    unnecessary = count_groups_analytically(n_first_id)
    
    # subtracting from full values unnecessary values
    res = sub_dicts(full, unnecessary)

    return res




if __name__ == "__main__":
    # 1st function:

    # * Manual calculate function. Works slower, but calculations are accurate.
    print(f" Manual calculations for 1000 ids: {count_groups(1000)}")

    # * Normal approximation function. Works pretty fast, but calculations are inaccurate. Should be used with large amount of ids.
    print(
        f" Normal approximation for 1000 ids: {count_groups_as_normal(1000)}")

    # * Analitically calculate function. Works much faster than previous, calculations are accurate
    print(f" Analitically calculations for 1000 ids: {count_groups_analytically(1000)}")


    # 2st function:

    # * Manual calculate function.
    print(
        f" Manual calculations for 1000 ids with start at 50: {count_groups_with_first(1000, 50)}")

    # * Normal approximation function.
    print(
        f" Normal approximation for 1000 ids with start at 50: {count_groups_as_normal_with_first(1000, 50)}")

    # * Analitically calculate function.
    print(f" Analitically calculations for 1000 ids: {count_groups_analytically_with_first(1000, 50)}")

