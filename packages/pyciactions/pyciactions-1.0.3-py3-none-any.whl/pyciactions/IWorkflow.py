from abc import ABC, abstractmethod
from typing import Dict

class IWorkflow(ABC):
    @abstractmethod
    def to_dict(self) -> Dict:
        pass