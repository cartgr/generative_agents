import re
import json
from typing import List, Dict


def monitor_task_status(scenario_name: str, agent_name: str, completion_keywords: List[str]):
    def load_logs(file_path: str) -> List[Dict]:
        with open(file_path, 'r') as file:
            # logs = [json.loads(line) for line in file] # output is list
            logs = json.load(file) # output is dict
        return logs
    
    def check_task_completion(logs: Dict, subject: str, completion_keywords: List[str]) -> bool:
        """Check if a log entry indicates task completion for a specific subject."""
        if logs.get("subject") == subject:
            return all(re.search(keyword, logs.get("description", ""), re.IGNORECASE) for keyword in completion_keywords)
        return False
    
    def analyze_logs(logs: List[Dict], subject: str, completion_keywords: List[str]):
        """Analyze logs and summarize task status for each agent."""
        complection_nodes = []
        for node_id, entry in logs.items():
            if check_task_completion(entry, subject, completion_keywords):
                complection_nodes.append({
                    "node_id": node_id,
                    "description": entry['description']
                })
        if complection_nodes:
            print(f"Task completion logs for {subject}:")
            print("------------------------------------------------------")
            for node in complection_nodes:
                print(f"{node['node_id']}: {node['description']}")
            print("------------------------------------------------------")
            print(f"Total number of task completion nodes: {len(complection_nodes)}")
        else:
            print(f"No completion log found for {subject}'s task.")
    agent_memory_file = f"./environment/frontend_server/storage/{scenario_name}/personas/{agent_name}/bootstrap_memory/associative_memory/nodes.json"
    agent_memory = load_logs(agent_memory_file)
    analyze_logs(agent_memory, agent_name, completion_keywords)

monitor_task_status("Oct281119", "Isabella Rodriguez", ["potluck", "feedback"])
