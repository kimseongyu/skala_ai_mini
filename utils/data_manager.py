import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional


class DataManager:
    def __init__(self, base_dir: str = "./data"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def save_agent_output(self, agent_name: str, data: Dict[str, Any]) -> str:
        """Save agent output with timestamp"""
        filepath = os.path.join(self.base_dir, agent_name)
        os.makedirs(os.path.join(self.base_dir, agent_name), exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}.json"
        filepath = os.path.join(filepath, filename)

        output = {"timestamp": timestamp, "data": data}

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        return filepath

    def get_latest_agent_output(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get the latest output from an agent if it exists and is from today"""
        agent_dir = os.path.join(self.base_dir, agent_name)
        if not os.path.exists(agent_dir):
            return None

        files = [f for f in os.listdir(agent_dir) if f.endswith(".json")]
        if not files:
            return None

        latest_file = max(files)
        filepath = os.path.join(agent_dir, latest_file)

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Check if the data is from today
        timestamp = datetime.strptime(data["timestamp"], "%Y%m%d_%H%M%S")
        if timestamp.date() == datetime.now().date():
            return data["data"]

        return None
