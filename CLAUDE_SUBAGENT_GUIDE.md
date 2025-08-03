# Claude Subagent Development Guide

## Based on Successful Analysis of Game AI Assistant Project

This guide documents the successful actions and decision-making process used to analyze and plan improvements for the Game AI Assistant project. Use these patterns to build effective Claude subagents.

## Core Principles

### 1. Systematic Approach
- **Always use TodoWrite** to track progress and ensure nothing is missed
- Break complex tasks into manageable steps
- Complete one task before moving to the next
- Mark tasks as completed immediately after finishing

### 2. Information Gathering Strategy
```python
# Optimal order for understanding a project:
1. Read CLAUDE.md / AGENTS.md (project-specific instructions)
2. Read README.md (project overview) 
3. Check for IMPLEMENTATION_PLAN.md files
4. Examine project structure with LS/Glob
5. Read key source files (main.py, core services)
6. Analyze requirements.txt for dependencies
```

### 3. Parallel Tool Usage
Always batch related tool calls for efficiency:
```xml
<function_calls>
  <invoke name="Read">
    <parameter name="file_path">CLAUDE.md</parameter>
  </invoke>
  <invoke name="Read">
    <parameter name="file_path">requirements.txt</parameter>
  </invoke>
  <invoke name="Glob">
    <parameter name="pattern">**/*.py</parameter>
  </invoke>
</function_calls>
```

## Analysis Decision Tree

### Step 1: Initial Context Gathering
```python
def gather_initial_context():
    """First actions when analyzing any project."""
    # 1. Create todo list
    todos = [
        "Analyze project structure and documentation",
        "Review implemented features vs expected functionality", 
        "Create/update implementation plan for missing features",
        "Document successful actions and decision-making process"
    ]
    
    # 2. Read key documents in parallel
    files_to_read = [
        "CLAUDE.md",        # Project-specific instructions
        "README.md",        # Project overview
        "requirements.txt", # Dependencies
        "AGENTS.md"         # Development guidelines
    ]
    
    # 3. Explore structure
    patterns_to_glob = [
        "**/*.py",          # All Python files
        "**/README.md",     # All READMEs
        "**/*PLAN*.md"      # Implementation plans
    ]
```

### Step 2: Deep Dive Analysis
```python
def analyze_implementation():
    """Analyze what's actually implemented."""
    # 1. Identify entry points
    key_files = [
        "server/src/main.py",     # Server entry
        "client/src/main.py",     # Client entry
        "server/src/services/*",  # Core services
        "server/src/api/endpoints/*" # API endpoints
    ]
    
    # 2. Compare against documentation
    # - Expected features from README/CLAUDE.md
    # - Actual implementation in code
    # - Missing components
    
    # 3. Check for patterns
    # - Service layer abstraction
    # - Error handling consistency
    # - Testing coverage
```

### Step 3: Gap Analysis
```python
def identify_gaps():
    """Systematic gap identification."""
    categories = {
        "fully_implemented": [],    # ✅ Working features
        "partially_implemented": [], # ⚠️ Needs work
        "not_implemented": []       # ❌ Missing completely
    }
    
    # For each expected feature:
    # 1. Check if code exists
    # 2. Verify it's connected/used
    # 3. Test if it actually works
    # 4. Categorize appropriately
```

## Successful Patterns Used

### 1. Document Structure
When creating analysis reports:
```markdown
# Title
## Executive Summary
## Architecture Overview
### Planned Architecture
### Current Architecture
## Feature Comparison: Expected vs Implemented
### ✅ Fully Implemented Features
### ⚠️ Partially Implemented Features  
### ❌ Not Implemented Features
## Implementation Gaps Analysis
## Recommendations
```

### 2. Implementation Planning
When creating implementation plans:
```markdown
# Implementation Plan Phase X: Description
## Overview
## Phase X.1: Component Name (Priority)
### 1. Sub-component
### 2. Sub-component
## Implementation Timeline
### Week 1
- [ ] Task 1
- [ ] Task 2
## Success Criteria
## Risk Mitigation
```

### 3. Code Reading Strategy
```python
# 1. Start with imports to understand dependencies
# 2. Look for class/function definitions
# 3. Identify patterns (decorators, inheritance)
# 4. Check error handling
# 5. Note configuration/environment usage
```

## Key Decision Points

### When to Create New Files
1. **Analysis Report**: When comparing expected vs actual
2. **Implementation Plan**: When identifying missing features
3. **Guide Document**: When documenting patterns for reuse

### When to Use Specific Tools
- **TodoWrite**: Always at task start and completion
- **Read**: For understanding existing code/docs
- **Write**: For creating new documentation
- **Edit**: For updating existing files
- **Glob**: For discovering file patterns
- **LS**: For understanding directory structure

## Communication Patterns

### 1. Progress Updates
- Use TodoWrite to show current task
- Brief status messages during long operations
- Clear completion messages

### 2. Report Writing
- Executive summary first
- Use clear section headers
- Emoji indicators (✅ ⚠️ ❌) for status
- Concrete examples with code snippets

### 3. Technical Accuracy
- Quote actual file paths and line numbers
- Show exact error messages
- Reference specific functions/classes

## Common Pitfalls to Avoid

1. **Don't skip TodoWrite** - It's essential for tracking
2. **Don't read files sequentially** - Batch operations
3. **Don't make assumptions** - Verify in actual code
4. **Don't create files without need** - Only when valuable
5. **Don't forget to complete todos** - Mark done immediately

## Subagent Prompt Template

```
You are a Claude subagent specialized in [DOMAIN].

Your primary responsibilities:
1. [Responsibility 1]
2. [Responsibility 2]
3. [Responsibility 3]

Follow these patterns:
- Always use TodoWrite for task tracking
- Batch tool calls for efficiency
- Create clear, structured documentation
- Verify assumptions with actual code
- Communicate progress clearly

When analyzing projects:
1. Start with CLAUDE.md/README.md
2. Identify key components
3. Compare expected vs actual
4. Document gaps systematically
5. Propose actionable solutions

Remember: Be systematic, thorough, and clear in communication.
```

## Example Successful Analysis Flow

1. **Started with TodoWrite** to track 4 main tasks
2. **Batch read** CLAUDE.md, README.md, requirements.txt
3. **Explored structure** with LS and Glob
4. **Deep dove** into main.py files and services
5. **Compared** documentation promises vs implementation
6. **Created report** with clear categorization
7. **Developed plan** with prioritized phases
8. **Documented patterns** for future use

This systematic approach ensures nothing is missed and provides clear, actionable output for users.