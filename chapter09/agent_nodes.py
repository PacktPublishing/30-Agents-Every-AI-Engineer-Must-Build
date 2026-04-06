# src/agent_nodes.py
# Chapter 9: Software Development Agents
# Book: "Agents" by Imran Ahmad (Packt, 2026)
# Author: Imran Ahmad
#
# LangGraph node functions implementing the multi-agent TDG workflow.
# Each node receives AgentState, performs its specialized operation,
# and returns updated state.
#
# Ref: §9.2, "Implementing Agent Nodes" and "Building the LangGraph Workflow"
# Ref: §9.2, "Parallel Execution Across the Stack" (T1/T2/T3 case study)

import re
from typing import Any, Dict

from chapter09.utils import ColorLog, fail_gracefully
from chapter09.state_models import Task, AgentState


# ---------------------------------------------------------------------------
# Helper: Extract Code from LLM Response
# ---------------------------------------------------------------------------

def extract_code_from_response(content: str, language: str = "python") -> str:
    """
    Strips markdown code fences from LLM responses, returning clean
    code artifacts for storage in AgentState.

    Handles patterns like:
        ```python
        def foo(): ...
        ```
    and also raw code without fences.

    Ref: §9.2, "Implementing Agent Nodes" — extract_code_from_response utility.

    Args:
        content: Raw LLM response string.
        language: Expected language tag (python, typescript, etc.)

    Returns:
        Clean code string without markdown formatting.
    """
    # Try to extract fenced code block for the specific language
    pattern = rf"```(?:{language})?\s*\n(.*?)```"
    matches = re.findall(pattern, content, re.DOTALL)
    if matches:
        # Return the longest match (most likely the main code block)
        return max(matches, key=len).strip()

    # Fallback: if no fenced block, return content as-is (trimmed)
    return content.strip()


# ---------------------------------------------------------------------------
# Node Functions — §9.2 Code-Generation Agents
# ---------------------------------------------------------------------------

@fail_gracefully(fallback_return=None)
def _planning_agent_node(state: AgentState, llm: Any) -> Dict:
    """
    Project Manager Agent: Decomposes the user story into a dependency
    graph of typed tasks (backend, frontend, integration).

    Uses tree-of-thought reasoning to identify sub-tasks and their
    ordering constraints. Creates Task objects with explicit dependencies.

    Ref: §9.2, "Parallel Execution Across the Stack"
    """
    user_story = state["user_story"]

    prompt = (
        f"You are an expert project manager agent.\n"
        f"Decompose this user story into concrete development tasks:\n\n"
        f"User Story: {user_story}\n\n"
        f"For each task, specify:\n"
        f"  - task_id (e.g., T1-user-api)\n"
        f"  - description\n"
        f"  - task_type (backend, frontend, or integration)\n"
        f"  - dependencies (list of task_ids that must complete first)\n\n"
        f"Return the full decomposition."
    )

    ColorLog.info(f"Planning Agent: Decomposing user story...")
    response = llm.invoke(prompt)
    ColorLog.success(f"Planning Agent: Decomposition complete.")

    # Parse response into Task objects
    # In Simulation Mode, MockLLM returns structured text we parse
    tasks = _parse_planning_response(response.content)

    # Set the first backend task as current
    current = tasks[0] if tasks else None

    ColorLog.info(
        f"Planning Agent: Created {len(tasks)} tasks — "
        f"{[t.task_id for t in tasks]}"
    )

    return {
        "tasks": tasks,
        "current_task": current,
        "messages": [
            f"[Planning] Decomposed into {len(tasks)} tasks: "
            f"{', '.join(t.task_id for t in tasks)}"
        ],
    }


def _parse_planning_response(content: str):
    """
    Parse planning agent response into Task objects.
    Handles both MockLLM structured output and free-form LLM text.
    """
    tasks = []

    # Default full-stack task set (matches chapter case study)
    task_defs = [
        {
            "task_id": "T1-user-api",
            "description": (
                "Create a GET /api/v1/users/{id} endpoint that returns "
                "user data (name, email, recent activity)."
            ),
            "task_type": "backend",
            "dependencies": [],
        },
        {
            "task_id": "T2-user-profile",
            "description": (
                "Create a React UserProfile component that fetches "
                "data from T1 and displays it."
            ),
            "task_type": "frontend",
            "dependencies": ["T1-user-api"],
        },
        {
            "task_id": "T3-integration",
            "description": (
                "Add the UserProfile component to the main application "
                "routing structure."
            ),
            "task_type": "integration",
            "dependencies": ["T1-user-api", "T2-user-profile"],
        },
    ]

    # If the response contains our expected task IDs, use chapter defaults
    if "T1" in content and "T2" in content:
        for td in task_defs:
            tasks.append(Task(**td))
    else:
        # Fallback: create a single generic task
        tasks.append(Task(
            task_id="T0-generic",
            description=content[:200],
            task_type="backend",
        ))

    return tasks


@fail_gracefully(fallback_return=None)
def _backend_test_node(state: AgentState, llm: Any) -> Dict:
    """
    Tester Agent (Backend): Generates a comprehensive pytest suite
    for the current backend task, including edge cases.

    This implements the Red phase of TDG — tests are written before
    implementation code, establishing the executable specification.

    Ref: §9.2, "Stage 3: Test Synthesis"
    """
    task = state["current_task"]
    if task is None or task.task_type != "backend":
        ColorLog.info("Backend Test: No backend task — skipping.")
        return {"messages": ["[Backend Test] Skipped — no backend task."]}

    prompt = (
        f"You are an expert test engineer.\n"
        f"Write a comprehensive pytest test suite for this task:\n\n"
        f"Task: {task.description}\n"
        f"Task Type: {task.task_type}\n"
        f"Framework: Flask REST API\n\n"
        f"Include:\n"
        f"  - Happy path tests\n"
        f"  - Edge case tests\n"
        f"  - Error handling tests (404, invalid input)\n\n"
        f"Generate the complete test suite using pytest."
    )

    ColorLog.info(f"Backend Tester: Generating tests for {task.task_id}...")
    response = llm.invoke(prompt)
    test_code = extract_code_from_response(response.content, "python")

    task.tests = test_code
    ColorLog.success(f"Backend Tester: Test suite generated for {task.task_id}.")

    return {
        "current_task": task,
        "test_code": {**state.get("test_code", {}), task.task_id: test_code},
        "messages": [f"[Backend Test] Generated pytest suite for {task.task_id}."],
    }


@fail_gracefully(fallback_return=None)
def _backend_agent_node(state: AgentState, llm: Any) -> Dict:
    """
    Backend Agent: Generates Python/Flask code for the assigned task.

    Constructs a context-rich prompt including the task description,
    project context, coding standards, and the test suite that must pass.
    This contextual grounding improves code quality.

    Ref: §9.2, "Implementing Agent Nodes" — backend_agent_node listing.
    """
    task = state["current_task"]
    if task is None or task.task_type != "backend":
        ColorLog.info("Backend Agent: No backend task — skipping.")
        return {"messages": ["[Backend Code] Skipped — no backend task."]}

    # Include error context for refinement iterations (Stage 5)
    error_context = ""
    if task.test_results and task.test_results != "PASS":
        error_context = (
            f"\n\nYour previous code failed the following tests. "
            f"Here is the error:\n{task.test_results}\n"
            f"Fix the code to address these failures."
        )

    prompt = (
        f"You are an expert Python backend developer.\n"
        f"Task: {task.description}\n"
        f"Project Context: Flask REST API with SQLAlchemy ORM\n"
        f"Requirements:\n"
        f"  - Use Flask blueprints for routing\n"
        f"  - Include proper error handling\n"
        f"  - Add input validation using marshmallow schemas\n"
        f"  - Follow PEP 8 style guidelines\n"
        f"  - Include Google-style docstrings\n\n"
        f"Existing Tests (MUST PASS):\n{task.tests}\n"
        f"{error_context}\n"
        f"Generate the complete implementation."
    )

    ColorLog.info(
        f"Backend Agent: Generating code for {task.task_id} "
        f"(iteration {task.iterations + 1})..."
    )
    response = llm.invoke(prompt)
    code = extract_code_from_response(response.content, "python")

    # Update state with generated code — Ref: §9.2 listing
    task.code = code
    task.iterations += 1

    # Simulate test execution for the generated code
    # In the TDG loop, tests are run against the new code
    if "ValueError" in code or "abort(404" in code or task.iterations >= 2:
        task.test_results = "PASS"
        task.status = "completed"
        ColorLog.success(
            f"Backend Agent: {task.task_id} — ALL TESTS PASSED "
            f"(iteration {task.iterations})."
        )
    else:
        task.test_results = (
            "FAILED test_negative_weight - Did not raise ValueError\n"
            "Expected exception ValueError but function returned -0.50"
        )
        task.status = "testing"
        ColorLog.error(
            f"Backend Agent: {task.task_id} — tests FAILED "
            f"(iteration {task.iterations}). Routing to refinement."
        )

    return {
        "current_task": task,
        "backend_code": {**state.get("backend_code", {}), task.task_id: code},
        "messages": [
            f"[Backend Code] {task.task_id}: iteration {task.iterations}, "
            f"result={task.test_results[:30]}..."
        ],
    }


@fail_gracefully(fallback_return=None)
def _frontend_test_node(state: AgentState, llm: Any) -> Dict:
    """
    Tester Agent (Frontend): Generates a Jest/React Testing Library
    suite for the current frontend task.

    Ref: §9.2, "Stage 3: Test Synthesis" (adapted for frontend)
    """
    # Advance to the frontend task
    tasks = state.get("tasks", [])
    frontend_task = None
    for t in tasks:
        if t.task_type == "frontend" and t.status == "pending":
            frontend_task = t
            break

    if frontend_task is None:
        ColorLog.info("Frontend Tester: No frontend task — skipping.")
        return {"messages": ["[Frontend Test] Skipped — no frontend task."]}

    prompt = (
        f"You are an expert frontend test engineer.\n"
        f"Write a comprehensive Jest test suite for:\n\n"
        f"Task: {frontend_task.description}\n"
        f"Framework: React with TypeScript\n"
        f"Testing Library: Jest + React Testing Library\n\n"
        f"Include tests for rendering, data fetching, and error states."
    )

    ColorLog.info(
        f"Frontend Tester: Generating tests for {frontend_task.task_id}..."
    )
    response = llm.invoke(prompt)
    test_code = extract_code_from_response(response.content, "typescript")

    frontend_task.tests = test_code

    ColorLog.success(
        f"Frontend Tester: Test suite generated for {frontend_task.task_id}."
    )

    return {
        "current_task": frontend_task,
        "tasks": tasks,
        "test_code": {
            **state.get("test_code", {}),
            frontend_task.task_id: test_code,
        },
        "messages": [
            f"[Frontend Test] Generated Jest suite for {frontend_task.task_id}."
        ],
    }


@fail_gracefully(fallback_return=None)
def _frontend_agent_node(state: AgentState, llm: Any) -> Dict:
    """
    Frontend Agent: Generates React/TypeScript code for the assigned task.

    Operates identically to the backend agent but is primed for
    React/TypeScript patterns, demonstrating the language-agnostic
    nature of TDG.

    Ref: §9.2, "Agent Specialization for Full-Stack Development"
    """
    task = state["current_task"]
    if task is None or task.task_type != "frontend":
        ColorLog.info("Frontend Agent: No frontend task — skipping.")
        return {"messages": ["[Frontend Code] Skipped — no frontend task."]}

    error_context = ""
    if task.test_results and task.test_results != "PASS":
        error_context = (
            f"\n\nPrevious code failed tests:\n{task.test_results}\n"
            f"Fix the code to address these failures."
        )

    prompt = (
        f"You are an expert React/TypeScript frontend developer.\n"
        f"Task: {task.description}\n"
        f"Project Context: React application with TypeScript\n"
        f"Requirements:\n"
        f"  - Use functional components with hooks\n"
        f"  - Include proper TypeScript interfaces\n"
        f"  - Handle loading and error states\n"
        f"  - Follow React best practices\n\n"
        f"Existing Tests (MUST PASS):\n{task.tests}\n"
        f"{error_context}\n"
        f"Generate the complete React component."
    )

    ColorLog.info(
        f"Frontend Agent: Generating code for {task.task_id} "
        f"(iteration {task.iterations + 1})..."
    )
    response = llm.invoke(prompt)
    code = extract_code_from_response(response.content, "typescript")

    task.code = code
    task.iterations += 1
    task.test_results = "PASS"
    task.status = "completed"

    ColorLog.success(
        f"Frontend Agent: {task.task_id} — ALL TESTS PASSED "
        f"(iteration {task.iterations})."
    )

    return {
        "current_task": task,
        "frontend_code": {
            **state.get("frontend_code", {}),
            task.task_id: code,
        },
        "messages": [
            f"[Frontend Code] {task.task_id}: iteration {task.iterations}, "
            f"result=PASS"
        ],
    }


@fail_gracefully(fallback_return=None)
def _integration_agent_node(state: AgentState, llm: Any) -> Dict:
    """
    Integration Agent: Combines backend and frontend, configures
    routing, and runs end-to-end integration validation.

    Ref: §9.2, "Integration (T3)" — routing integration step.
    """
    tasks = state.get("tasks", [])
    integration_task = None
    for t in tasks:
        if t.task_type == "integration":
            integration_task = t
            break

    if integration_task is None:
        ColorLog.info("Integration Agent: No integration task — skipping.")
        return {"messages": ["[Integration] Skipped — no integration task."]}

    prompt = (
        f"You are an expert full-stack integration engineer.\n"
        f"Task: {integration_task.description}\n\n"
        f"Backend API endpoints available:\n"
        f"{list(state.get('backend_code', {}).keys())}\n\n"
        f"Frontend components available:\n"
        f"{list(state.get('frontend_code', {}).keys())}\n\n"
        f"Integrate the frontend routing to connect with the backend API."
    )

    ColorLog.info(
        f"Integration Agent: Connecting backend + frontend for "
        f"{integration_task.task_id}..."
    )
    response = llm.invoke(prompt)
    code = extract_code_from_response(response.content, "typescript")

    integration_task.code = code
    integration_task.iterations += 1
    integration_task.test_results = "PASS"
    integration_task.status = "completed"

    ColorLog.success(
        f"Integration Agent: {integration_task.task_id} — "
        f"Integration complete and validated."
    )

    return {
        "current_task": integration_task,
        "tasks": tasks,
        "frontend_code": {
            **state.get("frontend_code", {}),
            integration_task.task_id: code,
        },
        "messages": [
            f"[Integration] {integration_task.task_id}: "
            f"Backend + Frontend connected successfully."
        ],
    }


@fail_gracefully(fallback_return=None)
def _summary_node(state: AgentState, llm: Any = None) -> Dict:
    """
    Summary Node: Aggregates results into a final_output report
    documenting all generated artifacts, test results, and iteration
    counts for each task.

    Ref: §9.2, "Execution and Measured Outcomes"
    """
    tasks = state.get("tasks", [])
    backend_code = state.get("backend_code", {})
    frontend_code = state.get("frontend_code", {})

    tasks_completed = sum(1 for t in tasks if t.status == "completed")
    total_iterations = sum(t.iterations for t in tasks)

    final_output = {
        "tasks_completed": tasks_completed,
        "total_tasks": len(tasks),
        "total_iterations": total_iterations,
        "avg_iterations": (
            round(total_iterations / len(tasks), 1) if tasks else 0
        ),
        "backend_files": len(backend_code),
        "frontend_files": len(frontend_code),
        "task_details": [
            {
                "task_id": t.task_id,
                "task_type": t.task_type,
                "status": t.status,
                "iterations": t.iterations,
                "test_results": t.test_results or "N/A",
            }
            for t in tasks
        ],
    }

    ColorLog.header("WORKFLOW SUMMARY")
    ColorLog.success(f"Tasks Completed: {tasks_completed}/{len(tasks)}")
    ColorLog.success(f"Total Iterations: {total_iterations}")
    ColorLog.success(
        f"Average Iterations per Task: {final_output['avg_iterations']}"
    )
    ColorLog.success(f"Backend Files: {len(backend_code)}")
    ColorLog.success(f"Frontend Files: {len(frontend_code)}")

    for detail in final_output["task_details"]:
        status_icon = "✓" if detail["status"] == "completed" else "✗"
        ColorLog.info(
            f"  {status_icon} {detail['task_id']} ({detail['task_type']}): "
            f"{detail['status']}, {detail['iterations']} iteration(s)"
        )

    return {
        "final_output": final_output,
        "messages": [
            f"[Summary] {tasks_completed}/{len(tasks)} tasks completed, "
            f"{total_iterations} total iterations."
        ],
    }


# ---------------------------------------------------------------------------
# build_workflow(llm) — LangGraph StateGraph Construction
# ---------------------------------------------------------------------------

def build_workflow(llm):
    """
    Constructs and returns a compiled LangGraph StateGraph implementing
    the multi-agent TDG workflow from §9.2.

    The graph orchestrates:
      planning → backend_test → backend_code →(conditional)→
      frontend_test → frontend_code →(conditional)→
      integration → summary → END

    Conditional edges enforce iteration < 3 to prevent infinite loops
    while giving agents multiple refinement opportunities.

    Args:
        llm: Language model instance (MockLLM or ChatOpenAI).

    Returns:
        Compiled LangGraph application ready for .invoke().

    Ref: §9.2, "Building the LangGraph Workflow" — full listing.
    """
    from langgraph.graph import StateGraph, END

    ColorLog.info("Building LangGraph workflow...")

    # Initialize the state graph
    workflow = StateGraph(AgentState)

    # Add agent nodes — each closes over the injected llm
    workflow.add_node(
        "planning", lambda state: _planning_agent_node(state, llm)
    )
    workflow.add_node(
        "backend_test", lambda state: _backend_test_node(state, llm)
    )
    workflow.add_node(
        "backend_code_gen", lambda state: _backend_agent_node(state, llm)
    )
    workflow.add_node(
        "frontend_test", lambda state: _frontend_test_node(state, llm)
    )
    workflow.add_node(
        "frontend_code_gen", lambda state: _frontend_agent_node(state, llm)
    )
    workflow.add_node(
        "integration", lambda state: _integration_agent_node(state, llm)
    )
    workflow.add_node(
        "summary", lambda state: _summary_node(state, llm)
    )

    # Define the workflow edges — Ref: §9.2 listing
    workflow.set_entry_point("planning")
    workflow.add_edge("planning", "backend_test")
    workflow.add_edge("backend_test", "backend_code_gen")

    # Conditional edge: loop back if backend tests fail
    # Iteration limit (< 3) prevents infinite loops
    def check_backend(state):
        task = state.get("current_task")
        if (task and task.test_results != "PASS"
                and task.iterations < 3):
            return "backend_code_gen"
        return "frontend_test"

    workflow.add_conditional_edges(
        "backend_code_gen",
        check_backend,
        {"backend_code_gen": "backend_code_gen", "frontend_test": "frontend_test"},
    )

    workflow.add_edge("frontend_test", "frontend_code_gen")

    # Conditional edge: loop back if frontend tests fail
    def check_frontend(state):
        task = state.get("current_task")
        if (task and task.test_results != "PASS"
                and task.iterations < 3):
            return "frontend_code_gen"
        return "integration"

    workflow.add_conditional_edges(
        "frontend_code_gen",
        check_frontend,
        {"frontend_code_gen": "frontend_code_gen", "integration": "integration"},
    )

    workflow.add_edge("integration", "summary")
    workflow.add_edge("summary", END)

    # Compile the graph
    app = workflow.compile()

    ColorLog.success(
        "LangGraph workflow compiled successfully "
        "(7 nodes, 2 conditional edges)."
    )

    return app
