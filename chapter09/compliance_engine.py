# src/compliance_engine.py
# Chapter 9: Software Development Agents
# Book: "Agents" by Imran Ahmad (Packt, 2026)
# Author: Imran Ahmad
#
# Compliance-Driven Agent components implementing the
# scan → evaluate → remediate feedback loop.
#
# Components:
#   - PolicyRule / PolicyEngine — declarative rule evaluation (Rego-like)
#   - ComplianceScanner — wraps PolicyEngine + semantic LLM analysis
#   - RemediationGenerator — generates fix suggestions via LLM
#   - AuditTrail — immutable append-only compliance log
#   - DataFlowAnalyzer — PII/PHI variable tagging and tracing
#
# Pre-loaded rules: PCI DSS (Req 3.3, 3.4, 4.1), HIPAA (PHI logging, API)
#
# Ref: §9.3, "Core Capabilities and Technical Architecture"
# Ref: §9.3, "Architectural Components and Integration"
# Ref: §9.3, "Practical Implementation: Enforcing PCI DSS"

import json
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from chapter09.utils import ColorLog, fail_gracefully


# ===================================================================
# PolicyRule — Declarative Rule Model
# ===================================================================

class PolicyRule(BaseModel):
    """
    A single compliance rule analogous to a Rego policy definition.
    Each rule specifies keyword triggers, severity, and the regulation
    it enforces.

    The policy engine acts as the 'test suite' for compliance: just as
    functional tests define correct behavior, policies define
    permissible behavior.

    Ref: §9.3, "Architectural Components — Policy Engine"
    """
    rule_id: str
    description: str
    keywords: List[str] = Field(
        description="Patterns that trigger this rule in source code"
    )
    severity: str = Field(
        description="CRITICAL, HIGH, MEDIUM, or LOW"
    )
    regulation_ref: str = Field(
        description="e.g., PCI-DSS 3.3, HIPAA Safe Harbor"
    )
    remediation_hint: str = Field(
        default="",
        description="Suggested fix pattern"
    )


# ===================================================================
# Pre-loaded PCI DSS and HIPAA Rules
# ===================================================================

# Ref: §9.3, "Static Compliance Validation" — PCI DSS examples
# Ref: §9.3, "PCI DSS Case Study" — Rego rule for Requirement 3.3

PCI_DSS_RULES = [
    PolicyRule(
        rule_id="PCI-DSS-3.3",
        description=(
            "Full card numbers must not appear in log output. "
            "Mask PAN when displayed."
        ),
        keywords=["card_number", "pan", "credit_card"],
        severity="CRITICAL",
        regulation_ref="PCI-DSS Requirement 3.3",
        remediation_hint=(
            "Use mask_card_number() to display only last 4 digits. "
            "Format: ****-****-****-1234"
        ),
    ),
    PolicyRule(
        rule_id="PCI-DSS-3.4",
        description=(
            "Stored cardholder data must be rendered unreadable using "
            "strong cryptography (SHA-256 or AES-256 minimum)."
        ),
        keywords=["sha1", "md5", "hashlib.sha1", "hashlib.md5"],
        severity="CRITICAL",
        regulation_ref="PCI-DSS Requirement 3.4",
        remediation_hint=(
            "Replace SHA-1/MD5 with SHA-256 or stronger. "
            "Use hashlib.sha256(data).hexdigest()."
        ),
    ),
    PolicyRule(
        rule_id="PCI-DSS-4.1",
        description=(
            "Sensitive cardholder data must be encrypted during "
            "transmission over open, public networks."
        ),
        keywords=["http://", "ftp://", "telnet://"],
        severity="HIGH",
        regulation_ref="PCI-DSS Requirement 4.1",
        remediation_hint=(
            "Use HTTPS (TLS 1.2+) for all data transmission. "
            "Replace http:// with https://."
        ),
    ),
]

# Ref: §9.3, "Semantic Code Understanding" — HIPAA anonymization
# Ref: §9.3, "Healthcare Applications" deployment pattern

HIPAA_RULES = [
    PolicyRule(
        rule_id="HIPAA-PHI-LOG",
        description=(
            "Protected Health Information (PHI) must not appear in "
            "log files, error messages, or debug output."
        ),
        keywords=["patient", "diagnosis", "medical_record", "ssn", "dob"],
        severity="CRITICAL",
        regulation_ref="HIPAA Privacy Rule §164.502",
        remediation_hint=(
            "Log only de-identified references (patient.id). "
            "Never log full patient records: logger.debug(f'Patient "
            "record retrieved: {patient.id}')"
        ),
    ),
    PolicyRule(
        rule_id="HIPAA-PHI-API",
        description=(
            "API responses must not expose raw PHI without proper "
            "redaction of identifiable fields."
        ),
        keywords=["patient.to_dict", "to_json", "serialize"],
        severity="HIGH",
        regulation_ref="HIPAA Privacy Rule §164.514",
        remediation_hint=(
            "Redact identifiable fields before serialization. "
            "Use a PHI-aware serializer that strips name, email, "
            "phone, DOB, and SSN."
        ),
    ),
]


# ===================================================================
# PolicyEngine — Declarative Rule Evaluation
# ===================================================================

class PolicyEngine:
    """
    Evaluates source code against a registry of PolicyRule definitions.
    Produces pass/fail decisions with detailed violation reports.

    Analogous to Open Policy Agent (OPA) with Rego rules, but
    implemented as a lightweight Python evaluator for educational
    demonstration.

    The engine acts as the 'test suite' for compliance: just as
    functional tests define correct behavior, policies define
    permissible behavior.

    Ref: §9.3, "Architectural Components — Policy Engine"
    Ref: §9.3, "PCI DSS Case Study — Rego policy listing"
    """

    def __init__(self, rules: Optional[List[PolicyRule]] = None):
        self.rules: List[PolicyRule] = rules or []
        self._version = "1.0.0"
        ColorLog.info(
            f"PolicyEngine initialized with {len(self.rules)} rules "
            f"(v{self._version})."
        )

    def add_rule(self, rule: PolicyRule):
        """Add a rule to the engine registry."""
        self.rules.append(rule)
        ColorLog.info(f"PolicyEngine: Added rule {rule.rule_id}.")

    def load_pci_dss(self):
        """Load pre-defined PCI DSS compliance rules."""
        for rule in PCI_DSS_RULES:
            if rule.rule_id not in [r.rule_id for r in self.rules]:
                self.rules.append(rule)
        ColorLog.info(
            f"PolicyEngine: Loaded {len(PCI_DSS_RULES)} PCI DSS rules."
        )

    def load_hipaa(self):
        """Load pre-defined HIPAA compliance rules."""
        for rule in HIPAA_RULES:
            if rule.rule_id not in [r.rule_id for r in self.rules]:
                self.rules.append(rule)
        ColorLog.info(
            f"PolicyEngine: Loaded {len(HIPAA_RULES)} HIPAA rules."
        )

    @fail_gracefully(fallback_return=lambda: [])
    def evaluate(self, code: str) -> List[Dict[str, Any]]:
        """
        Evaluate code against all registered policy rules.

        Scans each line for keyword matches, returning a list of
        violation dicts with rule details and line references.

        Ref: §9.3, "Static Compliance Validation"

        Args:
            code: Source code string to evaluate.

        Returns:
            List of violation dicts, empty if compliant.
        """
        violations = []
        lines = code.split("\n")

        for rule in self.rules:
            for line_num, line in enumerate(lines, 1):
                line_lower = line.lower()
                for keyword in rule.keywords:
                    if keyword.lower() in line_lower:
                        # Check for masking/mitigation patterns
                        if self._is_mitigated(line_lower, rule):
                            continue
                        violations.append({
                            "rule_id": rule.rule_id,
                            "regulation_ref": rule.regulation_ref,
                            "severity": rule.severity,
                            "description": rule.description,
                            "line_number": line_num,
                            "line_content": line.strip(),
                            "keyword_matched": keyword,
                            "remediation_hint": rule.remediation_hint,
                        })
                        break  # One match per rule per line

        if violations:
            ColorLog.error(
                f"PolicyEngine: {len(violations)} violation(s) detected "
                f"across {len(set(v['rule_id'] for v in violations))} rules."
            )
        else:
            ColorLog.success("PolicyEngine: Code is compliant. No violations.")

        return violations

    def _is_mitigated(self, line_lower: str, rule: PolicyRule) -> bool:
        """Check if the line contains mitigation patterns."""
        mitigations = {
            "PCI-DSS-3.3": ["mask_card", "****", "[-4:]", "[:-4]"],
            "PCI-DSS-3.4": ["sha256", "sha384", "sha512", "aes"],
            "PCI-DSS-4.1": ["https://"],
            "HIPAA-PHI-LOG": [".id)", ".id}", "patient_id"],
            "HIPAA-PHI-API": ["redact", "sanitize", "filter_phi"],
        }
        for pattern in mitigations.get(rule.rule_id, []):
            if pattern.lower() in line_lower:
                return True
        return False


# ===================================================================
# ComplianceScanner — PolicyEngine + Semantic LLM Analysis
# ===================================================================

class ComplianceScanner:
    """
    Wraps the PolicyEngine with an LLM-powered semantic analysis layer.

    Combines deterministic rule evaluation (fast, reliable for known
    patterns) with probabilistic semantic analysis (detects contextual
    violations that pattern matching misses).

    Ref: §9.3, "Semantic Code Understanding"
    Ref: §9.3, "Architectural Components — Language Model Layer"
    """

    def __init__(self, policy_engine: PolicyEngine, llm: Any = None):
        self.policy_engine = policy_engine
        self.llm = llm
        ColorLog.info("ComplianceScanner initialized.")

    @fail_gracefully(fallback_return=lambda: {"static": [], "semantic": ""})
    def full_scan(self, code: str) -> Dict[str, Any]:
        """
        Run both static policy evaluation and semantic analysis.

        Returns:
            Dict with 'static' (list of violations) and 'semantic'
            (LLM analysis string).
        """
        ColorLog.info("ComplianceScanner: Starting full scan...")

        # Phase 1: Static rule evaluation
        static_violations = self.policy_engine.evaluate(code)

        # Phase 2: Semantic analysis via LLM
        semantic_result = ""
        if self.llm:
            prompt = (
                f"You are a compliance analysis agent.\n"
                f"Analyze this code for semantic compliance violations "
                f"that pattern matching might miss.\n"
                f"Look for:\n"
                f"  - Functions claiming anonymization but retaining "
                f"identifiable fields\n"
                f"  - Incomplete data redaction\n"
                f"  - Implicit PII exposure through data structures\n\n"
                f"Code:\n{code}\n\n"
                f"Report any semantic violations found."
            )
            response = self.llm.invoke(prompt)
            semantic_result = response.content

        scan_result = {
            "static": static_violations,
            "semantic": semantic_result,
            "total_violations": len(static_violations),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if static_violations:
            ColorLog.error(
                f"ComplianceScanner: {len(static_violations)} static "
                f"violation(s) found."
            )
        else:
            ColorLog.success("ComplianceScanner: No static violations.")

        if semantic_result:
            ColorLog.info(
                f"ComplianceScanner: Semantic analysis complete "
                f"({len(semantic_result)} chars)."
            )

        return scan_result


# ===================================================================
# RemediationGenerator — Fix Suggestion Engine
# ===================================================================

class RemediationGenerator:
    """
    Generates specific remediation patches for detected violations.
    Uses the LLM to produce developer-friendly fix suggestions.

    Integrates directly with TDG refinement loops: just as test
    failures trigger code regeneration, policy violations trigger
    remediation suggestions.

    Ref: §9.3, "Contextual Intervention and Remediation"
    """

    def __init__(self, llm: Any = None):
        self.llm = llm
        ColorLog.info("RemediationGenerator initialized.")

    @fail_gracefully(fallback_return=lambda: {})
    def generate(self, violation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a remediation patch for a specific violation.

        Args:
            violation: Dict from PolicyEngine.evaluate() result.

        Returns:
            Dict with 'original', 'patched', and 'explanation' fields.
        """
        ColorLog.info(
            f"RemediationGenerator: Generating fix for "
            f"{violation.get('rule_id', 'unknown')}..."
        )

        line = violation.get("line_content", "")
        rule_id = violation.get("rule_id", "")
        hint = violation.get("remediation_hint", "")

        # Apply known remediation patterns
        patched = self._apply_known_fix(line, rule_id)

        # If LLM available, get richer remediation
        explanation = hint
        if self.llm and not patched:
            prompt = (
                f"Generate a remediation patch for this compliance "
                f"violation.\n\n"
                f"Violation: {violation.get('description', '')}\n"
                f"Regulation: {violation.get('regulation_ref', '')}\n"
                f"Code line: {line}\n\n"
                f"Provide the corrected code and explanation."
            )
            response = self.llm.invoke(prompt)
            explanation = response.content

        result = {
            "rule_id": rule_id,
            "original": line,
            "patched": patched or f"[See hint: {hint}]",
            "explanation": explanation,
            "auto_fixable": bool(patched),
        }

        if patched:
            ColorLog.success(
                f"RemediationGenerator: Auto-fix available for {rule_id}."
            )
        else:
            ColorLog.info(
                f"RemediationGenerator: Manual review needed for {rule_id}."
            )

        return result

    def _apply_known_fix(self, line: str, rule_id: str) -> Optional[str]:
        """
        Apply deterministic fixes for well-known violation patterns.
        Ref: §9.3, SHA-1 → SHA-256 remediation listing.
        """
        # PCI-DSS-3.3: Mask card numbers in logging
        if rule_id == "PCI-DSS-3.3":
            # Replace direct card_number refs with masked version
            patched = re.sub(
                r'\{card_number\}',
                '{mask_card_number(card_number)}',
                line,
            )
            if patched != line:
                return patched

        # PCI-DSS-3.4: SHA-1 → SHA-256
        if rule_id == "PCI-DSS-3.4":
            if "sha1" in line.lower():
                return line.replace("sha1", "sha256").replace(
                    "SHA1", "SHA256"
                )
            if "md5" in line.lower():
                return line.replace("md5", "sha256").replace(
                    "MD5", "SHA256"
                )

        # PCI-DSS-4.1: HTTP → HTTPS
        if rule_id == "PCI-DSS-4.1":
            return line.replace("http://", "https://")

        return None


# ===================================================================
# AuditTrail — Immutable Compliance Log
# ===================================================================

class AuditTrail:
    """
    Append-only log recording all compliance agent actions: scans,
    violations, remediations, and human overrides.

    Serializable to JSON for regulatory evidence gathering.

    Ref: §9.3, "Audit Trail Generation"
    Ref: §9.3, "PCI DSS Case Study — Workflow Integration, Audit Trail"
    """

    def __init__(self):
        self._entries: List[Dict[str, Any]] = []
        ColorLog.info("AuditTrail initialized (empty).")

    def append(
        self,
        action: str,
        details: Dict[str, Any],
        actor: str = "compliance_agent",
    ):
        """
        Record an immutable audit entry.

        Args:
            action: Type of action (scan, violation, remediation, override).
            details: Structured details of the action.
            actor: Who performed the action (agent or human reviewer).
        """
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "action": action,
            "actor": actor,
            "details": details,
            "entry_id": len(self._entries) + 1,
        }
        self._entries.append(entry)
        ColorLog.info(
            f"AuditTrail: Recorded #{entry['entry_id']} — "
            f"{action} by {actor}."
        )

    def to_json(self, indent: int = 2) -> str:
        """Serialize the full audit trail to JSON."""
        return json.dumps(self._entries, indent=indent, default=str)

    def get_entries(
        self,
        action_filter: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Retrieve entries, optionally filtered by action type."""
        if action_filter:
            return [e for e in self._entries if e["action"] == action_filter]
        return list(self._entries)

    @property
    def count(self) -> int:
        return len(self._entries)


# ===================================================================
# DataFlowAnalyzer — PII/PHI Variable Tagging and Tracing
# ===================================================================

class DataFlowAnalyzer:
    """
    Tags variables containing sensitive data at their point of origin
    and traces them through a simulated call graph.

    Raises violations when tagged variables are passed to unsafe
    sinks (logging, unencrypted storage, non-compliant regions).

    Ref: §9.3, "Data Flow Analysis"
    """

    # Known sensitive variable patterns
    _PII_PATTERNS = [
        "email", "phone", "ssn", "social_security", "address",
        "name", "dob", "date_of_birth", "ip_address",
    ]
    _PHI_PATTERNS = [
        "patient", "diagnosis", "medical_record", "prescription",
        "treatment", "health_record",
    ]
    _PAYMENT_PATTERNS = [
        "card_number", "cvv", "pan", "credit_card", "account_number",
    ]

    # Unsafe sinks — data should not flow here unprotected
    _UNSAFE_SINKS = [
        "logger.", "print(", "logging.", "console.log",
        "analytics.", "send_to_",
    ]

    def __init__(self):
        ColorLog.info("DataFlowAnalyzer initialized.")

    @fail_gracefully(fallback_return=lambda: [])
    def analyze(self, code: str) -> List[Dict[str, Any]]:
        """
        Trace sensitive data flow through code, flagging unsafe sinks.

        Args:
            code: Source code string to analyze.

        Returns:
            List of data flow violation dicts.
        """
        ColorLog.info("DataFlowAnalyzer: Tracing sensitive data flows...")
        violations = []
        lines = code.split("\n")

        # Phase 1: Identify tagged variables
        tagged_vars = self._tag_variables(code)

        # Phase 2: Check for unsafe sink access
        for line_num, line in enumerate(lines, 1):
            line_lower = line.lower()
            for sink in self._UNSAFE_SINKS:
                if sink.lower() in line_lower:
                    # Check if any tagged variable appears in this sink call
                    for var_name, data_class in tagged_vars.items():
                        if var_name.lower() in line_lower:
                            violations.append({
                                "type": "unsafe_data_flow",
                                "variable": var_name,
                                "data_class": data_class,
                                "sink": sink.rstrip(".("),
                                "line_number": line_num,
                                "line_content": line.strip(),
                                "recommendation": (
                                    f"Variable '{var_name}' ({data_class}) "
                                    f"flows to unsafe sink '{sink.rstrip('.(')}'."
                                    f" Redact or mask before output."
                                ),
                            })

        if violations:
            ColorLog.error(
                f"DataFlowAnalyzer: {len(violations)} unsafe data "
                f"flow(s) detected."
            )
        else:
            ColorLog.success(
                "DataFlowAnalyzer: No unsafe data flows detected."
            )

        return violations

    def _tag_variables(self, code: str) -> Dict[str, str]:
        """
        Scan code for variable names matching sensitive data patterns.
        Returns a dict mapping variable names to data classification.
        """
        tagged = {}
        # Simple heuristic: find assignments and function parameters
        identifiers = set(re.findall(r'\b([a-zA-Z_]\w*)\b', code))

        for ident in identifiers:
            ident_lower = ident.lower()
            for pattern in self._PAYMENT_PATTERNS:
                if pattern in ident_lower:
                    tagged[ident] = "PCI/Payment"
                    break
            for pattern in self._PHI_PATTERNS:
                if pattern in ident_lower:
                    tagged[ident] = "HIPAA/PHI"
                    break
            for pattern in self._PII_PATTERNS:
                if pattern in ident_lower:
                    tagged[ident] = "PII"
                    break

        if tagged:
            ColorLog.info(
                f"DataFlowAnalyzer: Tagged {len(tagged)} sensitive "
                f"variable(s): {list(tagged.keys())}"
            )
        return tagged
