# This source code is part of the Biotite package and is distributed
# under the 3-Clause BSD License. Please see 'LICENSE.rst' for further
# information.

from typing import Optional
from abc import abstractmethod
from .application import Application


class WebApp(Application):
    def __init__(self, app_url: str, obey_rules: bool = True) -> None: ...
    def app_url(self) -> str: ...
    def violate_rule(self, msg: Optional[str] = None) -> None: ...
    @abstractmethod
    def run(self) -> None: ...
    @abstractmethod
    def is_finished(self) -> bool: ...
    @abstractmethod
    def wait_interval(self) -> float: ...
    @abstractmethod
    def evaluate(self) -> None: ...


class RuleViolationError(Exception):
    ...
