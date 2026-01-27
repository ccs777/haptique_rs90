# Changelog - Haptique RS90 Home Assistant Integration

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.7.0] - 2025-01-XX

### ✨ New Features

#### Event-Based Key Press Detection
- **Fire events on every button press**, including repeated presses of the same button
- New event: `haptique_rs90_key_pressed` with data: `remote_id`, `device_id`, `button`, `timestamp`
- Enables **dual functionality**: RS90 macro execution + Home Assistant automation from single button press
- Solves issue where pressing the same button twice didn't trigger automations

**Example usage:**
```yaml
automation:
  trigger:
    - platform: event
      event_type: haptique_rs90_key_pressed
      event_data:
        button: 13
```

#### Device Triggers for Native UI Support
- **24 button triggers** (1-24) available in Home Assistant automation UI
- No manual YAML needed - fully visual automation builder compatible
- Select RS90 device and button directly from dropdown menus

**Example (UI-generated):**
```yaml
trigger:
  - platform: device
    device_id: [your_rs90]  # From sensor.rs90_info_summary → rs90_id
    domain: haptique_rs90
    type: button_pressed
    button: 13
```

#### Macro Status Synchronization
- **New MQTT topic**: Subscribe to `macro/{MacroName}/status` for state feedback
  - ⚠️ **Requires updated RS90 firmware** (upcoming release from Haptique - check with Haptique support for availability)
- **Proper state tracking** when macros are triggered from RS90 remote
- Switch entities now accurately reflect macro state regardless of trigger source
- Clean MQTT architecture: Commands (`/trigger`) separated from state (`/status`)

**Technical details:**
- Command topic: `macro/{MacroName}/trigger` (retain=False, ephemeral)
- Status topic: `macro/{MacroName}/status` (retain=True by RS90, authoritative state)
- No synchronization loops or duplicate commands

#### MQTT RemoteID Exposure
- Added `rs90_remote_id` attribute to `sensor.rs90_info_summary`
- Makes MQTT RemoteID easily discoverable for debugging and manual MQTT operations

**Example attributes:**
```yaml
sensor.rs90_info_summary:
  rs90_id: "9b974dab9a7649e13baeb921d4c9bb85"  # HA Device ID
  rs90_remote_id: "3d5d95aa3a7f7b20"  # MQTT RemoteID (new!)
  rs90_device_name: "RS90"
  devices: {...}
  macros: {...}
```

### 🔧 Improvements

#### Battery Refresh Optimizations
- **Automatic refresh on reconnection**: Battery level requested immediately when RS90 wakes from sleep
- **Optimized for sleep/wake cycles**: Up to 6x more frequent updates when RS90 is off charging dock
- **Throttle protection**: Minimum 5 minutes between refreshes to prevent spam during unstable connections
- **Reduced timer interval**: Periodic refresh every 30 minutes (was 60 minutes)

**Refresh frequency:**
- On charging dock (always online): Every 30 minutes
- Off dock (sleep/wake ~10 min): Every ~10 minutes on wake
- Unstable connection (<5 min disconnect/reconnect): Throttled to max 1 refresh per 5 minutes

#### Battery Refresh in `refresh_lists` Service
- Service `refresh_lists` now also requests battery level update
- Useful for manual refresh without waiting for automatic intervals

### 🐛 Bug Fixes

- Fixed macro state not updating when triggered from RS90 remote
- Fixed potential MQTT publish loops during macro state synchronization
- Fixed battery level not updating during RS90 sleep/wake cycles

### 📝 Documentation

- Added comprehensive examples for event-based automations
- Documented device trigger usage in automation UI
- Explained macro status synchronization architecture
- Added battery refresh behavior documentation

### ⚠️ Breaking Changes

**None** - This release is fully backward compatible with v1.5.1.

### 🙏 Credits

- **Macro status synchronization**: Special thanks to **Haptique Support** for implementing the `/status` topic and providing excellent collaboration!
- **Event detection issue**: Reported and validated by @Benz63Amg in issue #35

### 📋 Requirements

- **RS90 Firmware**: Macro status synchronization requires updated RS90 firmware with `/status` topic support
  - This feature will be available in an upcoming firmware release
  - Contact Haptique support for firmware availability and update instructions
  - All other features work with current firmware versions
- **Home Assistant**: 2024.1.0 or newer
- **MQTT**: Configured and working

---

## [1.5.1] - 2024-12-XX

### Previous stable release

See GitHub releases for details: https://github.com/daangel27/haptique_rs90/releases

---

## Links

- [GitHub Repository](https://github.com/daangel27/haptique_rs90)
- [Issue Tracker](https://github.com/daangel27/haptique_rs90/issues)
- [Documentation](https://github.com/daangel27/haptique_rs90/blob/main/README.md)
