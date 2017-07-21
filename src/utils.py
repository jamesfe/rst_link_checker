import re


def checkline(line):
    """ Return any non-relative links. """
    links = re.findall('<(http.*?)>', line)
    ret_vals = []
    for item in links:
        if '#' in item:
            ret_vals.append(item.split('#')[0])
        else:
            ret_vals.append(item)
    return ret_vals
