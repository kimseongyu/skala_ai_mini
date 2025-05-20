from abc import ABC, abstractmethod
from typing import Dict, Any
from utils.data_manager import DataManager


class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.data_manager = DataManager()

    @abstractmethod
    def save_state(self, state: Dict[str, Any], data: Any) -> None:
        """Save the state to the data manager"""
        pass

    @abstractmethod
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's main logic"""
        pass

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Main execution flow with data persistence"""
        latest_data = self.data_manager.get_latest_agent_output(self.name)
        if self.save_state(state, latest_data):
            print(f"Skipping {self.name} as data from today already exists")
            return state

        result, data = self.execute(state)
        self.data_manager.save_agent_output(self.name, data)
        return result
