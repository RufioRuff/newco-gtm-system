"""
Metal.ai Intelligence Module for NEWCO

Provides institutional intelligence capabilities inspired by Metal.ai:
- Document intelligence (pitch decks, LPAs, DD reports)
- Deal intelligence (manager/fund/portfolio analysis)
- Due diligence workflows
- Knowledge graph and search
- Market intelligence
- LP reporting automation

Uses local LLMs (Phase 1) with hooks for Metal.ai API (Phase 2)
"""

from .document_intelligence import DocumentIntelligence
from .deal_intelligence import DealIntelligence
from .due_diligence import DueDiligenceWorkflow
from .knowledge_graph import KnowledgeGraph
from .market_intelligence import MarketIntelligence
from .lp_reporting import LPReporting

__version__ = "1.0.0"
__all__ = [
    "DocumentIntelligence",
    "DealIntelligence",
    "DueDiligenceWorkflow",
    "KnowledgeGraph",
    "MarketIntelligence",
    "LPReporting",
]
