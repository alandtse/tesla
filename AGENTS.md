# Tesla Custom Integration - AI Agent Guide

This file provides a comprehensive reference for AI agents and developers working with the Tesla Custom Integration codebase. It covers directory structure, component organization, key entry points, development tools, and patterns that deviate from standard Python/Home Assistant conventions.

---

## Quick Navigation

**For detailed documentation**, see files in `docs/`:

- **Architecture & Design**: `docs/architecture.md`
- **Components & Modules**: `docs/components.md`
- **APIs & Interfaces**: `docs/interfaces.md`
- **Data Models**: `docs/data_models.md`
- **Workflows & Processes**: `docs/workflows.md`
- **Dependencies**: `docs/dependencies.md`
- **Index**: `docs/index.md` (navigation guide)

---

## Directory Structure

```
tesla/
├── custom_components/tesla_custom/       # Main integration code
│   ├── __init__.py                       # Core: Setup, coordinator, config entry handling
│   ├── base.py                           # Entity base classes (TeslaBaseEntity, TeslaCarEntity, TeslaEnergyEntity)
│   ├── config_flow.py                    # Configuration UI (OAuth, options)
│   ├── const.py                          # Constants
│   ├── services.py                       # Custom Home Assistant services
│   ├── util.py                           # Utilities (SSL context)
│   ├── teslamate.py                      # TeslaMate MQTT integration (optional)
│   │
│   ├── sensor.py                         # Sensor entities (18 classes)
│   ├── binary_sensor.py                  # Binary sensors (12 classes)
│   ├── switch.py                         # Switches (5 classes)
│   ├── climate.py                        # Climate/HVAC (1 class)
│   ├── cover.py                          # Covers/doors/windows (5 classes)
│   ├── button.py                         # Buttons/actions (7 classes)
│   ├── lock.py                           # Locks (2 classes)
│   ├── select.py                         # Select/option entities (6 classes)
│   ├── number.py                         # Number/value setters (3 classes)
│   ├── device_tracker.py                 # Location tracking (2 classes)
│   ├── update.py                         # Software update entity (1 class)
│   ├── text.py                           # Text input (1 class)
│   │
│   ├── manifest.json                     # Home Assistant integration metadata
│   └── strings.json                      # Internationalization strings
│
├── tests/                                # Test suite (3500+ LOC)
│   ├── conftest.py                       # Pytest configuration
│   ├── common.py                         # Test utilities
│   ├── test_*.py                         # Test modules (one per entity type)
│   └── mock_data/                        # Mock Tesla API responses
│       ├── car.py
│       └── energysite.py
│
├── docs/                                 # Generated documentation
│   ├── index.md                          # Documentation index & navigation
│   ├── codebase_info.md                  # Project metadata
│   ├── architecture.md                   # System design
│   ├── components.md                     # Component breakdown
│   ├── interfaces.md                     # APIs & contracts
│   ├── data_models.md                    # Data structures
│   ├── workflows.md                      # Processes & flows
│   └── dependencies.md                   # External dependencies
│
├── config/                               # Development configuration
├── .devcontainer/                        # Docker dev container
├── .github/                              # GitHub workflows
├── .vscode/                              # VS Code settings
├── .pre-commit-config.yaml               # Git pre-commit hooks
├── .prospector.yml                       # Linting rules
├── pyproject.toml                        # Poetry project config
├── poetry.lock                           # Locked dependencies
├── manifest.json → (in custom_components/)
├── README.md                             # User guide
├── CONTRIBUTING.md                       # Contribution guidelines
├── CHANGELOG.md                          # Version history
├── LICENSE                               # Apache 2.0
└── AGENTS.md                             # This file
```

---

## Core Components

### 1. Main Entry Point: `__init__.py`

**Central Coordinator**: `TeslaDataUpdateCoordinator`

- Manages API client lifecycle
- Coordinates polling of all vehicles and energy sites
- Caches vehicle/site state
- Distributes updates to all entities
- Handles token refresh and persistence

**Setup Functions**:

- `async_setup()` - Platform initialization
- `async_setup_entry()` - Config entry setup (creates coordinator, starts entities)
- `async_unload_entry()` - Cleanup on removal

**Key Pattern**: All data flows through the coordinator; entities read from coordinator cache.

### 2. Entity Base Classes: `base.py`

**Hierarchy**:

```
TeslaBaseEntity
├── TeslaCarEntity (vehicle-specific)
└── TeslaEnergyEntity (energy site-specific)
```

**Key Provided**:

- Access to coordinator and vehicle/site data
- Device info and unique ID generation
- Update listener callback mechanism
- Home Assistant entity registration

**Usage**: All 59 entity classes inherit from these bases.

### 3. Platform Modules (Entity Types)

**Pattern**: Each file (e.g., `sensor.py`, `switch.py`) implements `async_setup_entry()` which creates entities for its domain.

**62 Total Entity Classes**:

- Sensors: 18 classes (battery, temperature, range, charging, etc.)
- Binary Sensors: 12 classes (online, charging, doors, etc.)
- Switches: 5 classes (charger, sentry, polling, etc.)
- Climate: 1 class (HVAC)
- Covers: 5 classes (frunk, trunk, windows, etc.)
- Buttons: 7 classes (horn, flash, wake, etc.)
- Locks: 2 classes (doors, charge port)
- Selects: 6 classes (seat heaters, operation modes)
- Numbers: 3 classes (charge limit, amps, reserve)
- Device Tracker: 2 classes (location, destination)
- Update: 1 class (software version)
- Text: 1 class (TeslaMate ID)

### 4. Configuration: `config_flow.py`

**Handles**:

- OAuth token authentication
- Account validation with Tesla API
- Integration options (polling interval, wake behavior, etc.)
- Token refresh on expiration

**Classes**: `TeslaConfigFlow`, `OptionsFlowHandler`

### 5. Support Modules

- **`teslamate.py`**: Optional MQTT sync from TeslaMate (real-time alternative to polling)
- **`services.py`**: Custom Home Assistant services for runtime configuration
- **`util.py`**: SSL context creation for API requests

---

## Home Assistant Integration Patterns

### Data Coordinator Pattern

The integration uses Home Assistant's `DataUpdateCoordinator`:

- Single instance per config entry manages all data fetching
- Caches data to avoid redundant API calls
- Notifies listening entities of changes
- Implements exponential backoff on errors

**Key Methods**:

- `_async_update_data()` - Fetch data from Tesla API
- `async_request_refresh()` - Force immediate update
- `async_update_listeners_debounced()` - Notify entities (debounced)

### Entity Framework

- All entities inherit from appropriate Home Assistant entity class (SensorEntity, SwitchEntity, etc.)
- No polling at entity level; coordinator handles all updates
- State persisted in Home Assistant state machine
- Unique IDs ensure stable entity registry

### Config Entry System

- Credentials stored securely in Home Assistant
- Per-entry setup/teardown
- Options flow for user configuration
- Device and entity registry integration

---

## Development Patterns

### Async/Await Throughout

- All I/O operations are async
- Uses `asyncio` with Home Assistant event loop
- No blocking calls

### Type Hints

- Type hints on all public methods/properties
- `mypy` used for static type checking
- Validates at pre-commit time

### Entity Naming Convention

- **Vehicle sensors**: `TeslaCar{EntityType}` (e.g., `TeslaCarBattery`)
- **Energy sensors**: `TeslaEnergy{EntityType}` (e.g., `TeslaEnergyBattery`)
- **Base class methods**: Inherit from `TeslaCarEntity` or `TeslaEnergyEntity`

### Data Access Pattern

```python
# In TeslaCarEntity subclass
battery_level = self.vehicle["response"]["charge_state"]["battery_level"]
```

### Update Pattern

```python
# Entity notified of coordinator update
async def _handle_coordinator_update(self) -> None:
    # Read new state from coordinator
    new_value = self.vehicle["response"]["charge_state"]["battery_level"]
    # Write to Home Assistant
    self.async_write_ha_state()
```

---

## Key Configuration Files

### `manifest.json`

- Home Assistant integration metadata
- Declares domain, dependencies, capabilities
- Specifies minimum Home Assistant version

### `pyproject.toml`

- Poetry project configuration
- Dependencies: `teslajsonpy` (custom fork), `async-timeout`
- Dev dependencies: pytest, black, mypy, prospector, bandit
- Black formatting: 88 char line length, Python 3.13 target

### `.pre-commit-config.yaml`

- Git hooks that run on commit
- Enforces: black formatting, mypy type checking, prospector linting, bandit security
- Prevents commits that don't pass checks

### `.prospector.yml`

- Comprehensive linting configuration
- Enforces code style and quality standards

---

## Build & Test Tools

### Running Tests

```bash
pytest                  # Run all tests
pytest --cov           # With coverage
pytest tests/test_sensor.py  # Single test file
```

### Code Formatting

```bash
black .                 # Format all files
black custom_components/  # Format integration only
```

### Type Checking

```bash
mypy .                  # Type check everything
mypy custom_components/tesla_custom/sensor.py  # Single file
```

### Comprehensive Linting

```bash
prospector              # Full analysis
bandit -r .             # Security scan
pydocstyle              # Docstring check
```

### Pre-commit (Automatic on Commit)

```bash
pre-commit run --all-files  # Run manually
pre-commit install          # Setup hooks
```

---

## Development Container

The project includes a Docker dev container (`.devcontainer/`):

- Isolated Home Assistant instance
- Pre-configured with integration
- Easy one-click setup in VS Code

**Usage**:

1. Install "Remote - Containers" extension in VS Code
2. Reopen folder in container
3. Home Assistant runs at `localhost:8123`

---

## Testing Infrastructure

### Test Structure

- Mock data in `tests/mock_data/` (car.py, energysite.py)
- Utility functions in `tests/common.py`
- Per-entity-type test files (test_sensor.py, test_switch.py, etc.)
- 3500+ LOC of test coverage

### Test Utilities

- `setup_platform()` - Set up integration for testing
- `setup_mock_controller()` - Create mock coordinator
- Fixtures for hass instance, config entry, mock vehicles

---

## Repository-Specific Tools & Patterns

### teslajsonpy Custom Fork

**Why**: Official library missing features needed by this integration
**Source**: `git+https://github.com/grzesiek1711/teslajsonpy.git@dev`
**What**: Includes additional Tesla API commands and features

### Polling Strategy

- Default polling interval: 660 seconds
- Respects vehicle sleep state to minimize battery drain
- Configurable polling policies: always, connected_only, conserve
- Optional TeslaMate MQTT sync for real-time updates

### Fleet API Proxy Support

- Some newer Tesla vehicles require Fleet API proxy
- Integration auto-detects and supports Tesla HTTP Proxy addon
- Configuration via integration options

### Vehicle Sleep Logic

- Coordinator tracks vehicle online/asleep state
- Doesn't wake vehicles during polling (preserves battery)
- Respects user setting: wake on HA start or let sleep

---

## Configuration & Options

### Setup Flow

1. User provides Tesla refresh token (from mobile app or web generator)
2. Token validated with Tesla API
3. Config entry created with encrypted token
4. Options form for polling configuration

### User Options

- **polling_interval**: Seconds between updates (60-3600, default 660)
- **wake_on_start**: Wake cars when HA starts (default: false)
- **polling_policy**: Sleep optimization strategy (default: always)
- **teslamate_enabled**: Enable MQTT sync (default: false)

---

## Home Assistant IoT Class

- **IoT Class**: `cloud_polling` (updates via cloud API polling)
- **Dependencies**: `http` (required for API calls)
- **After Dependencies**: `mqtt` (optional, for TeslaMate sync)
- **DHCP Discovery**: Yes (detects Tesla devices on network)

---

## Known Deviations from Defaults

1. **Custom Fork**: Uses `teslajsonpy` fork instead of official package
2. **Vehicle Sleep Logic**: Special handling to minimize battery drain (not typical)
3. **Optional MQTT Integration**: Can sync from TeslaMate MQTT topics
4. **Fleet API Proxy**: Support for Tesla HTTP Proxy addon (newer vehicles)

---

## Common Tasks for AI Agents

### Add a New Vehicle Sensor

1. Understand vehicle state schema in `docs/data_models.md`
2. Look at similar sensor in `sensor.py` as template
3. Create new sensor class inheriting from `TeslaCarEntity` and `SensorEntity`
4. Implement properties: `native_value`, `unit_of_measurement`, `device_class`
5. Add `async_setup_entry()` entry to register it
6. Write test in `tests/test_sensor.py`

### Fix a Data Coordination Bug

1. Review `docs/workflows.md` for polling flow
2. Check `__init__.py` TeslaDataUpdateCoordinator class
3. Review `docs/data_models.md` for data structure
4. Look at entity update pattern in relevant platform file

### Add a New Entity Type

1. Review `docs/components.md` for existing patterns
2. Choose appropriate Home Assistant entity class (Switch, Cover, Select, etc.)
3. Create new platform file (e.g., `new_platform.py`)
4. Implement entity classes inheriting from base + HA class
5. Implement `async_setup_entry()` for entity creation
6. Add tests in `tests/test_new_platform.py`

### Understand Integration Flow

1. Start with `docs/architecture.md` for system design
2. Review `docs/workflows.md` for integration setup flow
3. Check `docs/components.md` for coordinator pattern
4. Look at actual code in `__init__.py`

---

## Quick Reference: Key Files & Their Purpose

| File               | Lines | Purpose                                   |
| ------------------ | ----- | ----------------------------------------- |
| `__init__.py`      | 588   | Coordinator, setup, config entry handling |
| `base.py`          | 149   | Entity base classes                       |
| `config_flow.py`   | 314   | OAuth, config UI, options                 |
| `sensor.py`        | 668   | 18 sensor classes                         |
| `binary_sensor.py` | 300   | 12 binary sensor classes                  |
| `select.py`        | 460   | 6 select option classes                   |
| `switch.py`        | 189   | 5 switch classes                          |
| `cover.py`         | 209   | 5 cover/door classes                      |
| `climate.py`       | 173   | HVAC control                              |
| `button.py`        | 153   | 7 action button classes                   |
| `teslamate.py`     | 380   | MQTT integration                          |
| `services.py`      | 177   | Custom services                           |

---

## Integration Metadata

| Property           | Value         |
| ------------------ | ------------- |
| **Domain**         | tesla_custom  |
| **Version**        | 3.26.3        |
| **Min HA Version** | 2024.11.0     |
| **License**        | Apache-2.0    |
| **Maintainer**     | @alandtse     |
| **Python Version** | 3.13+         |
| **IoT Class**      | cloud_polling |

---

## Custom Instructions

<!-- This section is for human and agent-maintained operational knowledge.
     Add repo-specific conventions, gotchas, and workflow rules here.
     This section is preserved exactly as-is when re-running codebase-summary. -->
