"""
Team A - Analysis Agent
Analyzes incoming requests and determines execution strategy
"""
from app.agents.base_agent import BaseAgent
from typing import Dict, Any, List

class AnalyzerAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Analyzer", team="A")

    async def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze data and create execution plan"""
        # Analyze the incoming data and determine appropriate actions
        analysis_result = {
            "status": "analyzed",
            "confidence": 0.95,
            "data_type": self._identify_data_type(data),
            "required_agents": self._identify_required_agents(data),
            "execution_plan": self._create_execution_plan(data),
            "priority": self._determine_priority(data),
            "risk_level": self._assess_risk_level(data)
        }

        return analysis_result

    def _identify_data_type(self, data: Dict[str, Any]) -> str:
        """Identify the type of data to be processed"""
        if "security_event" in data:
            return "security_event"
        elif "code_analysis" in data:
            return "code_analysis"
        elif "threat_intel" in data:
            return "threat_intel"
        elif "vulnerability_scan" in data:
            return "vulnerability_scan"
        else:
            return "general_task"

    def _identify_required_agents(self, data: Dict[str, Any]) -> List[str]:
        """Identify which agents are required to process this data"""
        required_agents = ["Analyzer"]

        data_type = self._identify_data_type(data)
        if data_type == "security_event":
            required_agents.extend(["ThreatDetector", "IncidentResponder"])
        elif data_type == "code_analysis":
            required_agents.extend(["CodeScanner", "VulnerabilityAnalyzer"])
        elif data_type == "threat_intel":
            required_agents.extend(["ThreatIntelligence", "RiskAssessor"])
        elif data_type == "vulnerability_scan":
            required_agents.extend(["VulnerabilityScanner", "RemediationAgent"])
        else:
            required_agents.append("DefaultProcessor")

        return required_agents

    def _create_execution_plan(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create an execution plan based on the data"""
        data_type = self._identify_data_type(data)

        execution_plan = {
            "data_type": data_type,
            "agents": self._identify_required_agents(data),
            "steps": [],
            "dependencies": [],
            "estimated_completion": "medium"
        }

        # Define steps based on data type
        if data_type == "security_event":
            execution_plan["steps"] = [
                {"id": 1, "action": "classify_event", "required_agent": "ThreatDetector"},
                {"id": 2, "action": "assess_impact", "required_agent": "RiskAssessor"},
                {"id": 3, "action": "contain_threat", "required_agent": "IncidentResponder"},
                {"id": 4, "action": "remediate", "required_agent": "RemediationAgent"}
            ]
        elif data_type == "code_analysis":
            execution_plan["steps"] = [
                {"id": 1, "action": "scan_code", "required_agent": "CodeScanner"},
                {"id": 2, "action": "identify_vulnerabilities", "required_agent": "VulnerabilityAnalyzer"},
                {"id": 3, "action": "generate_report", "required_agent": "Reporter"},
                {"id": 4, "action": "recommend_fixes", "required_agent": "FixRecommender"}
            ]
        else:
            execution_plan["steps"] = [
                {"id": 1, "action": "process_data", "required_agent": "DefaultProcessor"},
                {"id": 2, "action": "generate_output", "required_agent": "DefaultProcessor"}
            ]

        return execution_plan

    def _determine_priority(self, data: Dict[str, Any]) -> str:
        """Determine the priority of the task"""
        # Check for urgency indicators in the data
        if data.get("urgent", False) or data.get("priority") == "high":
            return "high"
        elif data.get("severity", "").lower() in ["critical", "high"]:
            return "high"
        elif data.get("severity", "").lower() in ["medium", "moderate"]:
            return "medium"
        else:
            return "low"

    def _assess_risk_level(self, data: Dict[str, Any]) -> str:
        """Assess the risk level based on data content"""
        # Assess risk based on data features
        if "critical_vulnerability" in str(data).lower() or \
           data.get("severity", "").lower() in ["critical", "emergency"]:
            return "critical"
        elif "high" in str(data).lower() or data.get("severity", "").lower() == "high":
            return "high"
        elif "medium" in str(data).lower() or data.get("severity", "").lower() == "medium":
            return "medium"
        else:
            return "low"
