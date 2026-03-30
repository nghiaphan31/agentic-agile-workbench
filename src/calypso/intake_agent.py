"""
Intake Agent — Enhanced intake processing with complexity scoring

Routes incoming ideas to the appropriate backlog and determines
refinement complexity score for routing decisions.

Usage:
    from intake_agent import IntakeAgent
    agent = IntakeAgent()
    result = agent.process_intake(raw_text)
    print(result.routing, result.complexity_score)
"""

import re
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class RoutingTarget(Enum):
    """Where to route the intake"""
    IDEAS_BACKLOG = "IDEAS_BACKLOG"  # Business requirements
    TECH_SUGGESTIONS_BACKLOG = "TECH_SUGGESTIONS_BACKLOG"  # Technical suggestions
    ORCHESTRATOR = "ORCHESTRATOR"  # Complex or ambiguous
    DEFER = "DEFER"  # Not enough info


class RefinementMode(Enum):
    """How to refine the idea"""
    ASYNC = "ASYNC"  # Agent works independently, human reviews
    SYNC = "SYNC"  # Real-time collaboration session
    HYBRID = "HYBRID"  # Combination approach


@dataclass
class IntakeResult:
    """Result of processing an intake"""
    routing: RoutingTarget
    complexity_score: int  # 1-10
    refinement_mode: RefinementMode
    idea_type: str  # BUSINESS or TECHNICAL
    idea_title: str
    idea_description: str
    suggested_id: Optional[str] = None
    confidence: float = 0.5  # 0.0-1.0
    warnings: list = None
    
    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


class ComplexityScorer:
    """
    Scores idea complexity to determine refinement approach.
    
    Based on PLAN-ideation-to-release-full-process.md:
    - Score 1-3: ASYNC refinement
    - Score 4-6: HYBRID refinement  
    - Score 7-10: SYNC refinement
    """
    
    # Indicators that increase complexity
    COMPLEXITY_INDICATORS = {
        # Technical complexity
        "api": 2,
        "database": 2,
        "authentication": 3,
        "migration": 3,
        "refactor": 2,
        "performance": 2,
        "security": 3,
        "scalability": 2,
        "distributed": 3,
        "microservice": 3,
        
        # Scope indicators
        "multiple": 2,
        "several": 1,
        "across": 2,
        "integration": 2,
        "dependency": 2,
        "cross-cutting": 3,
        
        # Ambiguity indicators (increase complexity due to unclear requirements)
        "maybe": 1,
        "possibly": 1,
        "either": 1,
        "or": 1,
        "unclear": 2,
        "maybe": 1,
        "not sure": 2,
        "flexible": 1,
        
        # Impact indicators
        "breaking": 3,
        "affects": 2,
        "impact": 2,
        "risk": 2,
    }
    
    @classmethod
    def score(cls, text: str) -> int:
        """
        Calculate complexity score (1-10) for a piece of text.
        
        Args:
            text: The raw idea text
            
        Returns:
            Complexity score from 1 to 10
        """
        text_lower = text.lower()
        score = 1  # Start with minimum
        
        # Check each indicator
        for indicator, weight in cls.COMPLEXITY_INDICATORS.items():
            if indicator in text_lower:
                score += weight
        
        # Cap at 10
        return min(score, 10)
    
    @classmethod
    def determine_mode(cls, complexity: int) -> RefinementMode:
        """
        Determine refinement mode based on complexity score.
        
        Args:
            complexity: Score from 1-10
            
        Returns:
            Recommended RefinementMode
        """
        if complexity <= 3:
            return RefinementMode.ASYNC
        elif complexity <= 6:
            return RefinementMode.HYBRID
        else:
            return RefinementMode.SYNC


class IntakeAgent:
    """
    Enhanced intake agent that routes ideas and scores complexity.
    
    Responsibilities:
    1. Classify idea as BUSINESS or TECHNICAL
    2. Route to appropriate backlog
    3. Calculate complexity score
    4. Determine refinement mode
    """
    
    # Patterns for identifying idea type
    TECHNICAL_PATTERNS = [
        r"\b(architecture|technical|deployment|infrastructure|api|performance|scalability|security|refactor)\b",
        r"\b(python|javascript|typescript|java|rust|golang|sql|nosql|database|cache)\b",
        r"\b(github|gitlab|jenkins|ci/cd|pipeline|deploy|docker|kubernetes|cloud)\b",
        r"\b(microservice|monolith|distributed|api|endpoint|integration)\b",
        r"\b(library|framework|tool|utility|script|automate)\b",
    ]
    
    BUSINESS_PATTERNS = [
        r"\b(user|customer|product|feature|requirement|usecase|workflow)\b",
        r"\b(UX|UI|design|interface|dashboard|report|analytics)\b",
        r"\b(workflow|automation|business process|stakeholder)\b",
        r"\b(market|revenue|growth|adoption|engagement)\b",
    ]
    
    def __init__(self):
        self.scorer = ComplexityScorer()
    
    def process_intake(self, raw_text: str) -> IntakeResult:
        """
        Process a raw idea input and determine routing.
        
        Args:
            raw_text: The raw idea, request, or remark
            
        Returns:
            IntakeResult with routing and complexity info
        """
        warnings = []
        
        # Clean the text
        cleaned = self._clean_text(raw_text)
        
        # Classify as BUSINESS or TECHNICAL
        idea_type = self._classify(cleaned)
        
        # Determine routing
        routing = self._determine_routing(idea_type, cleaned, warnings)
        
        # Calculate complexity
        complexity = self.scorer.score(cleaned)
        refinement_mode = self.scorer.determine_mode(complexity)
        
        # Extract title
        title = self._extract_title(cleaned)
        
        return IntakeResult(
            routing=routing,
            complexity_score=complexity,
            refinement_mode=refinement_mode,
            idea_type=idea_type,
            idea_title=title,
            idea_description=cleaned,
            warnings=warnings,
        )
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize input text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove common prefixes
        text = re.sub(r'^(hello|hi|hey|so |thus |actually |basically ),', '', text, flags=re.IGNORECASE)
        return text.strip()
    
    def _classify(self, text: str) -> str:
        """
        Classify idea as BUSINESS or TECHNICAL.
        
        Returns:
            "BUSINESS" or "TECHNICAL"
        """
        text_lower = text.lower()
        
        tech_matches = sum(1 for p in self.TECHNICAL_PATTERNS if re.search(p, text_lower))
        biz_matches = sum(1 for p in self.BUSINESS_PATTERNS if re.search(p, text_lower))
        
        if tech_matches > biz_matches:
            return "TECHNICAL"
        elif biz_matches > tech_matches:
            return "BUSINESS"
        else:
            # Default to business for ambiguous cases
            return "BUSINESS"
    
    def _determine_routing(self, idea_type: str, text: str, warnings: list) -> RoutingTarget:
        """
        Determine where to route the idea.
        
        Args:
            idea_type: BUSINESS or TECHNICAL
            text: Cleaned text
            warnings: List to append warnings to
            
        Returns:
            RoutingTarget enum value
        """
        text_lower = text.lower()
        
        # Check for off-topic or unclear inputs
        if len(text) < 20:
            warnings.append("Input is very short — may lack sufficient detail")
            return RoutingTarget.ORCHESTRATOR
        
        # Check for multiple ideas in one input
        idea_count = len(re.findall(r'\b(also|and|plus|another|additionally)\b', text_lower))
        if idea_count > 2:
            warnings.append("Multiple ideas detected — may need to be split")
        
        # Route based on type
        if idea_type == "TECHNICAL":
            # Check if it's really a tech suggestion vs vague tech talk
            if any(p in text_lower for p in ["could we", "should we", "maybe", "perhaps", "might be"]):
                return RoutingTarget.TECH_SUGGESTIONS_BACKLOG
            elif any(p in text_lower for p in ["need to", "must", "require", "critical", "bug", "fix"]):
                return RoutingTarget.ORCHESTRATOR  # Needs refinement
            else:
                return RoutingTarget.TECH_SUGGESTIONS_BACKLOG
        else:
            return RoutingTarget.IDEAS_BACKLOG
    
    def _extract_title(self, text: str, max_length: int = 60) -> str:
        """
        Extract a title from the text.
        
        Args:
            text: Cleaned text
            max_length: Maximum title length
            
        Returns:
            Extracted title
        """
        # Take first sentence or phrase
        title = text.split('.')[0].split('!')[0].split('?')[0]
        
        # If it looks like a full sentence, try to find noun phrase
        if len(title) > max_length:
            # Find first comma or dash split
            for sep in [',', ' - ', ' -- ', ':']:
                if sep in title:
                    title = title.split(sep)[0]
                    break
        
        # Truncate if still too long
        if len(title) > max_length:
            title = title[:max_length-3] + "..."
        
        return title.strip()
    
    def generate_idea_file(self, result: IntakeResult, next_id: str) -> dict:
        """
        Generate the frontmatter and content for a new idea file.
        
        Args:
            result: The intake processing result
            next_id: The next available IDEA number (e.g., "013")
            
        Returns:
            Dictionary with content and metadata
        """
        idea_id = f"IDEA-{next_id}"
        
        frontmatter = [
            "---",
            f"id: {idea_id}",
            f"title: {result.idea_title}",
            f"status: [IDEA]",
            f"type: {result.idea_type}",
            f"complexity_score: {result.complexity_score}",
            f"refinement_mode: {result.refinement_mode.value}",
            f"intake_date: {datetime.now().date().isoformat()}",
            "---",
            "",
        ]
        
        body = [
            f"## {result.idea_title}",
            "",
            "## Description",
            "",
            result.idea_description,
            "",
            "## Motivation",
            "",
            "_Why is this needed? What problem does it solve?_",
            "",
            "## Affected Documents",
            "",
            "- [ ] DOC-1 (PRD)",
            "- [ ] DOC-2 (Architecture)",
            "- [ ] DOC-3 (Implementation Plan)",
            "",
            "## Dependencies",
            "",
            "_Any dependencies on other ideas or deliverables?_",
            "",
            "## Verification",
            "",
            "- [ ] Criteria 1",
            "- [ ] Criteria 2",
            "",
            "## History",
            "",
            f"- {datetime.now().date().isoformat()}: Captured via Intake Agent (complexity={result.complexity_score})",
        ]
        
        return {
            "idea_id": idea_id,
            "content": "\n".join(frontmatter + body),
            "frontmatter": "\n".join(frontmatter),
        }


def main():
    """CLI for testing the intake agent"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python intake_agent.py <idea text>")
        print("Example: python intake_agent.py 'We should add a dashboard for analytics'")
        sys.exit(1)
    
    agent = IntakeAgent()
    text = " ".join(sys.argv[1:])
    result = agent.process_intake(text)
    
    print("=" * 50)
    print("INTAKE AGENT RESULT")
    print("=" * 50)
    print(f"Routing:        {result.routing.value}")
    print(f"Idea Type:      {result.idea_type}")
    print(f"Complexity:     {result.complexity_score}/10")
    print(f"Refinement:     {result.refinement_mode.value}")
    print(f"Title:          {result.idea_title}")
    print(f"Confidence:     {result.confidence:.0%}")
    if result.warnings:
        print(f"Warnings:       {', '.join(result.warnings)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
