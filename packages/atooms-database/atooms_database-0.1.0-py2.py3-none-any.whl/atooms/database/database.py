import os
import tempfile
import hashlib
from tinydb import TinyDB, Query
from atooms.core.utils import mkdir
from .helpers import _wget


class _TinyDB(TinyDB):

    def columns(self, merge=set.intersection):
        """Return columns of database"""
        cols = set(self.all()[0])
        for entry in self.all():
            cols = merge(cols, set(entry.keys()))
        return sorted(list(cols))

    
class Database(_TinyDB):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Look for the root of the db file, if present
        # This is where we will store the files, if requested
        try:
            path = self._storage._handle.name
            self.storage_root = os.path.dirname(path)
        except AttributeError:
            self.storage_root = None
        self.storage_path = '{md5_hash}'
        self._hooks = []

    def add_hook(self, hook, *args, **kwargs):
        """Register a new hook"""
        self._hooks.append((hook, args, kwargs))

    def _apply_hooks(self, entry):
        """Apply hooks and store the values in the new entry"""
        for hook in self._hooks:
            result = hook[0](os.path.join(self.storage_root, entry['path']), *hook[1], **hook[2])
            entry.update(result)
        return entry
        
    def insert(self, path, copy=False, **kwargs):
        # TODO: move path to kwargs?
        # Set paths: storage_path is what goes in the db
        if path.startswith('http'):
            tmpdir = tempfile.mkdtemp()
            basename = os.path.basename(path)
            _wget(path, tmpdir)
            local_path = os.path.join(tmpdir, basename)
        else:
            local_path = path
        # TODO: add to entry
        extension = os.path.splitext(local_path)[-1]

        # We now have a local copy in local_path, get the md5 hash
        with open(local_path, "rb") as fh:
            data = fh.read()
        md5_hash = hashlib.md5(data).hexdigest()

        # Create the new entry
        entry = {}
        # User provided data
        entry.update(**kwargs)
        # Default values
        entry['md5_hash'] = md5_hash
        # TODO: pass path explicitly to _apply_hooks() so we can use the additional metadata in defining the final path
        # TODO: handle http paths
        # If storing a local copy, we use the storage in path
        if copy:
            entry['path'] = self.storage_path.format(**entry)
        else:
            entry['path'] = path
        # Apply hooks and store the values in the new entry
        entry = self._apply_hooks(entry)
        
        # Store copy of data
        if copy:
            out_path = os.path.join(self.storage_root, entry["path"]) + extension
            with open(out_path, "wb") as fh:
                fh.write(data)

        # Add the entry to the database
        # If the file hash is found we update, else we add a new entry
        query = Query()
        self.upsert(entry, query.md5_hash == md5_hash)

    def insert_glob(self, path, copy=False, **kwargs):
        from glob import glob
        for _path in glob(path, recursive=True):
            self.insert(_path, copy, **kwargs)

    def insert_multiple(self, path, copy=False, **kwargs):
        for _path in path:
            self.insert(_path, copy, **kwargs)

    def update(self, ignore=()):
        """Useful to apply new hooks?"""
        # Move to _TinyDB?
        ignore = ['path'] + list(ignore)
        for entry in self.all():
            path = entry['path']
            kwargs = {k: entry[k] for k in entry if k not in ignore}
            self.insert(path, **kwargs)

    def copy(self, query, path='/tmp/{path}'):
        """Get a copy of `path` in the samples database and return the path to it"""
        import shutil
        paths = []
        # TODO: getting the full path via storage_root is what prevent this from
        # detaching as a standalone function
        for entry in self.search(query):
            if path is None:
                tmpdir = tempfile.mkdtemp()
                basename = os.path.basename(entry['path'])
                path = os.path.join(tmpdir, basename)
            else:
                path = path.format(**entry)
                
            if entry['path'].startswith('http'):
                _wget(entry['path'], tmpdir)
            else:
                from atooms.core.utils import mkdir
                mkdir(os.path.dirname(path))
                shutil.copy(os.path.join(self.storage_root, entry['path']), path)
            paths.append(path)
        return paths

    # The following two methods are redefined to allow for readonly
    # hooks that are applied only when accessing the
    # database. Otherwise, we can first store the hooks results in the
    # database (via some update?) and get rid of them.
    
    def __iter__(self):
        """
        Return an iterator for the default table's documents.
        """
        for entry in self.table(self.default_table_name):
            entry = self._apply_hooks(entry)
            yield entry

    def search(self, cond):
        """
        Search for all documents matching a 'where' cond.

        :param cond: the condition to check against
        :returns: list of matching documents
        """
        # TODO: how should we overload this?
        entries = self.table(self.default_table_name).search(cond)
        for entry in entries:
            self._apply_hooks(entry)
        return entries
            
