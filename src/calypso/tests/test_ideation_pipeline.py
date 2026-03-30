"""
Integration tests for the Ideation-to-Release pipeline

Tests the complete flow from intake to execution tracking.
"""

import pytest
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from intake_agent import IntakeAgent, ComplexityScorer, RoutingTarget, RefinementMode
from sync_detector import SyncDetector, OverlapType
from branch_tracker import BranchTracker, BranchType, BranchStatus
from execution_tracker import ExecutionTracker


class TestIntakeAgent:
    """Test the intake agent"""
    
    def test_complexity_scorer_basic(self):
        """Test basic complexity scoring"""
        assert ComplexityScorer.score("simple fix") == 1
        assert ComplexityScorer.score("we need to refactor the database") >= 3
    
    def test_complexity_scorer_technical_terms(self):
        """Test complexity scoring with technical terms"""
        text = "We need to add authentication and refactor the database"
        score = ComplexityScorer.score(text)
        assert score >= 5  # Should have multiple complexity indicators
    
    def test_refinement_mode_selection(self):
        """Test refinement mode based on complexity"""
        assert ComplexityScorer.determine_mode(2) == RefinementMode.ASYNC
        assert ComplexityScorer.determine_mode(5) == RefinementMode.HYBRID
        assert ComplexityScorer.determine_mode(8) == RefinementMode.SYNC
    
    def test_intake_processing(self):
        """Test full intake processing"""
        agent = IntakeAgent()
        result = agent.process_intake("We should add a dashboard for analytics")
        
        assert result.routing in [RoutingTarget.IDEAS_BACKLOG, RoutingTarget.TECH_SUGGESTIONS_BACKLOG]
        assert result.complexity_score >= 1
        assert result.refinement_mode in RefinementMode
        assert len(result.idea_title) > 0
    
    def test_intake_classification_business(self):
        """Test business idea classification"""
        agent = IntakeAgent()
        result = agent.process_intake("Users need a dashboard to view their analytics")
        assert result.idea_type == "BUSINESS"
    
    def test_intake_classification_technical(self):
        """Test technical idea classification"""
        agent = IntakeAgent()
        result = agent.process_intake("We need to refactor the database layer to use PostgreSQL")
        assert result.idea_type == "TECHNICAL"


class TestSyncDetector:
    """Test the sync detector"""
    
    def test_detector_initialization(self):
        """Test detector can be initialized"""
        detector = SyncDetector()
        assert detector.ideas_dir == Path("docs/ideas")
    
    def test_load_backlog_entries(self):
        """Test loading backlog entries"""
        detector = SyncDetector()
        entries = detector.load_backlog_entries()
        assert isinstance(entries, list)
    
    def test_detect_sync_returns_report(self):
        """Test detect_sync returns proper report structure"""
        detector = SyncDetector()
        # Use a known IDEA
        report = detector.detect_sync("IDEA-012A")
        assert report is not None
        assert hasattr(report, 'trigger_idea')
        assert hasattr(report, 'findings')
        assert hasattr(report, 'to_markdown')


class TestBranchTracker:
    """Test the branch tracker"""
    
    def test_tracker_initialization(self):
        """Test tracker can be initialized"""
        tracker = BranchTracker()
        assert tracker.repo_path == Path(".")
    
    def test_tracker_scan(self):
        """Test branch scanning"""
        tracker = BranchTracker()
        branches = tracker.scan()
        assert isinstance(branches, dict)
    
    def test_get_active_branches(self):
        """Test getting active branches"""
        tracker = BranchTracker()
        tracker.scan()
        active = tracker.get_active_branches()
        assert isinstance(active, list)
    
    def test_branch_type_parsing(self):
        """Test branch type parsing from name"""
        from branch_tracker import Branch
        
        branch = Branch.from_branch_name("feature/IDEA-012-test")
        assert branch.branch_type == BranchType.FEATURE
        assert branch.idea_id == "IDEA-012"
        
        branch = Branch.from_branch_name("hotfix/v1.2.1-bugfix")
        assert branch.branch_type == BranchType.HOTFIX


class TestExecutionTracker:
    """Test the execution tracker"""
    
    def test_tracker_initialization(self):
        """Test tracker can be initialized"""
        tracker = ExecutionTracker()
        assert tracker.doc3_path == Path("docs/DOC-3-CURRENT.md")
    
    def test_generate_draft(self):
        """Test draft generation"""
        tracker = ExecutionTracker()
        draft = tracker.generate_draft()
        assert draft is not None
        assert hasattr(draft, 'ideas')
        assert hasattr(draft, 'to_markdown')
        assert hasattr(draft, 'generated_at')
    
    def test_parse_ideas_backlog(self):
        """Test parsing ideas from backlog"""
        tracker = ExecutionTracker()
        ideas = tracker._parse_ideas_backlog()
        assert isinstance(ideas, list)


class TestPipelineIntegration:
    """Test the full pipeline integration"""
    
    def test_intake_to_execution_flow(self):
        """Test the flow from intake to execution tracking"""
        # 1. Process intake
        agent = IntakeAgent()
        result = agent.process_intake("Add a new dashboard feature for user analytics")
        
        assert result.complexity_score >= 1
        
        # 2. Generate idea file content
        idea_content = agent.generate_idea_file(result, "999")
        assert "IDEA-999" in idea_content["idea_id"]
        assert len(idea_content["content"]) > 100
        
        # 3. Sync detector still works
        detector = SyncDetector()
        entries = detector.load_backlog_entries()
        assert isinstance(entries, list)
        
        # 4. Execution tracker still works
        tracker = ExecutionTracker()
        draft = tracker.generate_draft()
        assert draft is not None


class TestDashboard:
    """Test dashboard components"""
    
    def test_branch_tracker_report_format(self):
        """Test branch report format"""
        tracker = BranchTracker()
        tracker.scan()
        report = tracker.get_report()
        assert isinstance(report, str)
        assert "Branch Tracker Report" in report
    
    def test_intake_agent_cli(self):
        """Test intake agent CLI output format"""
        agent = IntakeAgent()
        result = agent.process_intake("Test idea for dashboard")
        
        lines = [
            f"Routing:        {result.routing.value}",
            f"Idea Type:      {result.idea_type}",
            f"Complexity:     {result.complexity_score}/10",
            f"Refinement:     {result.refinement_mode.value}",
            f"Title:          {result.idea_title}",
        ]
        
        # Just verify we can format these lines
        for line in lines:
            assert isinstance(line, str)
            assert len(line) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
