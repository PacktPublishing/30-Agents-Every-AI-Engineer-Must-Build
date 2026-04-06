# src/__init__.py
# Author: Imran Ahmad
# Book: 30 Agents Every AI Engineer Must Build, Chapter 12
# Description: Package exports for the Chapter 12 source modules.

__version__ = "1.0.0"

# --- Utilities (src/utils.py) ---
from chapter12.utils import (
    ColorLogger,
    graceful_fallback,
    resolve_api_key,
    get_mode,
    is_simulation,
    logger,
)

# --- Mock Layer (src/mock_llm.py) ---
from chapter12.mock_llm import MockLLM, strip_meta

# --- Synthetic Data (src/synthetic_data.py) ---
from chapter12.synthetic_data import (
    generate_hr_dataset,
    generate_medical_dataset,
    summarize_hr_dataset,
    summarize_medical_dataset,
)

# --- Ethical Core (src/ethical_core.py) ---
from chapter12.ethical_core import (
    DeonticOperator,
    EthicalReasoningAgent,
    EUCompliantAgent,
    BiasDetector,
    BiasMonitoringPipeline,
    FairHiringAgent,
    FairnessEnforcer,
    ResumeAnalyzer,
    AuditLogger,
    DemographicParityMetric,
    EqualOpportunityMetric,
    DisparateImpactMetric,
    SlidingWindow,
)

# --- Explainability Core (src/explainability_core.py) ---
from chapter12.explainability_core import (
    ExplainableAgent,
    DecisionLogger,
    ExplanationGenerator,
    ConfidenceAwareAgent,
    TemperatureScaler,
    DiagnosticAssistant,
    DiagnosticReport,
    ClinicalExplainer,
    BiometricAnalyzer,
    SymptomInterpreter,
    DiagnosticCoordinator,
    ClinicalMemorySystem,
    compute_shap_explanation,
    compute_lime_explanation,
    generate_counterfactual,
)

__all__ = [
    # Version
    "__version__",
    # Utilities
    "ColorLogger",
    "graceful_fallback",
    "resolve_api_key",
    "get_mode",
    "is_simulation",
    "logger",
    # Mock
    "MockLLM",
    "strip_meta",
    # Data
    "generate_hr_dataset",
    "generate_medical_dataset",
    "summarize_hr_dataset",
    "summarize_medical_dataset",
    # Ethical Core
    "DeonticOperator",
    "EthicalReasoningAgent",
    "EUCompliantAgent",
    "BiasDetector",
    "BiasMonitoringPipeline",
    "FairHiringAgent",
    "FairnessEnforcer",
    "ResumeAnalyzer",
    "AuditLogger",
    "DemographicParityMetric",
    "EqualOpportunityMetric",
    "DisparateImpactMetric",
    "SlidingWindow",
    # Explainability Core
    "ExplainableAgent",
    "DecisionLogger",
    "ExplanationGenerator",
    "ConfidenceAwareAgent",
    "TemperatureScaler",
    "DiagnosticAssistant",
    "DiagnosticReport",
    "ClinicalExplainer",
    "BiometricAnalyzer",
    "SymptomInterpreter",
    "DiagnosticCoordinator",
    "ClinicalMemorySystem",
    "compute_shap_explanation",
    "compute_lime_explanation",
    "generate_counterfactual",
]
