def fix_dups(mylist, sep="", start=1, update_first=True):
    """
    https://stackoverflow.com/a/68916219/5168563
    """

    mylist_dups = {}
    # Build dictionary containing val: [occurrences, suffix]
    for val in mylist:
        if val not in mylist_dups:
            mylist_dups[val] = [1, start - 1]
        else:
            mylist_dups[val][0] += 1

    # Define function to update duplicate values with suffix, check if updated value already exists
    def update_val(val, num):
        temp_val = sep.join([str(x) for x in [val, num]])
        if temp_val not in mylist_dups:
            return temp_val, num
        num += 1
        return update_val(val, num)

    # Update list
    for i, val in enumerate(mylist):
        if mylist_dups[val][0] > 1:
            mylist_dups[val][1] += 1
            if update_first or mylist_dups[val][1] > start:
                new_val, mylist_dups[val][1] = update_val(val, mylist_dups[val][1])
                mylist[i] = new_val

    return mylist
