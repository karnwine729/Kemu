## Austin's code that I need to understand and change for Kemu

SENTINEL = "This can just be any string that you know you aren't ever gonna see ever... like ever ever"

def get_cfg(lines):
    cfg, _ = _get_cfg_internal(lines,0)
    return cfg

def _get_cfg_internal(lines, i):
    cfg = {}

    last_non_empty = ""
    while i < len(lines):
        line = lines[i]

        if '{' in line:
            foo, i = _get_cfg_internal(lines, i + 1)
            key = get_module_key(last_non_empty, cfg)
            cfg[key] = foo
        elif '}' in line:
            break
        elif '=' in line:
            key, val = parse_line(line)
            cfg[key] = val
        elif line:
            last_non_empty = line
        i += 1

    return cfg, i

def get_cfg_gen(lines):
    cfg = {}

    last_non_empty = ""
    while (line := next(lines)):
        if '{' in line:
            nest = get_cfg_gen(lines)
            cfg[last_non_empty] = nest
        elif '}' in line:
            break
        elif line.startswith('//'):
            continue
        elif '=' in line:
            key, val = parse_line(line)
            cfg[key] = val
        elif line == SENTINEL:
            break
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
        lines.append(SENTINEL)
        lg = (l for l in lines if l)

    cfg = get_cfg(lines)

    print(cfg)
