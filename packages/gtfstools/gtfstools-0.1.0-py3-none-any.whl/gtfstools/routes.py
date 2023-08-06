from dataclasses import dataclass
from typing import Any, Dict, Optional

from gtfstools.helpers import RecordBase, get_id


@dataclass(eq=False)
class Route(RecordBase):
    route_id: int
    agency_id: int
    route_short_name: Optional[str]
    route_long_name: Optional[str]
    route_type: int

    def __init__(self, values: Dict[str, str], context: Dict[str, Any]):
        route_id_map = context.setdefault('route_id_map', {})
        agency_id_map = context['agency_id_map']
        self.route_id = get_id(route_id_map, values['route_id'])
        self.agency_id = agency_id_map.get(values['agency_id'])
        self.route_short_name = values.get('route_short_name', None)
        self.route_long_name = values.get('route_long_name', None)
        self.route_type = int(values['route_type'])

    def primary(self) -> int:
        return self.route_id
