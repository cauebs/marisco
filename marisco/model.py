from dataclasses import dataclass
from typing import Optional, Union, Mapping, Iterable, Tuple


Params = Union[Mapping[str, str], Iterable[Tuple[str, str]]]


@dataclass
class Request:
    method: str
    url: str  # Union[str, yarl.URL]
    params: Optional[Params]
    # skip_auto_headers: Optional[Iterable[str]]
    # raise_for_status: bool = False
    # read_until_eof: bool = True
    # proxy: str  # Union[str, yarl.URL]
