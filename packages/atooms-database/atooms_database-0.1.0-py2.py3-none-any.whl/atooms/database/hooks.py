import os
import re
import numpy
from atooms.core.utils import tipify
from atooms.trajectory import Trajectory
from atooms.system.particle import distinct_species, composition


def model_version(path, model, version=0):
    return {
	"model": model,
        "version": version,
    }

def format_extension(path, format=None):
    if format is None:
        ext = os.path.splitext(path)[-1].strip('.')
        if len(ext) > 0:
            format = ext
    return {
        "format": format,
        "extension": ext
    }

def metadata_from_atooms(path):
    th = Trajectory(path)
    system = th[0]
    radii = system.dump('particle.radius')
    db = {}
    db['format'] = str(th.__class__)
    db['frames'] = len(th)
    db['megabytes'] = int((os.path.getsize(th.filename) / 1e6))
    db['particles'] = len(system.particle)
    db['species'] = ', '.join(distinct_species(system.particle))
    db['composition'] = dict(composition(system.particle))
    db['size dispersion'] = str((numpy.std(radii) / numpy.mean(radii)))
    db['density'] = round(system.density, 10)
    if system.cell is not None:
        db['cell side'] = str(list(system.cell.side))[1: -1]
        db['cell volume'] = system.cell.volume
    if len(th) > 1:
        db['steps'] = int(th.steps[-1])
        db['duration'] = int(th.times[-1])
        db['timestep'] = float(th.timestep)
        db['block size'] = int(th.block_size)
        db['grandcanonical'] = th.grandcanonical
    th.close()
    return db

def metadata_from_path(path, aliases=(('T', 'temperature'),
                                      ('P', 'pressure'))):
    db = {}
    for entry in os.path.dirname(path).split('/'):
        for sub in entry.split('_'):
            res = re.match('([a-zA-Z]*)([0-9.]*)', sub)
            if len(res.group(2)) > 0:
                key = res.group(1)
                for alias in aliases:
                    if key == alias[0]:
                        key = alias[1]
                    db[key] = tipify(res.group(2))
    return db
