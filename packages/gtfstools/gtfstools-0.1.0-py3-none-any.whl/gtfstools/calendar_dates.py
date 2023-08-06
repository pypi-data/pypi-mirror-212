from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict, Tuple

from gtfstools.helpers import DATE_FORMAT, RecordBase, get_id


@dataclass(eq=False)
class ServiceChange(RecordBase):
    service_id: int
    date: date
    exception_type: int

    def __init__(self, values: Dict[str, str], context: Dict[str, Any]):
        service_id_map = context.setdefault('service_id_map', {})
        self.service_id = get_id(service_id_map, values['service_id'])
        self.date = datetime.strptime(values['date'], DATE_FORMAT).date()
        self.exception_type = int(values['exception_type'])

    def primary(self) -> Tuple[int, int]:
        return self.service_id, \
            int(datetime.combine(self.date, datetime.min.time()).timestamp())

    def asdict(self) -> Dict[str, Any]:
        return {
            'service_id': self.service_id,
            'date': self.date.strftime(DATE_FORMAT),
            'exception_type': self.exception_type,
        }
