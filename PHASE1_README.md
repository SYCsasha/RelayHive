# RelayHive - AI Work Order System Module

## Phase 1: Foundation Implementation

This module implements Phase 1 of the AI Work Order System for RelayHive - a foundational layer that enables AI agents to issue, claim, and relay work orders to each other.

### 📋 Project Structure

```
app/
├── main.py                    # FastAPI application entry point
├── config.py                  # Configuration management
├── core/
│   ├── enums.py              # Status and type enumerations
│   └── __init__.py
├── db/
│   ├── base.py               # Database connection and Base class
│   └── __init__.py
├── models/
│   ├── ai_agent.py           # AI agent and capability models
│   ├── work_order.py         # Work order and tag models
│   ├── relay_history.py      # Relay step tracking
│   ├── result_package.py     # Result package and outputs
│   ├── relay_metrics.py      # Performance metrics
│   └── __init__.py
├── schemas/
│   ├── ai_agent.py           # AI agent Pydantic schemas
│   ├── work_order.py         # Work order Pydantic schemas
│   ├── result_package.py     # Result package Pydantic schemas
│   └── __init__.py
├── services/
│   ├── tag_service.py        # Tag protocol parsing and matching
│   ├── work_order_service.py # Work order business logic
│   ├── result_package_service.py  # Result package operations
│   └── __init__.py
└── api/
    ├── routes/
    │   ├── health.py         # Health check endpoint
    │   ├── ai_agents.py      # AI agent management endpoints
    │   ├── work_orders.py    # Work order management endpoints
    │   └── __init__.py
    └── __init__.py

tests/
├── conftest.py               # Test configuration and fixtures
├── test_tag_service.py       # Tag service tests
├── test_work_order_service.py  # Work order service tests
├── test_api_endpoints.py     # API endpoint tests
└── __init__.py

requirements.txt              # Python dependencies
pytest.ini                   # Pytest configuration
pyproject.toml               # Project metadata
```

### 🚀 Getting Started

#### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# For development with tests
pip install -r requirements.txt pytest pytest-asyncio httpx
```

#### Environment Setup

```bash
# Copy example environment
cp .env.example .env

# Edit .env with your configuration
# - Set DATABASE_URL to your PostgreSQL connection string
# - Set REDIS_URL for event bus (optional for Phase 1)
```

#### Running the Application

```bash
# Start the development server
uvicorn app.main:app --reload

# Server will be available at http://localhost:8000
# API documentation: http://localhost:8000/docs
```

#### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_tag_service.py -v
```

### 📊 Core Components

#### 1. **Work Order Model**
- Extends the RelayHive Task concept for AI-only execution
- Tracks issuer, current claim, relay history, and result packages
- Maintains immutable relay chain for auditability

#### 2. **Tag Protocol Service**
- Parses tags in format: `#<weight>_<semantic>[.<suffix>]`
- Matches tags to AI agent capabilities
- Detects conflicts and provides priority ordering

#### 3. **Work Order Service**
- Creates work orders issued by Main AI
- Handles claiming by worker AIs
- Manages rejection and escalation
- Queries available work based on agent capabilities
- Maintains relay step history

#### 4. **Result Package Service**
- Publishes versioned result packages
- Tracks execution logs and API calls
- Manages output artifacts
- Calculates retention periods

#### 5. **AI Agent Registry**
- Stores AI agent capabilities and constraints
- Manages agent configuration
- Tracks concurrent task limits

### 🔌 API Endpoints (Phase 1)

#### Health Check
- `GET /health` - Health check

#### AI Agent Management
- `POST /v1/ai-agents` - Register new AI agent
- `GET /v1/ai-agents` - List all agents
- `GET /v1/ai-agents/{agent_id}` - Get agent details
- `PUT /v1/ai-agents/{agent_id}` - Update agent
- `DELETE /v1/ai-agents/{agent_id}` - Remove agent

#### Work Order Management (for Main AI)
- `POST /v1/workorders` - Issue new work order

#### Work Order Management (for Worker AIs)
- `GET /v1/workorders/available?agent_id=<id>` - Query available work
- `POST /v1/workorders/{id}/claim` - Claim work order
- `POST /v1/workorders/{id}/start` - Start execution
- `POST /v1/workorders/{id}/publish-result` - Publish result package
- `POST /v1/workorders/{id}/reject` - Reject work order

#### Work Order Management (for Humans - Read Only)
- `GET /v1/workorders` - List all work orders
- `GET /v1/workorders/{id}` - Get work order details
- `GET /v1/workorders/{id}/relay-chain` - Get relay history

### 📈 Data Models

#### WorkOrder
```python
{
  "work_order_id": "wo_20260522_abc123",
  "title": "Analyze User Requirements",
  "description": "...",
  "issuer_agent_id": "main_ai",
  "claiming_agent_id": "analysis_ai",  # null until claimed
  "status": "in_progress",  # created, claimed, in_progress, etc.
  "priority_level": 1,      # 1=highest, 5=lowest
  "tags": [                 # Tag protocol
    {"tag_text": "#1_analysis_required", "weight": 1, ...},
    {"tag_text": "#2_context_history_needed", "weight": 2, ...}
  ],
  "relay_chain_depth": 0,
  "max_relay_depth": 10,
  "estimated_complexity": 45.5,
  "created_at": "2026-05-22T11:43:52Z",
  "updated_at": "2026-05-22T12:10:00Z"
}
```

#### ResultPackage
```python
{
  "package_id": "pkg_wo_20260522_abc123_v1",
  "version": 1,
  "producer_agent_id": "analysis_ai",
  "qa_summary": {"passed": true, "notes": "Initial analysis complete"},
  "confidence_score": 0.92,
  "next_tags": ["#2_design_needed"],
  "execution_log": "...",
  "checksum": "sha256:...",
  "created_at": "2026-05-22T12:10:00Z"
}
```

### 🏗️ Tag Protocol Examples

**Functional Tags** (What capability is needed):
- `#1_analysis_required` - Analysis AI should handle
- `#2_design_needed` - Design AI should handle
- `#2_implementation_needed` - Coding AI should handle
- `#3_testing_required` - QA AI should handle

**Behavioral Tags** (Constraints):
- `#2_no_external_api_calls` - Must not call external APIs
- `#1_requires_context_history` - Needs full project history

**Process Tags** (Workflow stage):
- `#3_waiting_for_review` - Pending review
- `#1_human_review_only` - Final human observation

### 🔄 Typical Work Order Flow

```
1. Main AI Issues Work Order
   POST /v1/workorders
   - Provides title, description, tags, requirements
   
2. Worker AI Discovers Work
   GET /v1/workorders/available?agent_id=worker_ai
   - Lists unclaimed orders matching its capabilities
   
3. Worker AI Claims Work
   POST /v1/workorders/{id}/claim
   - Commits to execution
   
4. Worker AI Executes
   POST /v1/workorders/{id}/start
   - Performs actual work
   
5. Worker AI Publishes Result
   POST /v1/workorders/{id}/publish-result
   - Submits versioned output with next_tags
   - Specifies next AI to handle (if relay needed)
   
6. Human Observes (Read-only)
   GET /v1/workorders/{id}/relay-chain
   - Views complete execution history
   - No permission to modify or submit work
```

### 🧪 Testing

Tests cover:
- **Tag parsing** - Verify tag format and weight parsing
- **Tag matching** - Capability-to-tag alignment
- **Work order lifecycle** - Create, claim, execute, complete
- **Relay chain** - Multi-step work order progression
- **API endpoints** - All HTTP operations

Example test run:
```bash
$ pytest -v tests/test_tag_service.py
tests/test_tag_service.py::test_parse_tag_valid PASSED
tests/test_tag_service.py::test_parse_tag_with_suffix PASSED
tests/test_tag_service.py::test_match_tags_to_capabilities PASSED
```

### 📝 Configuration

Key settings in `app/config.py`:
- `DATABASE_URL` - PostgreSQL connection
- `REDIS_URL` - Redis for event bus
- `MAX_RELAY_CHAIN_DEPTH` - Prevent infinite loops (default: 10)
- `WORK_ORDER_RETENTION_DAYS` - Keep results (default: 7)

### 🔗 Integration Points

Phase 1 prepares for integration with:
- **Event Bus** - Phase 2 will publish work order events
- **Main AI Translator** - Phase 2 will add disambiguation support
- **Human Dashboard** - Phase 4 will build visualization

### 📚 Next Phases

- **Phase 2**: AI-to-AI Communication + Event Bus integration
- **Phase 3**: Relay Chain Management + Auto-routing
- **Phase 4**: Human Observation Dashboard
- **Phase 5**: Integration & Testing

### ⚠️ Known Limitations (Phase 1)

- SQLite used in tests; PostgreSQL required for production
- No Event Bus integration yet (Phase 2)
- No automatic relay routing (Phase 2)
- No human dashboard (Phase 4)
- No cost tracking yet (Phase 3)

### 🛠️ Development Notes

- All timestamps in UTC
- Work order IDs: `wo_YYYYMMDD_<8-char-hex>`
- Package IDs: `pkg_<work_order_id>_v<version>`
- Tags follow weight-priority scheme: 1 (highest) to 5 (lowest)

### 📄 License

See LICENSE file in repository root.
