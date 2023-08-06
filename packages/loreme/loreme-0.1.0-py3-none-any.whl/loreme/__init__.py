"""
LoReMe (Long Read Methylaton) is a Python package facilitating analysis of DNA
methylation signals from PB or ONT long read sequencing data.

PB reads are aligned with `pbmm2 <https://github.com/PacificBiosciences/pbmm2>`_
and postprocessed by `pb-CpG-tools <https://github.com/PacificBiosciences/pb-CpG-tools>`_ .

ONT reads are optionally converted to `POD5 <https://github.com/nanoporetech/pod5-file-format>`_
format, then basecalled and aligned with `dorado <https://github.com/nanoporetech/dorado>`_ .

Finally, several postprocessing functions are available to generate diagnostic
statistics and plots.
"""

from loreme.version import __version__
from loreme.env import PBCPG_DIR
from loreme.pbcpg import pbcpg_check_tags, pbcpg_align_bam, pbcpg_align_bams, pbcpg_extract
from loreme.check_gpu_availability import check_gpu_availability
