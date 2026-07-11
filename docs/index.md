# Tesla Custom Integration - Documentation Index

**Purpose**: This index guides AI assistants and developers through the codebase documentation. Use the file descriptions and relationships below to locate relevant information for your task.

**Quick Links for Common Questions**:

- _"How does the integration work?"_ → `architecture.md`
- _"Where is [component] implemented?"_ → `components.md`
- _"What are the API/interfaces?"_ → `interfaces.md`
- _"What data structures are used?"_ → `data_models.md`
- _"How does [process] work?"_ → `workflows.md`
- _"What are the dependencies?"_ → `dependencies.md`
- _"General codebase metrics and info"_ → `codebase_info.md`

---

## Documentation File Reference

### 1. **codebase_info.md**

**Purpose**: High-level project metadata and codebase statistics
**Contains**:

- Project summary and purpose
- Technology stack and language info
- File structure overview
- Key statistics (files, lines of code, components)
- Version and licensing info
- Build and test tooling

**Use when**: You need general project context or want to understand what tools are in use

---

### 2. **architecture.md**

**Purpose**: System design patterns, architectural decisions, and design principles
**Contains**:

- Overall system architecture and data flow
- Integration design with Home Assistant
- Data coordination and polling strategy
- Entity lifecycle and state management
- Configuration flow and setup process
- Error handling and resilience patterns
- Home Assistant-specific patterns and conventions

**Use when**: You need to understand how the system is designed or how major components interact

---

### 3. **components.md**

**Purpose**: Detailed breakdown of all major components and their responsibilities
**Contains**:

- Core coordinator (`TeslaDataUpdateCoordinator`)
- Base entity classes and hierarchy
- Platform modules (entities by domain):
  - Sensors (battery, charging, temperature, etc.)
  - Switches (charger, sentry, polling, etc.)
  - Climate control
  - Covers (frunk, trunk, windows, etc.)
  - Buttons (actions)
  - Binary sensors (state indicators)
  - Locks (door and charge port)
  - Selects (options)
  - Numbers (numeric controls)
  - Device tracker (location)
  - Updates (software version)
  - Text (configuration)
- Support modules (config flow, TeslaMate, services)
- Responsibility matrix

**Use when**: You need to find or understand a specific component or entity type

---

### 4. **interfaces.md**

**Purpose**: Public APIs, interfaces, and integration points
**Contains**:

- Entity base class interfaces and contracts
- Coordinator interface and lifecycle hooks
- Config flow interface and validation
- Service definitions and async API
- TeslaMate MQTT integration interface
- External API consumption (Tesla API via teslajsonpy)
- Data contracts and type hints
- Home Assistant event/entity framework integration

**Use when**: You need to understand how to interact with a component or what methods are available

---

### 5. **data_models.md**

**Purpose**: Data structures, models, and type definitions
**Contains**:

- Entity data models (attributes, state types)
- Coordinator data state management
- Configuration data structures
- Car state schema (from Tesla API)
- Energy site state schema (Powerwall)
- TeslaMate state mappings
- Type hints and validation patterns

**Use when**: You need to understand data flow or what data structures hold

---

### 6. **workflows.md**

**Purpose**: Key processes, workflows, and execution flows
**Contains**:

- Integration setup and initialization flow
- Device discovery and entity creation
- Data polling and update coordination
- Command execution workflow (lock, climate, etc.)
- Configuration options flow
- TeslaMate synchronization flow
- Device removal and cleanup
- Error recovery workflows

**Use when**: You need to trace how a specific process executes or understand a workflow

---

### 7. **dependencies.md**

**Purpose**: External dependencies and their usage in the codebase
**Contains**:

- Python dependencies (with versions and git sources)
- Home Assistant framework usage
- teslajsonpy library integration
- Development and testing dependencies
- Pre-commit hooks and linting setup
- Build and release automation tools

**Use when**: You need to understand external dependencies or versions

---

## Navigation Patterns

### By Task Type

**Adding a new entity type**:

1. Read `components.md` to see existing entity patterns
2. Check `interfaces.md` for entity base class contracts
3. Review `workflows.md` for entity creation flow
4. Look at a similar entity in components for implementation template

**Fixing a bug in data coordination**:

1. Start with `workflows.md` for update flow
2. Review `components.md` for `TeslaDataUpdateCoordinator`
3. Check `data_models.md` for data contracts
4. Look at `architecture.md` for design patterns

**Integrating new data source or API**:

1. Review `interfaces.md` for API integration patterns
2. Check `dependencies.md` for external libraries
3. Look at `workflows.md` for data flow
4. Review `architecture.md` for design principles

**Understanding configuration**:

1. Read `components.md` for config flow implementation
2. Check `workflows.md` for config options flow
3. Review `interfaces.md` for validation contracts

### By Component

**Coordinator & Data Flow**: `components.md` → `workflows.md` → `architecture.md`

**Entities**: `components.md` (specific entity) → `interfaces.md` (base class) → `data_models.md` (data)

**Configuration**: `components.md` (config_flow.py) → `workflows.md` (setup flow) → `interfaces.md` (validation)

**Integration**: `architecture.md` (design) → `components.md` (implementation) → `dependencies.md` (libs used)

---

## Home Assistant Context

This integration follows Home Assistant custom component conventions:

- **Domain**: `tesla_custom`
- **IoT Class**: Cloud polling
- **Async Pattern**: Event-driven async/await throughout
- **Entity Framework**: Inherits from Home Assistant entity platform classes
- **Data Coordination**: Uses Home Assistant `DataUpdateCoordinator` for update management
- **Config Flow**: Implements Home Assistant config entry system

See `architecture.md` for Home Assistant-specific patterns and `components.md` for framework integration points.

---

## File Organization

```
docs/
├── index.md (this file)
├── codebase_info.md
├── architecture.md
├── components.md
├── interfaces.md
├── data_models.md
├── workflows.md
└── dependencies.md

Root-level consolidated files:
├── AGENTS.md (comprehensive AI agent guide)
├── README.md (user documentation)
└── CONTRIBUTING.md (development guide)
```

---

## How to Use This Documentation

1. **For specific questions**: Use the "Quick Links" at the top
2. **For exploring a component**: Start with `components.md`, then drill down to `interfaces.md` and `data_models.md` as needed
3. **For understanding processes**: Read `workflows.md` for execution flow, then check `architecture.md` for design context
4. **For adding features**: Follow the "Adding" section in Navigation Patterns above
5. **For external tools/libs**: Check `dependencies.md`

Each file is designed to be self-contained but cross-references related documents for deeper dives. Start with the files most relevant to your task and drill down as needed.

---

**Last Updated**: Generated for Tesla Custom Integration v3.26.3
**Focus**: Home Assistant custom component with cloud polling, supporting Tesla vehicles and energy sites
