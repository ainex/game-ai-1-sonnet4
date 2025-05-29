# Here's a structured and technically precise flow of how AI agents and LLMs are used in software engineering on a large enterprise project

## AI-Assisted Software Development Workflow for Large Enterprise Projects

This workflow outlines a systematic approach to leveraging AI agents and Large Language Models (LLMs) for feature implementation in a complex enterprise software project (approximately 100,000 lines of backend code with legacy architectural layers). The core principle is to create a detailed, AI-augmented implementation plan that serves as a single source of truth during development.

**Project Context & Prerequisites:**

* **Existing Codebase:** ~100,000 lines of code (backend only).
* **Architectural Complexity:** Contains "archaeological layers" (legacy code/design).
* **Documentation Standards:**
    * A general structural guideline with a high-level project description exists.
    * Deprecated modules contain a `DEPRECATED.md` file, outlining alternatives to adding new submodules.
    * Each module has a `README.md` describing its purpose and usage.

**Workflow Steps:**

1.  **Initial Feature Understanding & General Solution Design:**
    * **Action:** Before implementing a new feature, collaboratively with AI agents, develop a `IMPLEMENTATION_PLAN.md` document.
    * **Sub-step 1 (General Solution - `sd`):** Describe the general solution approach for the new feature within the `IMPLEMENTATION_PLAN.md`.

2.  **Codebase Analysis & Dependency Mapping (AI-Assisted):**
    * **Action:** Instruct the AI agents to identify all relevant existing code segments within the codebase related to the proposed feature.
    * **Output:** The agents generate a "dependencies and dependants investigation" section within the `IMPLEMENTATION_PLAN.md`, listing relevant files and their relationships.

3.  **Detailed Implementation Plan Generation (AI-Assisted):**
    * **Action:** Request the AI agents to synthesize the general solution and the dependency analysis into a concrete, step-by-step action plan.
    * **Output:** This forms the "implementation plan, finally" section of the `IMPLEMENTATION_PLAN.md`. The resulting document is highly detailed (potentially 1000+ lines).

4.  **(Optional) Test and Documentation Planning (AI-Assisted):**
    * **Action:** If desired, repeat the process (steps 1-3 conceptually) for planning tests and documentation related to the feature.
    * **Output:** Detailed plans for testing and documentation, potentially integrated into or supplementing the `IMPLEMENTATION_PLAN.md`.

5.  **AI-Driven Implementation:**
    * **Action:** Instruct the AI agent to proceed with the actual code implementation based on the super-detailed `IMPLEMENTATION_PLAN.md`.
    * **Flexibility:** Implementation can start with either test development (Test-Driven Development) or code development.
    * **Benefit:** The `IMPLEMENTATION_PLAN.md` serves as a "single source of truth" throughout the implementation phase, simplifying the process.

6.  **Post-Implementation Documentation & Cleanup:**
    * **Action 1:** Extract a summary of the implementation details into the relevant module's `README.md` file. This could potentially be AI-assisted.
    * **Action 2:** Delete the `IMPLEMENTATION_PLAN.md` as it is no longer needed after successful implementation and documentation update.

**Outcome:**

* Significant acceleration of feature development (e.g., a feature previously taking a full sprint can be implemented in a single day).
* Improved clarity and reduced ambiguity during implementation due to the detailed plan.
