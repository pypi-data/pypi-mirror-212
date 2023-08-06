try:
    from ._version import version as __version__
except ImportError:
    __version__ = "not-installed"

from ._reader import napari_get_reader
from ._dock_widget import DataPreview
