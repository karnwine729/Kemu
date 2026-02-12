## Austin's code that I need to understand and change for Kemu

import sys

def get_cfg(lines):
    lg = (l for l in lines)
    return get_cfg_rec(lg)

def get_cfg_rec(lines):
    cfg = {}

    last_non_empty = ""
    for line in lines:
        if '{' in line:
            nest = get_cfg_rec(lines)
            key = get_module_key(last_non_empty, cfg)
            cfg[key] = nest
        elif '}' in line:
            break
        elif line.startswith('//'):
            continue
        elif '=' in line:
            key, val = parse_line(line)
            cfg[key] = val
        else:
            last_non_empty = line

    return cfg

def parse_line(line):
    parts = [p.strip() for p in line.split("=")]
    return parts[0], parts[1]

def get_module_key(last_non_empty, cfg):
    key = ""
    if last_non_empty in cfg:
        cnt = len([k for k in cfg.keys() if k.startswith(last_non_empty)])
        key = f'{last_non_empty}_{cnt}'
    else:
        key = last_non_empty

    return key

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(-1)

    filename = sys.argv[1]

    lines = []
    with open(filename) as fin:
        lines = [l.strip() for l in fin.readlines()]

    cfg = get_cfg(lines)

    print(cfg)
