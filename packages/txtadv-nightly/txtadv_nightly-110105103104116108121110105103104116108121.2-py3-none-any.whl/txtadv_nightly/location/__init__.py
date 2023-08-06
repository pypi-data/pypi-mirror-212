"""Location-related utilites in txtadv. Some of these are copied in modules in txtadv."""
def get_loc_from_num(num):
    """Gets a location string from a number."""
    if num == 0:
        return 'north'
    if num == 1:
        return 'south'
    if num == 2:
        return 'east'
    if num == 3:
        return 'west'
    if num == 4:
        return 'up'
    return 'down'


def get_num_from_loc(loc):
    """Gets a number from a location string."""
    loc = loc.lower()
    if loc in ['north', 'n']:
        return 0
    if loc in ['south', 's']:
        return 1
    if loc in ['east', 'e']:
        return 2
    if loc in ['west', 'w']:
        return 3
    if loc in ['up', 'u']:
        return 4
    return 5
