from __future__ import annotations

import pathlib
import tempfile
from typing import Optional

import np_logging
import pynwb

logger = np_logging.getLogger(__name__)


def load_nwb(
    nwb_path: str | pathlib.Path,
    ) -> pynwb.NWBFile:
    """Load `pynb.NWBFile` instance from path."""
    logger.info(f'Loading .nwb file at {nwb_path}')
    with pynwb.NWBHDF5IO(nwb_path, mode='r') as f:
        return f.read()


def write_nwb(
    nwb_file: pynwb.NWBFile,
    output_path: Optional[str | pathlib.Path] = None,
    ) -> pathlib.Path:
    """
    Write `pynb.NWBFile` instance to disk.
    
    Tempfile dir is used if `output_path` isn't provided.
    """
    if output_path is None:
        output_path = pathlib.Path(tempfile.mkdtemp()) / f'{nwb_file.session_id}.nwb'
    
    nwb_file.set_modified()
    # not clear if this is necessary, but suggested by docs:
    # https://pynwb.readthedocs.io/en/stable/_modules/pynwb.html

    logger.info(f'Writing .nwb file `{nwb_file.session_id!r}` to {output_path}')
    with pynwb.NWBHDF5IO(output_path, mode='w') as f:
        f.write(nwb_file, cache_spec=True)
    logger.debug(f'Writing complete for nwb file `{nwb_file.session_id!r}`')
    return output_path
