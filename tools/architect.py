#!/usr/bin/env python3
"""
Skills Tree OS - Agent Skill Architect

Executable intelligence platform for generating agentic architecture blueprints.
Implements recommendation engine, graph query logic, and blueprint generation.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any


class SkillsGraph:
    """Load and query the skills knowledge graph"""
    
    def __init__(self, graph_path: str = "../data/SKILLS_GRAPH.json"):
        with open(graph_path, 'r') as f:
            self.data = json.load(f)
        self.nodes = {n['id']: n for n in self.data['nodes']}
        self.edges = self.data['edges']
    
    def get_node(self, node_id: str) -> Dict:
        return self.nodes.get(node_id)
    
    def get_dependencies(self, node_id: str, edge_type: str = "REQUIRES") -> List[Dict]:
        """Get all nodes connected via specific edge type"""
        deps = []
        for edge in self.edges:
            if edge['source'] == node_id and edge['type'] == edge_type:
                target = self.get_node(edge['target'])
                if target:
                    deps.append({**target, 'confidence': edge['confidence']})
        return deps
    
    def get_recommendations(self, node_id: str) -> List[Dict]:
        return self.get_dependencies(node_id, "RECOMMENDED_WITH")
    
    def get_learning_path(self, goal_skills: List[str]) -> List[str]:
        """Generate a learning path based on LEARN_BEFORE edges"""
        path = []
        visited = set()
        
        def traverse(skill_id):
            if skill_id in visited:
                return
            visited.add(skill_id)
            
            # Get prerequisites
            prereqs = self.get_dependencies(skill_id, "LEARN_BEFORE")
            for prereq in prereqs:
                traverse(prereq['id'])
            
            if skill_id not in path:
                path.append(skill_id)
        
        for skill in goal_skills:
            traverse(skill)
        
        return path


class RecommendationEngine:
    """Generate skill recommendations for agentic goals"""
    
    GOAL_MAPPINGS = {
        "Coding Agent": {
            "required": ["skill:code-generation", "skill:prompt-engineering"],
            "optional": ["skill:function-calling"],
            "deployment": "local",
            "complexity": "Medium"
        },
        "Browser Agent": {
            "required": ["skill:browser-automation", "skill:error-recovery"],
            "optional": ["skill:web-scraping", "skill:data-extraction"],
            "deployment": "cloud",
            "complexity": "High"
        },
        "RAG Assistant": {
            "required": ["skill:rag-retrieval", "skill:vector-search", "skill:embedding-generation"],
            "optional": ["skill:context-management"],
            "deployment": "cloud",
            "complexity": "Medium"
        },
        "Research Agent": {
            "required": ["skill:web-scraping", "skill:data-extraction"],
            "optional": ["skill:llm-orchestration"],
            "deployment": "cloud",
            "complexity": "Medium"
        },
        "Multi-Agent System": {
            "required": ["skill:multi-agent-coordination", "skill:llm-orchestration", "skill:context-management"],
            "optional": ["skill:workflow-automation"],
            "deployment": "cloud",
            "complexity": "Expert"
        }
    }
    
    def __init__(self, graph: SkillsGraph):
        self.graph = graph
    
    def recommend(self, goal: str) -> Dict[str, Any]:
        """Generate recommendations for a goal"""
        if goal not in self.GOAL_MAPPINGS:
            return {"error": f"Unknown goal: {goal}. Available: {list(self.GOAL_MAPPINGS.keys())}"}
        
        mapping = self.GOAL_MAPPINGS[goal]
        required_skills = [self.graph.get_node(sid) for sid in mapping["required"]]
        optional_skills = [self.graph.get_node(sid) for sid in mapping["optional"]]
        
        # Expand dependencies
        all_dependencies = []
        for skill in required_skills:
            deps = self.graph.get_dependencies(skill['id'])
            all_dependencies.extend(deps)
        
        # Generate learning path
        all_skill_ids = mapping["required"] + mapping["optional"]
        learning_path = self.graph.get_learning_path(all_skill_ids)
        
        # Calculate confidence
        confidence = self._calculate_confidence(required_skills, all_dependencies)
        
        return {
            "required_skills": required_skills,
            "optional_skills": optional_skills,
            "dependencies": all_dependencies,
            "learning_path": [self.graph.get_node(sid) for sid in learning_path],
            "confidence_score": confidence,
            "deployment": mapping["deployment"],
            "complexity": mapping["complexity"]
        }
    
    def _calculate_confidence(self, skills: List[Dict], dependencies: List[Dict]) -> float:
        """Calculate confidence based on graph coverage"""
        if not skills:
            return 0.0
        
        # Base confidence from skill stability
        stable_count = sum(1 for s in skills if s.get('stability') == 'stable')
        base = stable_count / len(skills)
        
        # Boost from well-defined dependencies
        dep_boost = min(len(dependencies) * 0.05, 0.2)
        
        return min(base + dep_boost, 1.0)


class BlueprintGenerator:
    """Generate architecture blueprints from recommendations"""
    
    RISK_LIBRARY = {
        "Code Generation": [
            {"severity": "Major", "probability": "Medium", "mitigation": "Implement code review and testing"}
        ],
        "Browser Automation": [
            {"severity": "Major", "probability": "High", "mitigation": "Add retry logic and error handling"},
            {"severity": "Minor", "probability": "High", "mitigation": "Handle dynamic UI changes"}
        ],
        "RAG Retrieval": [
            {"severity": "Major", "probability": "Medium", "mitigation": "Validate retrieval accuracy"},
            {"severity": "Critical", "probability": "Low", "mitigation": "Monitor for hallucinations"}
        ]
    }
    
    def generate(self, goal: str, recommendation: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a complete architecture blueprint"""
        
        # Collect risks
        risks = []
        for skill in recommendation['required_skills']:
            skill_name = skill['name']
            if skill_name in self.RISK_LIBRARY:
                risks.extend(self.RISK_LIBRARY[skill_name])
        
        blueprint = {
            "$schema": "https://skillstree.os/schemas/v1/blueprint.json",
            "id": f"blueprint-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "title": goal,
            "goal": goal,
            "description": f"Architecture blueprint for {goal}",
            "confidence_score": recommendation['confidence_score'],
            "generated_at": datetime.now().isoformat(),
            "architecture_type": self._infer_architecture_type(goal),
            "deployment_type": recommendation.get('deployment', 'cloud'),
            "complexity": recommendation.get('complexity', 'Medium'),
            "maturity": "Alpha",
            "required_skills": [
                {
                    "id": s['id'],
                    "name": s['name'],
                    "priority": "Critical" if i < 2 else "High",
                    "rationale": f"Core capability for {goal}",
                    "learn_time": f"{10 + i*5} hours"
                }
                for i, s in enumerate(recommendation['required_skills'])
            ],
            "optional_skills": [
                {"id": s['id'], "name": s['name']} 
                for s in recommendation['optional_skills']
            ],
            "dependencies": [
                {"name": d['name'], "confidence": d.get('confidence', 0.0)}
                for d in recommendation['dependencies']
            ],
            "learning_path": [
                s['name'] for s in recommendation['learning_path']
            ],
            "risks": risks
        }
        
        return blueprint
    
    def _infer_architecture_type(self, goal: str) -> str:
        mapping = {
            "Coding Agent": "Single-Agent",
            "Browser Agent": "Single-Agent",
            "RAG Assistant": "RAG",
            "Multi-Agent System": "Multi-Agent"
        }
        return mapping.get(goal, "Single-Agent")


def print_blueprint(blueprint: Dict[str, Any]):
    """Pretty-print a blueprint to console"""
    print(f"\n{'='*70}")
    print(f"ARCHITECTURE BLUEPRINT: {blueprint['title']}")
    print(f"{'='*70}")
    print(f"\nID: {blueprint['id']}")
    print(f"Confidence Score: {blueprint['confidence_score']:.2f}")
    print(f"Architecture Type: {blueprint['architecture_type']}")
    print(f"Deployment: {blueprint['deployment_type']}")
    print(f"Complexity: {blueprint['complexity']}")
    print(f"Maturity: {blueprint['maturity']}")
    
    print(f"\n{'─'*70}")
    print("REQUIRED SKILLS:")
    for skill in blueprint['required_skills']:
        print(f"  • {skill['name']} (Priority: {skill['priority']}, Learn Time: {skill['learn_time']})")
        print(f"    Rationale: {skill['rationale']}")
    
    if blueprint['optional_skills']:
        print(f"\n{'─'*70}")
        print("OPTIONAL SKILLS:")
        for skill in blueprint['optional_skills']:
            print(f"  • {skill['name']}")
    
    if blueprint['dependencies']:
        print(f"\n{'─'*70}")
        print("DEPENDENCIES:")
        for dep in blueprint['dependencies']:
            print(f"  • {dep['name']} (Confidence: {dep['confidence']:.2f})")
    
    print(f"\n{'─'*70}")
    print("LEARNING PATH:")
    for i, skill in enumerate(blueprint['learning_path'], 1):
        print(f"  {i}. {skill}")
    
    if blueprint['risks']:
        print(f"\n{'─'*70}")
        print("RISKS:")
        for risk in blueprint['risks']:
            print(f"  ⚠️  [{risk['severity']}] Probability: {risk['probability']}")
            print(f"      Mitigation: {risk['mitigation']}")
    
    print(f"\n{'='*70}\n")


def main():
    """Main entry point for Skills Tree Architect"""
    print("\n🌳 Skills Tree OS - Agent Skill Architect")
    print("Transform goals into executable architectures\n")
    
    # Initialize systems
    script_dir = os.path.dirname(os.path.abspath(__file__))
    graph_path = os.path.join(script_dir, "..", "data", "SKILLS_GRAPH.json")
    
    try:
        graph = SkillsGraph(graph_path)
        engine = RecommendationEngine(graph)
        generator = BlueprintGenerator()
    except FileNotFoundError:
        print(f"❌ Error: Could not find {graph_path}")
        print("Make sure SKILLS_GRAPH.json exists in the data/ directory.")
        return
    
    # Interactive prompt
    print("Available Goals:")
    for goal in engine.GOAL_MAPPINGS.keys():
        print(f"  • {goal}")
    
    print("\nWhat do you want to build?")
    user_goal = input("> ").strip()
    
    if not user_goal:
        print("No goal provided. Exiting.")
        return
    
    # Generate recommendation
    print(f"\n⚙️  Analyzing architecture for: {user_goal}...")
    recommendation = engine.recommend(user_goal)
    
    if "error" in recommendation:
        print(f"❌ {recommendation['error']}")
        return
    
    # Generate blueprint
    blueprint = generator.generate(user_goal, recommendation)
    
    # Display
    print_blueprint(blueprint)
    
    # Save to file
    output_path = f"blueprint_{blueprint['id']}.json"
    with open(output_path, 'w') as f:
        json.dump(blueprint, f, indent=2)
    
    print(f"✅ Blueprint saved to: {output_path}")


if __name__ == "__main__":
    main()
