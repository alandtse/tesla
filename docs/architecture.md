# Tesla Custom Integration - System Architecture

## High-Level System Design

The Tesla Custom Integration follows the **Data Coordinator Pattern** with **Cloud Polling Strategy**, implemented within Home Assistant's async entity framework.

```mermaid
graph TB
    HA["Home Assistant Core"]
    CF["Config Flow<br/>OAuth Setup"]
    TDC["TeslaDataUpdateCoordinator<br/>Central Hub"]
    TAC["Tesla API Client<br/>teslajsonpy"]

    Entities["Entity Platforms<br/>Sensors, Switches, Climate, etc."]

    HA --> CF
    CF --> TDC
    HA --> Entities
    TDC --> Entities
    TDC --> TAC
    TAC --> TeslaCloud["Tesla Cloud API"]

    TeslaMate["TeslaMate MQTT<br/>Alternative Data Source"]
    TDC -.-> TeslaMate
```

## Architecture Layers

### 1. Setup & Configuration Layer

**Entry Point**: `async_setup()` and `async_setup_entry()`

```mermaid
sequenceDiagram
    participant User
    participant ConfigFlow
    participant Coordinator
    participant TeslaAPI
    participant Entities

    User->>ConfigFlow: Add Integration
    ConfigFlow->>TeslaAPI: Authenticate (OAuth token)
    ConfigFlow->>Coordinator: Initialize with tokens
    Coordinator->>TeslaAPI: Fetch vehicles/sites
    Coordinator->>Entities: Create entity instances
    Entities->>User: Display in Home Assistant UI
```

**Key Functions**:

- `async_setup()` - Platform initialization (register services, set up coordinator)
- `async_setup_entry()` - Per-config-entry setup (create entities, start polling)
- `async_unload_entry()` - Clean up integration (stop polling, remove entities)

### 2. Data Coordination Layer

**Core Class**: `TeslaDataUpdateCoordinator`

Responsibilities:

- Manage API client lifecycle and authentication tokens
- Coordinate polling of all registered vehicles and energy sites
- Handle vehicle wake-up/sleep logic to minimize battery drain
- Cache vehicle/site state data
- Distribute updates to all listening entities
- Implement exponential backoff on API failures
- Support optional TeslaMate MQTT sync as alternative to polling

```mermaid
graph LR
    A["Polling Timer<br/>660s default"] --> B["TeslaDataUpdateCoordinator"]
    B --> C["Fetch Vehicle State"]
    B --> D["Fetch Energy Site State"]
    B --> E["Update Token if Needed"]

    C --> F["Cache State"]
    D --> F
    F --> G["Notify Listeners<br/>All Entities"]

    G --> H["Entity Updates<br/>State & Attributes"]
```

**Key Methods**:

- `_async_update_data()` - Fetch latest state from Tesla API
- `async_update_listeners_debounced()` - Notify entities of state changes
- `_async_update_vehicles()` - Fetch and cache all vehicle states
- `async_remove_config_entry_device()` - Handle device removal

### 3. Entity Layer

**Base Classes**: `TeslaBaseEntity`, `TeslaCarEntity`, `TeslaEnergyEntity`

The entity layer implements Home Assistant entity framework patterns for different domains:

```mermaid
graph TB
    TBE["TeslaBaseEntity<br/>Common State & Properties"]

    TCE["TeslaCarEntity<br/>Vehicle Data Access"]
    TEE["TeslaEnergyEntity<br/>Site Data Access"]

    TBE --> TCE
    TBE --> TEE

    TCE --> S1["Sensors"]
    TCE --> S2["Switches"]
    TCE --> S3["Climate"]
    TCE --> S4["Covers"]
    TCE --> S5["Locks"]
    TCE --> S6["...Other Car Entities"]

    TEE --> E1["Sensors"]
    TEE --> E2["Switches"]
    TEE --> E3["Selects"]
```

**Entity Lifecycle**:

1. Created during `async_setup_entry()`
2. Registered with Home Assistant entity registry
3. Receive updates from `TeslaDataUpdateCoordinator`
4. Update their state in Home Assistant state machine
5. Removed during `async_unload_entry()`

**Platform Modules** (one per entity domain):

- `sensor.py` - Numeric and text state values
- `binary_sensor.py` - On/off state indicators
- `switch.py` - Toggle controls
- `climate.py` - HVAC temperature and modes
- `cover.py` - Openable/closable elements
- `button.py` - One-time action triggers
- `lock.py` - Lock/unlock controls
- `select.py` - Option selectors
- `number.py` - Numeric setters
- `device_tracker.py` - Location tracking
- `update.py` - Software version tracking
- `text.py` - Text configuration

Each platform implements `async_setup_entry()` to create and register its entities.

### 4. Configuration Layer

**File**: `config_flow.py` - Implements Home Assistant config flow UI

```mermaid
graph TD
    A["Start Config Flow"] --> B["User provides Tesla token"]
    B --> C["Validate with Tesla API"]
    C --> D{Valid?}
    D -->|No| E["Show Error"]
    E --> B
    D -->|Yes| F["Create Config Entry"]
    F --> G["Request Options<br/>Polling Interval, etc."]
    G --> H["Save Configuration"]
    H --> I["Setup Integration"]
```

**Key Components**:

- `TeslaConfigFlow` - Main flow handler
- `OptionsFlowHandler` - Options configuration
- Async validation of credentials
- Token refresh and persistence
- Support for multiple accounts

### 5. Support Integrations

#### TeslaMate MQTT Integration (`teslamate.py`)

Optional alternative to polling - syncs data from TeslaMate via MQTT:

```mermaid
graph LR
    TM["TeslaMate Instance<br/>Real-time tracking"]
    MQTT["MQTT Broker"]
    TeslaMate["TeslaMate Module<br/>MQTT listener"]
    TDC["TeslaDataUpdateCoordinator"]

    TM --> MQTT
    MQTT --> TeslaMate
    TeslaMate --> TDC
```

**Benefits**:

- Real-time updates without frequent polling
- Reduced battery drain
- Syncs location, charging state, climate state
- Works alongside or instead of cloud polling

#### Services (`services.py`)

Custom services for Home Assistant automations:

- `set_update_interval` - Change polling frequency at runtime
- `async_call_tesla_service` - Generic Tesla API command wrapper

## Data Flow Patterns

### Polling Cycle

```
1. Timer fires (polling_interval seconds)
2. TeslaDataUpdateCoordinator._async_update_data() called
3. Fetch all vehicles and energy sites from Tesla API
4. Cache new state in coordinator
5. Notify all subscribed entities
6. Entities update their Home Assistant state
7. Wait for next polling interval
```

**Sleep Optimization**:

- Coordinator tracks vehicle sleep state
- Skips polling for sleeping vehicles to save battery
- Respects user preference: wake on start or let sleep
- Configurable polling policy

### Entity Update Cycle

```mermaid
sequenceDiagram
    participant Coordinator
    participant Entity
    participant HA as Home Assistant

    Coordinator->>Coordinator: Fetch new data
    Coordinator->>Entity: _handle_coordinator_update()
    Entity->>Entity: Read new state from coordinator
    Entity->>HA: async_write_ha_state()
    HA->>HA: Update entity state in state machine
```

### Command Execution

```
1. User triggers action in Home Assistant UI
2. Entity method called (e.g., async_lock(), async_turn_on())
3. Entity calls Tesla API via coordinator.api
4. Tesla processes command and wakes vehicle if needed
5. Coordinator polls for confirmation
6. Entity state updated in Home Assistant
```

## Key Design Patterns

### 1. Data Coordinator Pattern

- Centralized data fetching and caching
- Single API client manages all connections
- Automatic retry and backoff
- Listeners notified of updates
- Reduces API calls and improves responsiveness

### 2. Entity Framework Integration

- All entities inherit from Home Assistant entity classes
- Async/await throughout for non-blocking operations
- State machine integration for persistence
- Unique IDs for device tracking
- Device grouping by vehicle/site

### 3. Async/Await Pattern

- Non-blocking I/O for API calls
- Concurrent polling of multiple vehicles
- Timeout handling with `async-timeout`
- Exception handling and logging

### 4. Configuration Entry System

- Credentials stored securely in Home Assistant config
- Per-entry setup and teardown
- Options flow for user configuration
- Device/entity registry updates

## Error Handling & Resilience

### API Error Handling

```mermaid
graph TD
    A["API Call"] --> B{Success?}
    B -->|Yes| C["Return Data"]
    B -->|No| D["Check Error Type"]
    D -->|Auth Error| E["Refresh Token"]
    D -->|Rate Limit| F["Backoff"]
    D -->|Other| G["Retry with Backoff"]
    E --> H["Retry Request"]
    F --> H
    G --> H
    H --> I{Max Retries?}
    I -->|No| A
    I -->|Yes| J["Log Error, Continue"]
```

**Patterns**:

- Exponential backoff on transient failures
- Token refresh on auth errors
- Graceful degradation if API unavailable
- Detailed logging for debugging

### Vehicle Sleep Logic

- Coordinator monitors vehicle sleep state
- Doesn't actively wake vehicles during polling
- Respects user configuration for wake behavior
- Vehicles wake naturally on commands or user action

## Home Assistant Integration Points

### Entity Framework

- Inherits from `RestoreEntity` for state persistence
- Uses `CoordinatorEntity` for automatic update handling
- Registers with entity and device registries
- Follows unique ID conventions

### State Machine

- Entity state stored in Home Assistant state machine
- Attributes for additional data (e.g., vehicle odometer)
- Binary entities for on/off indicators
- Numeric entities for sensors and controls

### Config Entry System

- One config entry per Tesla account
- Supports multiple accounts (multiple entries)
- Options flow for configuration changes
- Device and entity discovery

### Services

- Custom services for Tesla-specific commands
- Available for automations and scripts
- Async/await for non-blocking execution

### Device & Entity Registry

- Vehicles and sites as devices
- Entities grouped by device
- Supports device removal/grouping
- Unique identifiers for stability

## Technology Stack Integration

### Home Assistant

- `homeassistant` package for entity/device/config entry APIs
- Async patterns and event bus
- Logging and notification systems

### teslajsonpy Library

- OAuth 2.0 authentication
- Tesla API endpoint abstractions
- Vehicle and site data structures
- Command execution (lock, climate, etc.)

### asyncio

- Concurrent operations (multiple vehicles)
- Non-blocking I/O for HTTP requests
- Event-driven architecture

### Python 3.13+

- Type hints throughout codebase
- Async/await syntax
- Modern Python features

## Deployment Model

The integration runs within Home Assistant process:

- Single coordinator instance per config entry
- Entities created and managed by Home Assistant
- Polling runs as background task
- No external services or sidecars required
- Optional external: Tesla HTTP Proxy for Fleet API compatibility

---

**Key Takeaway**: The architecture prioritizes responsive real-time updates with minimal battery drain through intelligent polling, while maintaining clean separation between configuration, coordination, and entity layers per Home Assistant conventions.
