from dataclasses import dataclass, field
from typing import List

@dataclass
class MessageCollector:
    messages: List[str] = field(default_factory=list)

    def collect(self, message: str) -> None:
        self.messages.append(message)

    def get_messages(self) -> List[str]:
        return self.messages