"""
Database of interaction models and samples for classical molecular
dynamics and Monte Carlo simulations

Note: accessing the database should only be done via the public,
read-only API defined below. Inserting new entries on a checked-out
database should only be done for registering new database or samples
in the official repository.
"""

import os
import glob
import json
import tempfile
import shutil
import hashlib
from copy import deepcopy
from .helpers import _wget
from . import _schemas
from . import f90, rumd
from .database import _TinyDB, Database, Query
from .helpers import pprint
import hooks

_root = os.path.dirname(__file__)
_storage = os.path.join(_root, 'storage')
schemas = {1: _schemas.m1, 2: _schemas.m2}
default_schema_version = 1

# Databases
samples = Database(os.path.join(_storage, "_db.json"))
samples.storage_path='{model}/{version}_{md5_hash}'
models = _TinyDB(os.path.join(_root, "_db.json"))

# Default query
query = Query()

# Public API

def model(name, version=0, schema_version=None):
    """
    Return database matching `name` and optionally `version`.

    The default `version` is 0 (original model); setting
    `version=None` will return a list of all matching database.
    """
    def _capitalize(name):
        return '-'.join([entry.capitalize() for entry in name.split('_')])
    if schema_version is None:
        schema_version = default_schema_version
        
    matches = models.search(((query.name == name) | (query.name == _capitalize(name))) &
                             (query.version == version) &
                             (query.schema_version == schema_version))
    if len(matches) == 0:
        raise KeyError(f'Model {name} not found with schema {schema_version}')
    return matches[0]

def sample(path):
    """
    Return a single sample matching the path
    """
    matches = samples.search(query.path == path)
    if len(matches) == 0:
        raise KeyError(f'Model {name} not found with schema {schema_version}')
    return matches[0]

# Potentials and cutoffs

# TODO: implement add() method with checks on existence
from inspect import getmembers, isfunction, isclass
from .helpers import _objdict
from . import _potentials
from . import _cutoffs

potentials = _objdict()
for name, func in getmembers(_potentials, isfunction):
    potentials[name] = func

cutoffs = _objdict()
for name, cls in getmembers(_cutoffs, isclass):
    cutoffs[name] = cls

def potential(name):
    return potentials[name]
    
def cutoff(name):
    return cutoffs[name]

# Internal API for entries to database

# TODO: This should be done as import via an org mode file
def add_model(path):
    """
    If `path` is a directory, add all json files in there to the
    global `database`. If `path` ends with `json`, it will be assumed
    to be match one or multiple json files (ex. `*.json`).
    """
    if path.endswith('json'):
        search_path = glob.glob(path)
    else:
        search_path = glob.glob('{}/*.json'.format(path))

    for _path in search_path:
        # Read json file
        with open(_path) as fh:
            try:
                model = json.load(fh)
            except (ValueError, json.decoder.JSONDecodeError):
                print('Error reading file {}'.format(_path))
                raise

        # By default, the model name is the file basename (stripped of .json)
        if 'name' not in model:
            name = os.path.basename(_path)[:-5]
            model['name'] = '-'.join([entry.capitalize() for entry in name.split('_')])
        if 'version' not in model:
            model['version'] = 0
        model['schema_version'] = _schema_version(model)

        # Store model in database
        query = Query()
        models.upsert(model,
                      (query.name == model["name"]) &
                      (query.version == model["version"]) &
                      (query.schema_version == model["schema_version"]))

# def store_from_json(json_file, pretend=False):
#     import json
#     with open(json_file) as fh:
#         data = json.load(fh)
#         data["path"] = os.path.join(os.path.dirname(json_file),
#                                     os.path.basename(data["path"]))
#         store(pretend=pretend, **data)

        
# Model schema internal helpers

def _validate_model(model, schema_version=None):
    from jsonschema import validate
    if schema_version is None:
        schema_version = default_schema_version
    validate(instance=model, schema=schemas[schema_version])

def _schema_version(model):
    """
    Return the schema version of the model
    """
    from jsonschema import ValidationError

    # Validate model against either version
    valid = []
    for schema_version in [1, 2]:
        try:
            _validate_model(model, schema_version)
            valid.append(schema_version)
        except ValidationError:
            pass
    # Return the schema id
    if len(valid) == 1:
        return valid[0]
    elif len(valid) == 0:
        raise ValidationError(f'invalid model {model}')
    else:
        raise InternalError(f'model {model} is valid for multiple schemas, this should not happen')

def _convert(model, schema_version):
    """
    Convert model to schema `schema_version`. Do nothing is schema version is already the requested one
    """
    from .helpers import _upgrade_1_to_2
    if _schema_version(model) == schema_version:
        return model
    elif _schema_version(model) == 1 and schema_version == 2:
        return _upgrade_1_to_2(model)
    else:
        raise ValueError('cannot handle this conversion')

