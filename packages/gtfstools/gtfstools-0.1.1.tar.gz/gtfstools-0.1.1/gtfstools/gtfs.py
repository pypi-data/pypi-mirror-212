from csv import DictReader, DictWriter
from dataclasses import dataclass, field, fields
from io import TextIOWrapper
from typing import Any, Dict, List, Optional
from zipfile import ZIP_DEFLATED, ZipFile

from gtfstools.agency import Agency
from gtfstools.calendar import Service
from gtfstools.calendar_dates import ServiceChange
from gtfstools.helpers import RecordBase
from gtfstools.routes import Route
from gtfstools.stop_times import StopTime
from gtfstools.stops import Stop
from gtfstools.trips import Trip

GTFS_DATASET_MAPPINGS: List[Dict[str, Any]] = [
    {'filename': 'agency.txt', 'fieldname': 'agencies', 'class': Agency},
    {'filename': 'stops.txt', 'fieldname': 'stops', 'class': Stop},
    {'filename': 'routes.txt', 'fieldname': 'routes', 'class': Route},
    {'filename': 'calendar.txt', 'fieldname': 'services', 'class': Service},
    {'filename': 'calendar_dates.txt', 'fieldname': 'service_changes',
     'class': ServiceChange},
    {'filename': 'trips.txt', 'fieldname': 'trips', 'class': Trip},
    {'filename': 'stop_times.txt', 'fieldname': 'stop_times',
     'class': StopTime},
]


@dataclass
class GTFS:
    agencies: List[Agency]
    stops: List[Stop]
    routes: List[Route]
    trips: List[Trip]
    stop_times: List[StopTime]

    services: List[Service] = field(default_factory=list)
    service_changes: List[ServiceChange] = field(default_factory=list)


def read(path: str) -> GTFS:
    context: Dict[str, Any] = {}
    gtfs_fields: Dict[str, List[RecordBase]] = {}
    with ZipFile(path, 'r') as gtfs_file:
        for mapping in GTFS_DATASET_MAPPINGS:
            if mapping['filename'] not in gtfs_file.namelist():
                continue
            data = []
            with gtfs_file.open(mapping['filename'], 'r') as data_file:
                data_file_wrapper = TextIOWrapper(data_file, encoding='utf-8')
                reader = DictReader(data_file_wrapper)
                for row in reader:
                    data.append(mapping['class'](row, context))
            gtfs_fields[mapping['fieldname']] = data
    return GTFS(**gtfs_fields)  # type: ignore


def write(path: str, gtfs: GTFS, compression: int = ZIP_DEFLATED,
          compresslevel: Optional[int] = None) -> None:
    with ZipFile(path, 'w', compression=compression,
                 compresslevel=compresslevel) as gtfs_file:
        for mapping in GTFS_DATASET_MAPPINGS:
            if len(getattr(gtfs, mapping['fieldname'])) == 0:
                continue

            with gtfs_file.open(mapping['filename'], 'w') as data_file:
                data_file_wrapper = TextIOWrapper(data_file, encoding='utf-8',
                                                  write_through=True)
                fieldnames = [field.name for field in fields(mapping['class'])]
                writer = DictWriter(data_file_wrapper, fieldnames=fieldnames)
                writer.writeheader()

                records = getattr(gtfs, mapping['fieldname'])
                records.sort()
                for record in records:
                    writer.writerow(record.asdict())
