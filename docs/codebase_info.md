# Tesla Custom Integration - Codebase Information

## Project Overview

**Name**: Tesla Custom Integration  
**Version**: 3.26.3  
**License**: Apache-2.0  
**Repository**: https://github.com/alandtse/tesla  
**Domain**: Home Assistant custom component for Tesla vehicles and energy sites

This is a fork of the official Home Assistant Tesla integration, maintained as a community project after the official integration was removed due to Tesla API login issues.

## Purpose

Provides comprehensive Home Assistant integration for:

- **Tesla Vehicles**: Real-time state, climate control, charging, vehicle commands
- **Energy Sites**: Powerwall status, solar generation, grid interaction, load management

The integration uses cloud polling with intelligent sleep strategies to minimize battery drain while keeping data current.

## Technology Stack

| Component      | Technology                         | Version/Source                |
| -------------- | ---------------------------------- | ----------------------------- |
| **Runtime**    | Python                             | ^3.13.2                       |
| **Framework**  | Home Assistant                     | >=2025.2.0                    |
| **API Client** | teslajsonpy                        | Custom fork (git branch: dev) |
| **Async**      | asyncio + async-timeout            | >=4.0.0                       |
| **Testing**    | pytest + Home Assistant test utils | >=0.13.107                    |

## Codebase Statistics

```
Total Files: 104
Primary Files: 41
Lines of Code: 8,713
Programming Language: Python (100%)

Component Breakdown:
- Core Integration: 19 Python modules
- Tests: 13 test modules
- Mock Data: 2 mock data modules
- Configuration: 5+ config/manifest files
```

## Directory Structure

```
tesla/
├── custom_components/tesla_custom/     # Main integration code
│   ├── __init__.py                     # Core coordinator & setup
│   ├── base.py                         # Entity base classes
│   ├── config_flow.py                  # Configuration UI
│   ├── const.py                        # Constants
│   ├── services.py                     # Custom services
│   ├── teslamate.py                    # TeslaMate MQTT integration
│   ├── util.py                         # Utilities (SSL context)
│   │
│   ├── sensor.py                       # Sensor entities
│   ├── binary_sensor.py                # Binary sensor entities
│   ├── switch.py                       # Switch entities
│   ├── climate.py                      # Climate entity
│   ├── cover.py                        # Cover entities
│   ├── button.py                       # Button entities
│   ├── lock.py                         # Lock entities
│   ├── select.py                       # Select entities
│   ├── number.py                       # Number entities
│   ├── device_tracker.py               # Device tracker entities
│   ├── update.py                       # Update entity
│   ├── text.py                         # Text entity
│   │
│   ├── manifest.json                   # Home Assistant manifest
│   └── strings.json                    # i18n strings (if exists)
│
├── tests/                              # Test suite
│   ├── conftest.py                     # Pytest configuration
│   ├── common.py                       # Test utilities
│   ├── test_*.py                       # Test modules (one per entity type)
│   └── mock_data/                      # Mock Tesla API responses
│       ├── car.py                      # Mock car data
│       └── energysite.py               # Mock energy site data
│
├── docs/                               # Documentation (this folder)
├── config/                             # Development configuration
├── .github/                            # GitHub workflows
├── .venv/                              # Python virtual environment
├── .vscode/                            # VS Code settings
│
├── pyproject.toml                      # Poetry project config
├── poetry.lock                         # Locked dependencies
├── manifest.json → (in custom_components/)
├── README.md                           # User guide
├── CONTRIBUTING.md                     # Development guide
├── CHANGELOG.md                        # Version history
├── LICENSE                             # Apache 2.0 license
└── info.md                            # Home Assistant display info
```

## Key Entry Points

### Integration Setup

- **File**: `custom_components/tesla_custom/__init__.py`
- **Entry Functions**:
  - `async_setup()` - Initial platform setup
  - `async_setup_entry()` - Configure a new integration entry
  - `async_unload_entry()` - Clean up integration
- **Main Class**: `TeslaDataUpdateCoordinator` - Manages all data fetching and state

### Configuration

- **File**: `custom_components/tesla_custom/config_flow.py`
- **Class**: `TeslaConfigFlow` - Handles user authentication and options
- **Process**: OAuth token acquisition → account validation → entity creation

### Entities

- **Base Classes** (`base.py`):
  - `TeslaBaseEntity` - Common functionality
  - `TeslaCarEntity` - Vehicle-specific
  - `TeslaEnergyEntity` - Energy site-specific

- **Platform Modules** (one per entity type):
  - Each implements `async_setup_entry()` to register entities
  - Uses `TeslaCarEntity` or `TeslaEnergyEntity` as base
  - Follows Home Assistant entity framework patterns

## Core Components

### TeslaDataUpdateCoordinator

The central hub for all data operations:

- Manages Tesla API client lifecycle
- Coordinates periodic polling of all vehicles/sites
- Handles vehicle wake-up and sleep logic
- Distributes updates to all listening entities
- Implements retry/backoff on API failures
- Supports TeslaMate MQTT sync as alternative to polling

### Entity Hierarchy

```
TeslaBaseEntity (common methods & properties)
├── TeslaCarEntity (vehicle-specific)
│   ├── Climate (HVAC control)
│   ├── Covers (frunk, trunk, windows, sunroof)
│   ├── Sensors (battery, temperature, range, etc.)
│   ├── Switches (charger, sentry, polling, etc.)
│   ├── Buttons (horn, flash, wake, etc.)
│   ├── Binary Sensors (charging, online, etc.)
│   ├── Locks (doors, charge port)
│   ├── Selects (seat heaters, overheat protection)
│   ├── Numbers (charge limit, amps)
│   ├── Device Tracker (location)
│   ├── Update (software version)
│   └── Text (TeslaMate ID)
│
└── TeslaEnergyEntity (Powerwall-specific)
    ├── Sensors (power, battery, reserve)
    ├── Switches (modes)
    └── Selects (operation modes)
```

## Development Tools & Configuration

### Build & Testing

```bash
poetry install              # Install dependencies
pytest                     # Run test suite
pytest --cov              # With coverage
black .                   # Format code
mypy .                    # Type checking
prospector                # Full linting
```

### Pre-commit Hooks

- File: `.pre-commit-config.yaml`
- Hooks: black, mypy, prospector, bandit (security)
- Runs automatically on commit

### Configuration Files

- `pyproject.toml` - Poetry dependencies, pytest, black, mypy config
- `.prospector.yml` - Linting rules
- `manifest.json` - Home Assistant integration metadata
- `.pre-commit-config.yaml` - Git hooks

## Home Assistant Integration Details

| Property               | Value                       |
| ---------------------- | --------------------------- |
| **Domain**             | tesla_custom                |
| **IoT Class**          | cloud_polling               |
| **Config Flow**        | Yes (OAuth-based)           |
| **Dependencies**       | http                        |
| **After Dependencies** | mqtt                        |
| **Import Executor**    | Yes                         |
| **Min HA Version**     | 2024.11.0                   |
| **DHCP Discovery**     | Yes (Tesla network devices) |

## Dependencies & Versions

### Runtime Dependencies

- **teslajsonpy** (custom fork) - Tesla API client library
  - Source: `git+https://github.com/grzesiek1711/teslajsonpy.git@dev`
  - Provides: OAuth, API endpoints, vehicle/site data structures
- **async-timeout** >=4.0.0 - Timeout management for async operations

### Dev Dependencies

- **pytest** + **pytest-homeassistant-custom-component** - Testing framework
- **pytest-asyncio**, **pytest-httpx** - Async and HTTP mocking
- **black**, **mypy**, **prospector** - Code quality
- **bandit** - Security scanning
- **pre-commit** - Git hooks

## Build & Release

### Version Management

- Version sources: `pyproject.toml`, `custom_components/tesla_custom/const.py`, `manifest.json`
- Automated via semantic-release on git tags
- Changelog sections: feature, fix, breaking, documentation, performance, refactor

### Distribution

- **HACS**: Home Assistant Community Store listing
- **Release**: GitHub releases with zip archives
- **No PyPI**: Project-mode in poetry (not published to PyPI)

## Known Configuration

### CI/CD

- GitHub Actions workflows in `.github/workflows/`
- Semantic versioning with automated changelog

### VS Code

- Configuration in `.vscode/` for workspace settings
- Recommended extensions for Python/Home Assistant development

### Development Container

- Config: `.devcontainer.json`
- Optional: Use for isolated development environment

## API & External Integrations

### Tesla API (via teslajsonpy)

- OAuth 2.0 token-based authentication
- REST API for vehicle commands and state
- Polling interval configurable (default: 660 seconds)
- Supports optional Tesla HTTP Proxy for Fleet API compatibility

### MQTT Integration (via TeslaMate)

- Optional syncing from TeslaMate MQTT topics
- Provides real-time updates alternative to polling
- Requires MQTT configured in Home Assistant

### Home Assistant Framework

- Entity creation and lifecycle management
- Config entry system for credential storage
- Data coordinator pattern for update coordination
- Service registration for custom commands

---

**Integration Class**: Home Assistant Custom Component  
**Code Quality**: Type hints throughout, async/await patterns, comprehensive tests  
**Maintenance**: Active (version 3.26.3 as of latest documentation)
