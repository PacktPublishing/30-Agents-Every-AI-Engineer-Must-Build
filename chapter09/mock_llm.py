# src/mock_llm.py
# Chapter 9: Software Development Agents
# Book: "Agents" by Imran Ahmad (Packt, 2026)
# Author: Imran Ahmad
#
# Simulation Mode engine: MockLLM (keyword-matched response registry)
# and MockTestRunner (progressive pass/fail simulator).
#
# Every mock response constant is structurally identical to what a
# real LLM would produce for the corresponding chapter section.
# Ref: Strategy §2.3 — 12 response entries across §9.2, §9.3, §9.4.

from chapter09.utils import ColorLog


# ===================================================================
# Mock Response Constants — §9.2 Code-Generation Agents
# ===================================================================

# --- §9.2, Stage 1: Task Assignment (shipping calculator) ----------
_MOCK_SHIPPING_TASK_ASSIGNMENT = (
    "Task assigned: Implement a shipping cost calculator.\n"
    "Function: calculate_shipping(cart_total, weight)\n"
    "Requirements:\n"
    "  - Base rate: $5.00\n"
    "  - Weight cost: $0.50 per unit\n"
    "  - Tiered discounts: >$100 → 20%, >$50 → 10%, else 0%\n"
    "  - Must handle edge cases (zero weight, negative weight)\n"
    "Status: Ready for code synthesis."
)

# --- §9.2, Stage 2: Code Synthesis (initial — missing ValueError) --
_MOCK_SHIPPING_CODE_INITIAL = '''```python
def calculate_shipping(cart_total, weight):
    base_rate = 5.00
    weight_cost = weight * 0.50
    if cart_total > 100:
        discount = 0.20
    elif cart_total > 50:
        discount = 0.10
    else:
        discount = 0.0
    total = (base_rate + weight_cost) * (1 - discount)
    return total
```'''

# --- §9.2, Stage 3: Test Synthesis (pytest suite) -----------------
_MOCK_SHIPPING_TESTS = '''```python
import pytest
from shipping import calculate_shipping

def test_basic_shipping():
    assert calculate_shipping(30, 2) == 6.00

def test_tier_one_discount():
    assert calculate_shipping(60, 2) == 5.40

def test_tier_two_discount():
    assert calculate_shipping(120, 2) == 4.80

def test_zero_weight():
    assert calculate_shipping(100, 0) == 4.00

def test_negative_weight():
    with pytest.raises(ValueError):
        calculate_shipping(50, -1)
```'''

# --- §9.2, Stage 5: Refined Code (with ValueError) ----------------
_MOCK_SHIPPING_CODE_REFINED = '''```python
def calculate_shipping(cart_total, weight):
    if weight < 0:
        raise ValueError("Weight cannot be negative")
    base_rate = 5.00
    weight_cost = weight * 0.50
    if cart_total > 100:
        discount = 0.20
    elif cart_total > 50:
        discount = 0.10
    else:
        discount = 0.0
    total = (base_rate + weight_cost) * (1 - discount)
    return total
```'''

# --- §9.2, Full-Stack: Planning Agent (task decomposition) ---------
_MOCK_PLANNING_DECOMPOSITION = (
    "User story decomposed into 3 tasks:\n\n"
    "T1 (Backend): Create a GET /api/v1/users/{id} endpoint that returns "
    "user data (name, email, recent activity).\n"
    "  - task_id: T1-user-api\n"
    "  - task_type: backend\n"
    "  - dependencies: []\n\n"
    "T2 (Frontend): Create a React UserProfile component that fetches "
    "data from T1 and displays it.\n"
    "  - task_id: T2-user-profile\n"
    "  - task_type: frontend\n"
    "  - dependencies: [T1-user-api]\n\n"
    "T3 (Integration): Add the UserProfile component to the main "
    "application routing.\n"
    "  - task_id: T3-integration\n"
    "  - task_type: integration\n"
    "  - dependencies: [T1-user-api, T2-user-profile]"
)

# --- §9.2, Full-Stack: Backend Agent (T1 — Flask user API) --------
_MOCK_BACKEND_CODE = '''```python
from flask import Flask, Blueprint, jsonify, abort

user_bp = Blueprint("users", __name__)

# In-memory user store (mock database)
USERS = {
    "1": {
        "id": "1",
        "name": "Alice Chen",
        "email": "alice@example.com",
        "recent_activity": [
            {"action": "login", "timestamp": "2026-03-29T10:00:00Z"},
            {"action": "update_profile", "timestamp": "2026-03-28T14:30:00Z"},
        ],
    },
    "2": {
        "id": "2",
        "name": "Bob Martinez",
        "email": "bob@example.com",
        "recent_activity": [
            {"action": "login", "timestamp": "2026-03-29T09:00:00Z"},
        ],
    },
}

@user_bp.route("/api/v1/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """Return user data by ID. Returns 404 if not found."""
    user = USERS.get(user_id)
    if user is None:
        abort(404, description=f"User {user_id} not found")
    return jsonify(user), 200

app = Flask(__name__)
app.register_blueprint(user_bp)
```'''

# --- §9.2, Full-Stack: Backend Tests (T1 pytest) ------------------
_MOCK_BACKEND_TESTS = '''```python
import pytest
from unittest.mock import patch
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_user_success(client):
    response = client.get("/api/v1/users/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Alice Chen"
    assert "recent_activity" in data

def test_get_user_not_found(client):
    response = client.get("/api/v1/users/999")
    assert response.status_code == 404

def test_user_json_schema(client):
    response = client.get("/api/v1/users/1")
    data = response.get_json()
    assert "id" in data
    assert "name" in data
    assert "email" in data
    assert "recent_activity" in data
```'''

# --- §9.2, Full-Stack: Frontend Agent (T2 — React UserProfile) ----
_MOCK_FRONTEND_CODE = '''```typescript
import React, { useEffect, useState } from "react";

interface UserActivity {
  action: string;
  timestamp: string;
}

interface UserData {
  id: string;
  name: string;
  email: string;
  recent_activity: UserActivity[];
}

const UserProfile: React.FC<{ userId: string }> = ({ userId }) => {
  const [user, setUser] = useState<UserData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`/api/v1/users/${userId}`)
      .then((res) => {
        if (!res.ok) throw new Error("User not found");
        return res.json();
      })
      .then((data) => { setUser(data); setLoading(false); })
      .catch((err) => { setError(err.message); setLoading(false); });
  }, [userId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!user) return null;

  return (
    <div className="user-profile">
      <h2>{user.name}</h2>
      <p>{user.email}</p>
      <h3>Recent Activity</h3>
      <ul>
        {user.recent_activity.map((a, i) => (
          <li key={i}>{a.action} — {a.timestamp}</li>
        ))}
      </ul>
    </div>
  );
};

export default UserProfile;
```'''

# --- §9.2, Full-Stack: Frontend Tests (T2 Jest) -------------------
_MOCK_FRONTEND_TESTS = '''```typescript
import { render, screen, waitFor } from "@testing-library/react";
import UserProfile from "./UserProfile";

const mockUser = {
  id: "1",
  name: "Alice Chen",
  email: "alice@example.com",
  recent_activity: [{ action: "login", timestamp: "2026-03-29T10:00:00Z" }],
};

beforeEach(() => {
  global.fetch = jest.fn(() =>
    Promise.resolve({ ok: true, json: () => Promise.resolve(mockUser) })
  ) as jest.Mock;
});

test("renders user name", async () => {
  render(<UserProfile userId="1" />);
  await waitFor(() => expect(screen.getByText("Alice Chen")).toBeInTheDocument());
});

test("renders recent activity", async () => {
  render(<UserProfile userId="1" />);
  await waitFor(() => expect(screen.getByText(/login/i)).toBeInTheDocument());
});

test("shows error for missing user", async () => {
  global.fetch = jest.fn(() =>
    Promise.resolve({ ok: false, status: 404 })
  ) as jest.Mock;
  render(<UserProfile userId="999" />);
  await waitFor(() => expect(screen.getByText(/error/i)).toBeInTheDocument());
});
```'''

# --- §9.2, Full-Stack: Integration (T3 — routing) -----------------
_MOCK_INTEGRATION_CODE = '''```typescript
import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import UserProfile from "./components/UserProfile";

const App: React.FC = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/users/:userId" element={<UserProfile userId="1" />} />
    </Routes>
  </BrowserRouter>
);

export default App;
```

Integration complete. Backend API serves user data at /api/v1/users/{id}.
Frontend React component fetches and renders user profiles.
Routing configured to map /users/:userId to the UserProfile component.'''


# ===================================================================
# Mock Response Constants — §9.3 Compliance-Driven Agents
# ===================================================================

# --- §9.3, Static Compliance Validation (PCI card_number in log) ---
_MOCK_COMPLIANCE_SCAN = (
    "COMPLIANCE SCAN RESULTS\n"
    "=======================\n"
    "File: payment_handler.py\n"
    "Line 12: logger.info(f\"Processing payment for card {card_number}\")\n\n"
    "VIOLATION DETECTED:\n"
    "  Rule: PCI-DSS Requirement 3.3\n"
    "  Severity: CRITICAL\n"
    "  Description: Full card numbers must not appear in log output.\n"
    "  Evidence: Variable 'card_number' passed directly to logger.info()\n"
    "            without masking.\n\n"
    "RECOMMENDED REMEDIATION:\n"
    "  Replace: logger.info(f\"Processing payment for card {card_number}\")\n"
    "  With:    logger.info(f\"Processing payment for card "
    "{mask_card_number(card_number)}\")\n\n"
    "  Where mask_card_number() returns '****-****-****-1234' format."
)

# --- §9.3, Contextual Remediation (SHA-1 → SHA-256) ---------------
_MOCK_REMEDIATION_SHA = (
    "REMEDIATION PATCH\n"
    "=================\n"
    "Vulnerability: Use of deprecated SHA-1 hash algorithm.\n"
    "Regulation: PCI-DSS Requirement 3.4 (strong cryptography)\n\n"
    "Original code:\n"
    "  import hashlib\n"
    "  hash_value = hashlib.sha1(data).hexdigest()\n\n"
    "Patched code:\n"
    "  import hashlib\n"
    "  hash_value = hashlib.sha256(data).hexdigest()  # Updated to SHA-256\n\n"
    "Impact: SHA-256 provides collision resistance suitable for PCI DSS.\n"
    "Tests: Re-run test suite to verify hash-dependent logic still passes."
)

# --- §9.3, Semantic Code Understanding (anonymization analysis) ----
_MOCK_SEMANTIC_ANALYSIS = (
    "SEMANTIC CODE ANALYSIS\n"
    "======================\n"
    "Function: anonymize_user_data(record)\n"
    "Declared purpose (docstring): 'Anonymizes patient records by removing "
    "all identifying information.'\n\n"
    "ANALYSIS:\n"
    "  Fields removed: ['name']\n"
    "  Fields RETAINED: ['email', 'phone_number', 'date_of_birth', 'ip_address']\n\n"
    "VIOLATION DETECTED:\n"
    "  Rule: HIPAA Safe Harbor De-identification\n"
    "  Severity: HIGH\n"
    "  Description: The function claims full anonymization but retains\n"
    "    email, phone number, date of birth, and IP address — all of\n"
    "    which are HIPAA-defined identifiers. True de-identification\n"
    "    under the Safe Harbor method requires removal or generalization\n"
    "    of all 18 HIPAA identifier categories.\n\n"
    "RECOMMENDED REMEDIATION:\n"
    "  Remove or generalize: email, phone_number, date_of_birth, ip_address.\n"
    "  Update docstring to reflect actual scope if partial anonymization\n"
    "  is intended."
)


# ===================================================================
# Mock Response Constants — §9.4 Self-Improving Agents
# ===================================================================

# --- §9.4, Planner Agent Hypothesis Generation --------------------
_MOCK_PLANNER_HYPOTHESES = '''{
    "hypotheses": [
        {
            "source_signal": "async pattern rejections (23 of 31 async tasks)",
            "adaptation_type": "prompt_update",
            "proposed_change": "Add 3 async/await few-shot examples to code-gen prompt",
            "confidence": 0.87,
            "evidence_count": 23,
            "rollback_safe": true
        },
        {
            "source_signal": "false positives on test files (41% of violations)",
            "adaptation_type": "threshold_adjustment",
            "proposed_change": "Add test-file context exception to compliance rules",
            "confidence": 0.92,
            "evidence_count": 67,
            "rollback_safe": true
        },
        {
            "source_signal": "escalation rate for policy-related queries exceeds 45%",
            "adaptation_type": "retrieval_strategy",
            "proposed_change": "Weight recency more heavily for policy-related queries in RAG retrieval",
            "confidence": 0.78,
            "evidence_count": 34,
            "rollback_safe": true
        }
    ],
    "requires_human_review": false,
    "baseline_metrics": {"task_completion": 0.74, "false_positive_rate": 0.41}
}'''

# --- §9.4, Critic Agent KPI Evaluation ----------------------------
_MOCK_CRITIC_EVALUATION = (
    "CRITIC AGENT EVALUATION\n"
    "=======================\n"
    "Evaluation Period: 2026-Q1 (90 days)\n\n"
    "KPI Scores:\n"
    "  Task Completion Rate:     0.74  (target: 0.80) — BELOW TARGET\n"
    "  Error Recovery Ratio:     0.89  (target: 0.85) — ABOVE TARGET\n"
    "  Latency P95:              2.3s  (target: 3.0s) — WITHIN RANGE\n"
    "  User Satisfaction Index:  3.8   (target: 4.0)  — BELOW TARGET\n"
    "  Improvement Velocity:     0.12  (target: 0.10) — ABOVE TARGET\n\n"
    "IDENTIFIED FAILURE MODES:\n"
    "  1. Async pattern handling: 74% rejection rate on async/await code.\n"
    "  2. Policy query resolution: 45% escalation rate (vs. 20% target).\n"
    "  3. Tone mismatch: Formal responses to frustrated users scored\n"
    "     1.2 points below mean satisfaction.\n\n"
    "RECOMMENDATION: Route to Planner Agent for hypothesis generation."
)

# --- §9.4, Sensing Layer Summary ----------------------------------
_MOCK_SENSING_SUMMARY = (
    "SENSING LAYER REPORT\n"
    "====================\n"
    "Collection Period: 2026-03-01 to 2026-03-29\n\n"
    "Explicit Feedback:  142 signals\n"
    "  - Ratings: avg 3.8/5.0, std 0.9\n"
    "  - Comments: 67 (47% mention 'context understanding')\n\n"
    "Implicit Feedback:  1,847 signals\n"
    "  - Avg turns per resolution: 4.2\n"
    "  - Rephrased questions: 23% of conversations\n"
    "  - Abandonment rate: 8.3%\n\n"
    "Synthetic Feedback: 500 benchmark evaluations\n"
    "  - Functional correctness: 91%\n"
    "  - Code quality score: 78%\n"
    "  - Maintainability index: 72%\n\n"
    "Top signals forwarded to Critic Agent for evaluation."
)


# ===================================================================
# MockLLMResponse — Mimics LLM response interface
# ===================================================================

class MockLLMResponse:
    """
    Lightweight response object compatible with LangChain's
    AIMessage interface. Provides .content attribute for text
    extraction in agent node functions.
    """

    def __init__(self, content: str):
        self.content = content

    def __repr__(self):
        preview = self.content[:80].replace("\n", " ")
        return f"MockLLMResponse('{preview}...')"


# ===================================================================
# MockLLM — Context-Aware Response Engine
# ===================================================================

class MockLLM:
    """
    Simulation Mode LLM that returns chapter-accurate mock responses
    based on keyword matching against the prompt.

    Supports 12 response entries spanning:
      - §9.2: Shipping calculator (stages 1-6), full-stack (T1/T2/T3)
      - §9.3: Compliance scan, remediation, semantic analysis
      - §9.4: Critic evaluation, planner hypotheses, sensing summary

    The keyword registry maps prompt content to the corresponding
    chapter section's expected output.

    Ref: Strategy §2.3 — all 12 mock entries.
    """

    def __init__(self):
        self._call_count = {}
        ColorLog.info("MockLLM initialized (Simulation Mode active).")

    def invoke(self, prompt):
        """
        Match prompt keywords to chapter-derived mock responses.
        Returns a MockLLMResponse with .content attribute.
        """
        if isinstance(prompt, list):
            # Handle LangChain message list format
            text = " ".join(
                m.content if hasattr(m, "content") else str(m)
                for m in prompt
            )
        else:
            text = str(prompt)

        text_lower = text.lower()
        response_content = self._match_response(text_lower, text)

        ColorLog.info(
            f"MockLLM invoked — matched response "
            f"({len(response_content)} chars)."
        )
        return MockLLMResponse(response_content)

    def _match_response(self, text_lower, text_original):
        """
        Keyword-based routing to the correct mock response constant.
        Order matters: more specific patterns are checked first.
        """

        # --- §9.2 Shipping Calculator ---
        # Stage 5: Refinement (prompt contains error context)
        if ("shipping" in text_lower or "calculate_shipping" in text_lower):
            if "failed" in text_lower or "valueerror" in text_lower or "fix" in text_lower:
                self._track("shipping_refined")
                return _MOCK_SHIPPING_CODE_REFINED

        # Stage 3: Test synthesis
        if ("test" in text_lower and
                ("shipping" in text_lower or "calculate_shipping" in text_lower)):
            self._track("shipping_tests")
            return _MOCK_SHIPPING_TESTS

        # Stage 2: Initial code synthesis
        if ("shipping" in text_lower or "calculate_shipping" in text_lower):
            call_key = "shipping_code"
            count = self._call_count.get(call_key, 0)
            self._track(call_key)
            if count > 0:
                return _MOCK_SHIPPING_CODE_REFINED
            return _MOCK_SHIPPING_CODE_INITIAL

        # Stage 1: Task assignment
        if "task" in text_lower and "assign" in text_lower:
            self._track("task_assignment")
            return _MOCK_SHIPPING_TASK_ASSIGNMENT

        # --- §9.2 Full-Stack User Profile ---
        # Planning decomposition
        if ("decompos" in text_lower or "user story" in text_lower or
                "plan" in text_lower and "profile" in text_lower):
            self._track("planning")
            return _MOCK_PLANNING_DECOMPOSITION

        # Integration (T3)
        if "integrat" in text_lower and ("route" in text_lower or "routing" in text_lower):
            self._track("integration")
            return _MOCK_INTEGRATION_CODE

        # Frontend tests
        if "test" in text_lower and ("frontend" in text_lower or
                "react" in text_lower or "jest" in text_lower):
            self._track("frontend_tests")
            return _MOCK_FRONTEND_TESTS

        # Frontend code (T2)
        if ("frontend" in text_lower or "react" in text_lower or
                "userprofile" in text_lower or "user profile" in text_lower and
                "component" in text_lower):
            self._track("frontend_code")
            return _MOCK_FRONTEND_CODE

        # Backend tests
        if "test" in text_lower and ("backend" in text_lower or
                "flask" in text_lower or "pytest" in text_lower or
                "api" in text_lower):
            self._track("backend_tests")
            return _MOCK_BACKEND_TESTS

        # Backend code (T1)
        if ("backend" in text_lower or "flask" in text_lower or
                "endpoint" in text_lower or "api" in text_lower):
            self._track("backend_code")
            return _MOCK_BACKEND_CODE

        # --- §9.3 Compliance ---
        # Semantic analysis (anonymization)
        if "anonymiz" in text_lower or "semantic" in text_lower:
            self._track("semantic_analysis")
            return _MOCK_SEMANTIC_ANALYSIS

        # Remediation (SHA / encryption)
        if ("remediat" in text_lower or "sha" in text_lower or
                "encrypt" in text_lower or "patch" in text_lower):
            self._track("remediation")
            return _MOCK_REMEDIATION_SHA

        # Compliance scan (PCI / card_number)
        if ("complian" in text_lower or "pci" in text_lower or
                "card_number" in text_lower or "violation" in text_lower or
                "scan" in text_lower):
            self._track("compliance_scan")
            return _MOCK_COMPLIANCE_SCAN

        # --- §9.4 Self-Improving ---
        # Planner hypotheses
        if ("planner" in text_lower or "hypothes" in text_lower or
                "improvement" in text_lower and "propose" in text_lower):
            self._track("planner")
            return _MOCK_PLANNER_HYPOTHESES

        # Critic evaluation
        if ("critic" in text_lower or "kpi" in text_lower or
                "evaluat" in text_lower):
            self._track("critic")
            return _MOCK_CRITIC_EVALUATION

        # Sensing summary
        if ("sensing" in text_lower or "feedback" in text_lower or
                "collect" in text_lower):
            self._track("sensing")
            return _MOCK_SENSING_SUMMARY

        # --- Fallback ---
        self._track("fallback")
        return (
            "MockLLM: No specific mock response matched for this prompt. "
            "This is a simulation fallback. In Live Mode, the real LLM "
            "would generate a contextual response here."
        )

    def _track(self, key):
        """Track invocation counts per response category."""
        self._call_count[key] = self._call_count.get(key, 0) + 1


# ===================================================================
# MockTestRunner — Progressive Pass/Fail Simulator
# ===================================================================

class MockTestRunner:
    """
    Simulates pytest execution with progressive pass/fail behavior
    to demonstrate the TDG refinement loop (§9.2, Stages 4–6).

    First invocation: Fails on code without ValueError handling.
    Subsequent invocations: Passes if code contains 'ValueError'.

    This models the chapter's shipping calculator progression:
      Run 1 → FAILED test_negative_weight (no ValueError raised)
      Run 2 → ALL TESTS PASSED (ValueError added after refinement)
    """

    _FAIL_RESULT = (
        "============================= test session starts =============================\n"
        "collected 5 items\n\n"
        "test_shipping.py::test_basic_shipping PASSED\n"
        "test_shipping.py::test_tier_one_discount PASSED\n"
        "test_shipping.py::test_tier_two_discount PASSED\n"
        "test_shipping.py::test_zero_weight PASSED\n"
        "test_shipping.py::test_negative_weight FAILED\n\n"
        "=================================== FAILURES ===================================\n"
        "_________________________ test_negative_weight _________________________________\n\n"
        "    def test_negative_weight():\n"
        ">       with pytest.raises(ValueError):\n"
        "E       Failed: DID NOT RAISE <class 'ValueError'>\n\n"
        "FAILED test_negative_weight - Did not raise ValueError\n"
        "Expected exception ValueError but function returned -0.50\n\n"
        "========================= 1 failed, 4 passed in 0.03s ========================="
    )

    _PASS_RESULT = (
        "============================= test session starts =============================\n"
        "collected 5 items\n\n"
        "test_shipping.py::test_basic_shipping PASSED\n"
        "test_shipping.py::test_tier_one_discount PASSED\n"
        "test_shipping.py::test_tier_two_discount PASSED\n"
        "test_shipping.py::test_zero_weight PASSED\n"
        "test_shipping.py::test_negative_weight PASSED\n\n"
        "========================= 5 passed in 0.02s ========================="
    )

    def __init__(self):
        self._run_count = 0

    def run(self, code_content=""):
        """
        Execute a simulated test run.

        Args:
            code_content: The code string to evaluate. If it contains
                'ValueError', the negative weight test passes.

        Returns:
            tuple: (passed: bool, output: str)
        """
        self._run_count += 1

        if "ValueError" in code_content:
            ColorLog.success(
                f"MockTestRunner: Run {self._run_count} — "
                f"ALL 5 TESTS PASSED."
            )
            return True, self._PASS_RESULT
        else:
            ColorLog.error(
                f"MockTestRunner: Run {self._run_count} — "
                f"1 FAILED (test_negative_weight), 4 passed."
            )
            return False, self._FAIL_RESULT

    def reset(self):
        """Reset the run counter for a new test sequence."""
        self._run_count = 0
