"""
Chapter 12: Ethical and Explainable Agents — Source Package

Author: Imran Ahmad
Book: 30 Agents Every AI Engineer Must Build, Chapter 12
Publisher: Packt Publishing
"""

__version__ = "1.0.0"
__author__ = "Imran Ahmad"

# -- Utility layer ----------------------------------------------------------
from src.utils import (
    ColorLogger,
    graceful_fallback,
    resolve_api_key,
    get_mode,
    is_simulation,
)

# -- Mock layer --------------------------------------------------------------
from src.mock_llm import MockLLM, get_mock_llm

# -- Synthetic data -----------------------------------------------------------
from src.synthetic_data import generate_hr_dataset, generate_medical_dataset

# -- Ethical core --------------------------------------------------------------
from src.ethical_core import (
    DeonticOperator,
    EthicalReasoningAgent,
    EUCompliantAgent,
    DemographicParityMetric,
    EqualOpportunityMetric,
    DisparateImpactMetric,
    BiasDetector,
    BiasMonitoringPipeline,
    ResumeAnalyzer,
    FairnessEnforcer,
    FairHiringAgent,
    demonstrate_impossibility_theorem,
)

# -- Explainability core -------------------------------------------------------
from src.explainability_core import (
    DecisionLogger,
    ExplainableAgent,
    compute_shap_explanations,
    compute_lime_explanations,
    train_diagnostic_model,
    generate_counterfactual,
    TemperatureScaler,
    ConfidenceAwareAgent,
    BiometricAnalyzer,
    SymptomInterpreter,
    DiagnosticCoordinator,
    ClinicalExplainer,
    DiagnosticAssistant,
)

# -- Public API ---------------------------------------------------------------
__all__ = [
    # Utils
    "ColorLogger",
    "graceful_fallback",
    "resolve_api_key",
    "get_mode",
    "is_simulation",
    # Mock
    "MockLLM",
    "get_mock_llm",
    # Data
    "generate_hr_dataset",
    "generate_medical_dataset",
    # Ethical Core
    "DeonticOperator",
    "EthicalReasoningAgent",
    "EUCompliantAgent",
    "DemographicParityMetric",
    "EqualOpportunityMetric",
    "DisparateImpactMetric",
    "BiasDetector",
    "BiasMonitoringPipeline",
    "ResumeAnalyzer",
    "FairnessEnforcer",
    "FairHiringAgent",
    "demonstrate_impossibility_theorem",
    # Explainability Core
    "DecisionLogger",
    "ExplainableAgent",
    "compute_shap_explanations",
    "compute_lime_explanations",
    "train_diagnostic_model",
    "generate_counterfactual",
    "TemperatureScaler",
    "ConfidenceAwareAgent",
    "BiometricAnalyzer",
    "SymptomInterpreter",
    "DiagnosticCoordinator",
    "ClinicalExplainer",
    "DiagnosticAssistant",
]
