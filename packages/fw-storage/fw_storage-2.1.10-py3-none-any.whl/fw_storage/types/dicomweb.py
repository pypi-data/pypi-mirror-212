"""DICOM web storage module."""
import tempfile
import typing as t
from pathlib import Path

import urllib3
from fw_http_client import ClientError, HttpClient
from fw_utils import Filters, fileglob
from pydicom.dataset import Dataset

from .. import __version__
from ..config import DICOMWebConfig
from ..fileinfo import FileInfo
from ..storage import AnyPath
from .dicom import DICOMBase, apply_exclude_filters, parse_filters_to_dict, parse_path

__all__ = ["DICOMWebStorage"]

client_info = {"client_name": "fw-storage", "client_version": __version__}


class DICOMWebStorage(DICOMBase):
    """Storage class for web-based medical imaging."""

    def __init__(
        self, config: DICOMWebConfig, headers: t.Dict[str, str] = None
    ) -> None:
        """Construct DICOM web storage.

        Args:
            config: DICOMConfig
            headers: dict
        """
        self.config = config
        self.client = DICOMwebClient(
            baseurl=self.config.api_url,
            auth=self.config.auth,
            headers=headers or {},
            **client_info,
        )

    def fullpath(self, path: AnyPath) -> str:  # pragma: no cover
        """Return absolute path string including the storage URL."""
        return f"dicomweb://TODO/{path}"

    def ls(
        self,
        path: AnyPath = "",
        *,
        include: Filters = None,
        exclude: Filters = None,
        **_,
    ) -> t.Iterator[FileInfo]:
        """Yield items under path that match the include/exclude filters."""
        query: dict = {
            "includefield": [
                "NumberOfSeriesRelatedInstances",
                "SeriesDate",
                "SeriesTime",
            ]
        }
        study_uid, series_uid = parse_path(path, required_parts=0)
        if include:
            inc_filters = parse_filters_to_dict(include)
            query.update(inc_filters)
        if exclude:
            exc_filters = parse_filters_to_dict(exclude)
            query["includefield"].extend(list(exc_filters.keys()))
        # TODO: Series level ls might be unnecessary, see stat method
        if study_uid and series_uid:
            query.update({"SeriesInstanceUID": series_uid})
            result = self.client.qido(f"/studies/{study_uid}/series", params=query)
            if result:
                if exclude and apply_exclude_filters(result[0], exc_filters):
                    return
                yield self.result_to_fileinfo(result[0])
            return
        if study_uid:
            study_uids = [study_uid]
        else:
            study_uids = [ds.StudyInstanceUID for ds in self.client.qido("/studies")]
        for study_uid in study_uids:
            for ds in self.client.qido(f"/studies/{study_uid}/series", params=query):
                if exclude and apply_exclude_filters(ds, exc_filters):
                    continue
                yield self.result_to_fileinfo(ds)

    def get(self, path: AnyPath, **kwargs) -> AnyPath:  # type: ignore
        """Return a path pointing to the downloaded series."""
        study_uid, series_uid = parse_path(path, required_parts=2)
        parts = self.client.wado(f"/studies/{study_uid}/series/{series_uid}")
        tmp = Path(tempfile.gettempdir()) / self.abspath(path)
        tmp.mkdir(parents=True, exist_ok=True)
        for index, part in enumerate(parts):
            with open(f"{tmp}/{index + 1:05}.dcm", "wb") as f:
                f.write(part.content)
        return str(tmp)

    def set(self, file: AnyPath) -> None:  # type: ignore
        """Write a file at the given path in storage."""
        path = Path(self.abspath(file))
        paths = []
        if path.is_dir():
            paths.extend(list(fileglob(path)))
        else:
            paths.append(path)
        boundary = urllib3.filepost.choose_boundary()
        headers = {
            "Content-Type": (
                "multipart/related; " "type=application/dicom; " f"boundary={boundary}"
            )
        }
        parts = get_instances_bytes(paths)
        content = multi_encode(parts, boundary)
        self.client.post("/studies", data=content, headers=headers)

    def rm(self, path: AnyPath, recurse: bool = False) -> None:
        """Remove file from storage."""
        # TODO: Performance can be better if we use SHA1 encoded UIDs
        # https://book.orthanc-server.com/faq/orthanc-ids.html
        series_path = self.abspath(path)
        study_uid, series_uid = parse_path(series_path, required_parts=1)
        try:
            self.client.delete_resource(study_uid, series_uid)
        except ClientError as exc:
            msg = "DICOM Web backend might not support delete operation on resources"
            raise ClientError(msg) from exc

    def stat(self, path: AnyPath) -> FileInfo:
        """Return FileInfo for a single series."""
        study_uid, series_uid = parse_path(path, required_parts=2)
        query: dict = {
            "SeriesInstanceUID": series_uid,
            "includefield": [
                "NumberOfSeriesRelatedInstances",
                "SeriesDate",
                "SeriesTime",
            ],
        }
        results = self.client.qido(f"/studies/{study_uid}/series", params=query)
        if len(results) == 1:
            return self.result_to_fileinfo(results[0])
        raise ValueError("Ambiguous resource or resource not found")

    def get_image_count(self, study_uid: str, series_uid: str) -> int:
        """Get image count of series."""
        result = self.client.qido(f"/studies/{study_uid}/series/{series_uid}/instances")
        return len(result)


class DICOMwebClient(HttpClient):
    """DICOM web client."""

    def qido(self, url, params=None):
        """Handle QIDO requests."""
        headers = {"Accept": "application/json"}
        response = super().get(url, raw=True, params=params, headers=headers)
        content_type = response.headers.get("Content-Type")
        datasets = []
        if content_type in ["application/json", "application/dicom+json"]:
            for ds in response.json():
                datasets.append(Dataset.from_json(ds))
        return datasets

    def wado(self, url):
        """Handle WADO requests."""
        headers = {"Accept": "multipart/related; type=application/dicom;"}
        response = super().get(url, stream=True, headers=headers)
        yield from response.iter_parts()

    def delete_resource(self, study_uid, series_uid=None):
        """Handle DELETE study/series requests."""
        url = self.baseurl.rstrip("/dicom-web")
        study = None
        for study_id in self.get(f"{url}/studies"):
            study = self.get(f"{url}/studies/{study_id}")
            if study.get("MainDicomTags").get("StudyInstanceUID") == study_uid:
                break
        if not study:
            raise ValueError("Resource not found")
        if series_uid:
            for series_id in study.get("Series"):
                series = self.get(f"{url}/series/{series_id}")
                uid = series.get("MainDicomTags").get("SeriesInstanceUID")
                if uid == series_uid:
                    self.delete(f"{url}/series/{series_id}")
        else:
            self.delete(f"{url}/studies/{study.get('ID')}")


def get_instances_bytes(paths: t.List[Path]) -> t.Iterator[bytes]:
    """Yield bytes of an instance from file."""
    for path in paths:
        yield path.read_bytes()


def multi_encode(
    parts: t.Iterator[bytes], boundary: str, encoding: str = "utf-8"
) -> t.Iterator[bytes]:
    """Yield HTTP multipart message parts."""
    b_crlf = "\r\n".encode(encoding)
    b_boundary = f"--{boundary}".encode(encoding)
    b_boundary_end = f"--{boundary}--".encode(encoding)
    b_media_type = "Content-Type: application/dicom".encode(encoding)
    b_part_header = b"".join([b_boundary, b_crlf, b_media_type, b_crlf, b_crlf])
    for part in parts:
        yield b"".join([b_part_header, part, b_crlf])
    yield b"".join([b_boundary_end, b_crlf, b_crlf])
