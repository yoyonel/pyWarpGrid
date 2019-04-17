"""
"""
import logging
import pickle
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from warp_grid.warp_map_simulation import WarpMapSimulation

logger = logging.getLogger(__name__)


@dataclass
class WarpMapRecorder:
    warp_map_simu: WarpMapSimulation

    record_freq: int = 4

    export_dir: Path = Path(tempfile.gettempdir())

    export_fn: str = field(init=False)
    export_fp: Path = field(init=False)

    def __post_init__(self):
        self.export_fn = ''.join(f"""
        warp#{self.record_freq}hz#{self.warp_map_simu.w}
        #{self.warp_map_simu.h}
        #{self.warp_map_simu.size}.pkl
        """.split())
        self.export_fp = Path.joinpath(self.export_dir, self.export_fn)
        logger.debug(f"Export filepath={self.export_fp}")

    def record(self):
        logger.debug(f"Record into: {self.export_fp} ...")
        with self.export_fp.open("ab") as record_file:
            pickle.dump(self.warp_map_simu.get_web_crossings(), record_file)
