def pprint(rows, columns=None, sort_by=None, max_rows=20):
    """Pretty print rows from a list of dicts"""
    
    def _tabular(data, sort_by=0, max_len=100):
        """General function to format `data` list in tabular table"""
        # Predict formatting
        lens = [0 for _ in range(len(data[0]))]
        for entry in data:
            for i, value in enumerate(entry):
                lens[i] = max(lens[i], len(str(value)))
        fmts = [f'{{:{lens[i]}s}}' for i in range(len(lens))]
        fmt = ' '.join(fmts)

        # Store list of lines
        lines = []
        lines.append(fmt.format(*data[0]))
        lines.append('-'*(sum(lens) + len(lens) - 1))
        for entry in sorted(data[1:], key=lambda x: x[sort_by]):
            entry = [str(_) for _ in entry]
            lines.append(fmt.format(*entry))
            if len(lines) > max_rows:
                break

        # Limit columns
        if sum(lens) > max_len:
            for i, line in enumerate(lines):
                if i < 2:
                    fill = '     '
                else:
                    fill = ' ... '
                lines[i] = line[:max_len//2] + fill + line[sum(lens) - max_len//2:]
        return lines

    # Format and sort the data        
    if columns is None:
        columns = set(rows[0])
        for entry in rows:
            columns = set.union(columns, set(entry.keys()))
    if sort_by is None:
        sort_by = 0
    else:
        sort_by = columns.index(sort_by)

    # Tabularize lines and join them
    rows = [columns] + [[str(entry.get(key)) for key in columns] for entry in rows]
    lines = _tabular(rows, sort_by=sort_by)
    print('\n'.join(lines))

def _wget(url, output_dir):
    """Like wget on the command line"""
    import sys
    import os
    import shutil
    try:
        from urllib.request import urlopen  # Python 3
    except ImportError:
        from urllib2 import urlopen  # Python 2

    basename = os.path.basename(url)
    output_file = os.path.join(output_dir, basename)
    response = urlopen(url)
    length = 16*1024
    with open(output_file, 'wb') as fh:
        shutil.copyfileobj(response, fh, length)

def _upgrade_1_to_2(model):
    """Convert from schema version 1 to 2"""
    new_model = {}
    # Optional
    if "reference" in model:
        new_model["reference"] = model["reference"]
    if "doi" in model:
        new_model["doi"] = model["doi"]
    new_model["potential"] = []
    for potential in model["potential"]:
        new_potential = {}
        new_potential["type"] = potential["type"]
        new_potential["parameters"] = {}
        db = {}
        for key in potential["parameters"]:
            db[key] = {}
            nsp = len(potential["parameters"][key])
            for i in range(nsp):
                for j in range(nsp):
                    if j<i: continue
                    pair = f'{i+1}-{j+1}'
                    db[key][pair] = potential["parameters"][key][i][j]
        last_key = key
        for pair in db[last_key].keys():
            new_potential["parameters"][pair] = {key:db[key][pair] for key in db.keys()}
        new_model["potential"].append(new_potential)

    new_cutoffs = []
    for cutoff in model["cutoff"]:
        new_cutoff = {}
        new_cutoff["type"] = cutoff["type"]
        new_cutoff["parameters"] = {}
        db = {}
        for key in cutoff["parameters"]:
            db[key] = {}
            nsp = len(cutoff["parameters"][key])
            for i in range(nsp):
                for j in range(nsp):
                    if j<i: continue
                    pair = f'{i+1}-{j+1}'
                    db[key][pair] = cutoff["parameters"][key][i][j]
        last_key = key
        for pair in db[last_key].keys():
            new_cutoff["parameters"][pair] = {key:db[key][pair] for key in db.keys()}
        new_cutoffs.append(new_cutoff)
    for i, new_cutoff in enumerate(new_cutoffs):
        new_model["potential"][i]["cutoff"] = new_cutoff
    return new_model


class _objdict(dict):

    """Boots a dict with object-like attribute accessor"""

    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        del self[name]
