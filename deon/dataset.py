"""DeON dataset management utilities."""

import os
import shutil
import tempfile

import deon.data.sources as sources
import deon.data.dataset_util as dataset_util


def _tmp_dir(tmp, force):
    if not tmp:
        return tempfile.mkdtemp()

    if os.path.exists(tmp):
        files = os.listdir(tmp)
        if files and force:
            shutil.rmtree(tmp)
            os.makedirs(tmp)
    else:
        os.makedirs(tmp)

    return tmp


def _dest_dir(dest, force):
    if os.path.exists(dest):
        if force:
            shutil.rmtree(dest)
    else:
        os.makedirs(dest)
    return dest


def _clean(tmp):
    for filename in os.listdir(tmp):
        if filename.endswith('.tsv')\
            or filename.endswith('.rio')\
            or filename.endswith('.idx'):
            os.remove(os.path.join(tmp, filename))


def _move_to_dataset(dest, tmp):
    for filename in os.listdir(tmp):
        if filename.startswith(('test', 'train', 'validation', 'vocabolary')):
            frompath = os.path.join(tmp, filename)
            topath = os.path.join(dest, filename)
            shutil.move(frompath, topath)
    pass


def build(source_keys=('w00',), dest='dataset', split=(70, 20, 10), tmp=None, force=False, download=False, clean=False):
    """Build the DeON dataset from differnt data sources."""
    print("Build the DeON dataset from differnt data sources.")
    dest = _dest_dir(dest, force)
    tmp = _tmp_dir(tmp, force)

    if clean:
        _clean(tmp)

    [sources.resolve(key).pull(tmp, download) for key in source_keys]
    print('Splitting dataset', split, '...')
    dataset_util.split_dataset(tmp, split)
    _move_to_dataset(dest, tmp)
    print('Done!')