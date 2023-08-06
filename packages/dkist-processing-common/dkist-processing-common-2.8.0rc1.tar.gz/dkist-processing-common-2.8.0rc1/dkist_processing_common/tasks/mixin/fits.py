"""Mixin for a WorkflowDataTaskBase subclass which implements fits data retrieval functionality."""
from io import BytesIO
from pathlib import Path
from typing import Generator
from typing import Iterable
from typing import Type

from astropy.io import fits

from dkist_processing_common.models.fits_access import FitsAccessBase

tag_type_hint = Iterable[str] | str


class FitsDataMixin:
    """Mixin for the WorkflowDataTaskBase to support fits r/w operations."""

    def fits_data_read(
        self, tags: tag_type_hint
    ) -> Generator[tuple[Path, fits.HDUList], None, None]:
        """Return a generator of paths and fits HDU lists for input data matching the given tags."""
        for path in self.read(tags=tags):
            yield path, self.fits_data_open(path)

    def fits_data_read_hdu(
        self, tags: tag_type_hint
    ) -> Generator[tuple[Path, fits.PrimaryHDU | fits.CompImageHDU], None, None]:
        """Return a generator of paths and hdus for the input data matching the given tags."""
        for path, hdul in self.fits_data_read(tags=tags):
            yield path, self.fits_data_extract_hdu(hdul=hdul)

    def fits_data_read_fits_access(
        self,
        tags: tag_type_hint,
        cls: Type[FitsAccessBase],
        auto_squeeze: bool = True,
    ) -> Generator[FitsAccessBase, None, None]:
        """Return a generator of fits access objects for the input data matching the given tags."""
        for path, hdu in self.fits_data_read_hdu(tags=tags):
            yield cls(hdu=hdu, name=str(path), auto_squeeze=auto_squeeze)

    @staticmethod
    def fits_data_extract_hdu(hdul: fits.HDUList) -> fits.PrimaryHDU | fits.CompImageHDU:
        """Return the fits hdu associated with the data in the hdu list."""
        if hdul[0].data is not None:
            return hdul[0]
        return hdul[1]

    @staticmethod
    def fits_data_open(path: str | Path) -> fits.HDUList:
        """Return the fits object for the given path."""
        return fits.open(path)

    def fits_data_write(
        self,
        hdu_list: fits.HDUList,
        tags: tag_type_hint,
        relative_path: Path | str | None = None,
        overwrite: bool = False,
    ) -> Path:
        """Write the fits object to a file with the given path and tag with the given tags."""
        file_obj = BytesIO()
        hdu_list.writeto(file_obj, checksum=True)
        file_obj.seek(0)
        return self.write(
            file_obj=file_obj, tags=tags, relative_path=relative_path, overwrite=overwrite
        )
