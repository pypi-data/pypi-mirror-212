from dataclasses import dataclass
from typing import Union
import empaquetadas.samples as samples  # noqa


@dataclass
class Converter:
    records: dict[str, float]

    def change_factor(self, initial_record: str, final_record: str) -> float:
        return self.records[final_record] / self.records[initial_record]


def get_change_in_time(
    initial_value: float,
    initial_record: str,
    final_record: str,
    converter: Union[Converter, list[Converter]],
) -> float:
    final_value = initial_value
    converter = [converter] if isinstance(converter, Converter) else converter
    for conv in converter:
        final_value *= conv.change_factor(initial_record, final_record)
    return final_value
