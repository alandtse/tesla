# Contribution Guidelines

Contributing to this project should be as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features

## GitHub is used for everything

Github is used to host code, to track issues and feature requests, as well as accept pull requests.

Pull requests are the best way to propose changes to the codebase.

1. Fork the repo and create your branch from `main`.
2. If you've changed something, update the documentation.
3. Make sure your code lints (using black).
4. Test your contribution.
5. Issue that pull request!

---

## Development Setup

### Prerequisites

- Python 3.13+
- Poetry (for dependency management)
- Docker (optional, for development container)
- Git

### Local Development Installation

```bash
# Clone the repository
git clone https://github.com/alandtse/tesla.git
cd tesla

# Install dependencies with Poetry
poetry install

# Or with pip
pip install -e .[dev]
```

### Development Container (Recommended)

The project includes a Docker dev container with isolated Home Assistant instance:

1. Install "Remote - Containers" extension in VS Code
2. Reopen folder in container
3. Home Assistant instance available at `localhost:8123`
4. Integration pre-configured for testing

---

## Code Style & Quality

### Code Formatting with Black

This project uses [Black](https://github.com/ambv/black) for code formatting (88 character line length, Python 3.13 target).

```bash
# Format all files
black .

# Format specific directory
black custom_components/tesla_custom/

# Check formatting without changes
black --check .
```

### Type Checking with mypy

All code must have proper type hints and pass mypy validation.

```bash
# Type check entire project
mypy .

# Type check specific file
mypy custom_components/tesla_custom/sensor.py
```

### Linting with Prospector

Comprehensive code analysis to enforce style and quality standards.

```bash
# Run full analysis
prospector

# Check specific issues
bandit -r .           # Security scan
pydocstyle            # Docstring check
```

### Pre-commit Hooks

Hooks automatically run on commit to enforce standards:

```bash
# Setup hooks (one-time)
pre-commit install

# Run manually
pre-commit run --all-files

# Skip hooks (not recommended)
git commit --no-verify
```

**Hooks run**: black, mypy, prospector, bandit

---

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov

# Run single test file
pytest tests/test_sensor.py

# Run specific test
pytest tests/test_sensor.py::test_battery_value
```

### Writing Tests

Tests follow Home Assistant testing patterns:

**Test Structure**:

- One test file per entity type (test_sensor.py, test_switch.py, etc.)
- Mock data in `tests/mock_data/` (car.py, energysite.py)
- Utilities in `tests/common.py` for setup helpers

**Example Test**:

```python
@pytest.mark.asyncio
async def test_battery_value(hass):
    """Test battery sensor reads correct value"""
    # Setup
    coordinator = setup_mock_controller(hass)
    await hass.async_block_till_done()

    # Get entity
    battery_entity = hass.states.get("sensor.tesla_battery")

    # Assert
    assert battery_entity.state == "42"
```

### Test Utilities

- `setup_platform()` - Set up integration for testing
- `setup_mock_controller()` - Create mock coordinator with test data
- Fixtures for hass, config_entry, mock vehicles/sites

---

## Making Changes

### Adding a New Entity

1. **Choose entity type** - Sensor, Switch, Climate, Cover, etc.
2. **Find similar entity** - Use as template in `{platform}.py`
3. **Create entity class** - Inherit from base class + HA entity class
4. **Implement required properties** - native_value, state, etc.
5. **Register in async_setup_entry** - Add to entity creation list
6. **Write tests** - Add test in `tests/test_{platform}.py`
7. **Update documentation** - Document in README or docs/

### Fixing a Bug

1. **Reproduce the issue** - Provide steps to reproduce
2. **Write a failing test** - Test case that demonstrates the bug
3. **Fix the code** - Make minimal changes to fix the issue
4. **Verify test passes** - Confirm test now passes
5. **Check no regressions** - Run full test suite
6. **Update docs if needed** - Reflect behavior change

### Adding a Feature

1. **Discuss first** - Open issue to discuss approach
2. **Plan implementation** - Consider architecture impact
3. **Implement incrementally** - Small, focused changes
4. **Write comprehensive tests** - Cover new functionality
5. **Update documentation** - Document user-facing changes
6. **Get review** - Request feedback from maintainers

---

## Pull Request Process

### Before Submitting

- [ ] Code follows black formatting (run: `black .`)
- [ ] Type hints present and mypy passes (run: `mypy .`)
- [ ] Code passes linting (run: `prospector`)
- [ ] All tests pass (run: `pytest`)
- [ ] Documentation updated
- [ ] No unrelated changes included

### Submitting a Pull Request

1. Create a descriptive branch name from `main`
   - Good: `fix/charger-state-update`, `feature/seat-heaters`
   - Bad: `fix-bug`, `patch`, `my-changes`

2. Write a clear PR title (under 70 characters)
   - Good: "Fix battery level not updating when charging"
   - Bad: "update", "fix", "various improvements"

3. Include PR description with:
   - Summary of changes
   - Why this change is needed
   - What was tested
   - Any breaking changes

4. Link related issues
   - "Fixes #123" (auto-closes issue)
   - "Related to #456"

5. Be responsive to review feedback
   - Address comments constructively
   - Ask questions if unclear
   - Push fixes as new commits (don't force-push during review)

### Review & Merge

- Maintainers will review for:
  - Code quality and style
  - Test coverage
  - Documentation completeness
  - Home Assistant integration patterns
  - Security and performance

- Merge requires:
  - Approval from at least one maintainer
  - All checks passing (CI/CD)
  - No conflicts with main branch

---

## Bug Reports

### Opening an Issue

Use GitHub's [issue tracker](../../issues) to report bugs.

**Great Bug Reports Typically Have**:

- **Clear title** - Briefly describe the problem
- **Steps to reproduce** - Specific, detailed steps
- **Expected behavior** - What should happen
- **Actual behavior** - What actually happens
- **Environment info**:
  - Home Assistant version
  - Integration version
  - Python version
  - Vehicle model/year
  - Any error logs/stack traces

**Example**:

```
Title: Battery level sensor not updating when charging

Steps to reproduce:
1. Start charging vehicle via Tesla app
2. Wait 10 minutes (polling interval 660s)
3. Check battery level sensor in HA

Expected: Battery level increases, sensor state updates

Actual: Battery level stays at 42%, sensor unchanged

Environment:
- HA version: 2025.2.0
- Integration version: 3.26.3
- Vehicle: Model 3 2023
- Error log: [include any relevant logs]
```

---

## Feature Requests

### Opening a Feature Request

1. Search existing issues to avoid duplicates
2. Open an issue with:
   - Clear description of desired feature
   - Use case or problem it solves
   - Proposed implementation (if applicable)
   - Any relevant context or examples

**Example**:

```
Title: Add support for Powerwall backup reserve threshold

Description:
Currently I can see the backup reserve percentage, but can't set it
programmatically or in automations. Would be great to have a service
to adjust the reserve threshold.

Use case: Automation to increase backup reserve during high wildfire
season, reduce during winter.

Proposed: Add `tesla_custom.set_backup_reserve` service similar to
existing `set_update_interval`.
```

---

## Code Review Expectations

### What We Look For

- **Correctness**: Logic is sound, handles edge cases
- **Testing**: Changes have appropriate test coverage
- **Style**: Follows project conventions (black, type hints)
- **Documentation**: Changes documented for users/developers
- **Performance**: No unnecessary complexity or inefficiency
- **Security**: No unsafe operations, proper error handling
- **Integration**: Follows Home Assistant patterns

### Constructive Feedback

- Assume good intent
- Ask clarifying questions
- Suggest solutions, not just problems
- Acknowledge good work
- Focus on code, not person

---

## Any Contributions You Make Will Be Under the Apache License

In short, when you submit code changes, your submissions are understood to be under the same [Apache License](https://choosealicense.com/licenses/apache-2.0/) that covers the project. Feel free to contact the maintainers if that's a concern.

---

## License

By contributing, you agree that your contributions will be licensed under its [Apache License](LICENSE).

---

## Questions?

- Open an issue for questions about contributing
- Chat with the community on [Discord](https://discord.gg/Qa5fW2R)
- Check the [Wiki](https://github.com/alandtse/tesla/wiki) for additional resources

Thank you for contributing! 🎉
