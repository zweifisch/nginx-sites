color_map = {
    'black': 0,
    'red': 1,
    'green': 2,
    'yellow': 3,
    'blue': 4,
    'magenta': 5,
    'cyan': 6,
    'white': 7,
}

csi = '\x1b['
reset = '\x1b[0m'


def formatter(fg, bg=None, bold=False):
    params = []
    if bg in color_map:
        params.append(str(color_map[bg] + 40))
    if fg in color_map:
        params.append(str(color_map[fg] + 30))
    if bold:
        params.append('1')

    def format(message):
        if params:
            message = ''.join((csi, ';'.join(params),
                               'm', message, reset))
        return message

    return format
