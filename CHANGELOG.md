# Changelog

All notable changes to this project will be documented in this file.

## [1.2.8] - 2025-12-12

### ✨ Major Improvements

This release brings automatic device command discovery and battery monitoring improvements.

#### 🎯 New Features
- **Automatic Device Commands Discovery**: New devices added in Haptique Config now automatically appear with their commands
  - No manual action required after adding a device
  - Commands appear within 2-3 seconds
  - Works seamlessly like macro detection
- **Automatic Battery Refresh**: Battery level now updates automatically every hour
  - No more stale battery readings
  - Configurable refresh interval (default: 1 hour)
  - Ensures current battery status

#### 🔧 Improvements
- **Enhanced refresh_lists Service**: Improved to actively re-scan and subscribe to new devices/macros
  - Can be used as a fallback if automatic detection doesn't trigger
  - Now actually processes and subscribes, not just logs
- **Better MQTT Compliance**: Fixed final QoS issue with macro trigger subscriptions
  - Changed from QoS 1 to QoS 0 for monitoring (as per Haptique best practices)
  - 100% compliant with official MQTT specification

#### 🐛 Bug Fixes
- **Fixed Integration Reload Error**: Resolved "Cannot unsubscribe topic twice" error
  - Clean shutdown and restart now works perfectly
  - Proper subscription lifecycle management
  - No more error logs on reload

#### 📚 Documentation
- Added comprehensive bug report for Haptique support
  - Documented discrepancies in official MQTT documentation
  - Provided working examples and code snippets
  - Ready to submit to improve official documentation

---

## [1.2.7] - 2025-12-11 (Internal Release)

### 🔧 Technical Release

This version was an internal release focused on MQTT protocol compliance verification.

#### ✨ Changes
- Comprehensive MQTT compliance analysis
- QoS level corrections
- Empty payload handling improvements
- Documentation of RS90 actual behavior vs official docs

**Note**: This version was superseded by v1.2.8 which includes the correct fixes.

---

## [1.2.6] - 2025-12-11

### 🔧 Maintenance Release

This is a maintenance release with documentation updates and minor improvements.

#### 📚 Documentation
- Updated all documentation dates from 2024 to 2025
- Refreshed version badges and references
- Updated copyright year to 2025
- Minor formatting improvements

#### ✨ Improvements
- Enhanced README clarity
- Updated examples with current year
- Improved consistency across documentation

---

## [1.2.5] - 2024-12-10

### 🎉 Major Changes from v1.2.0

#### ✨ New Features
- **Device Command Sensors**: Added diagnostic sensors showing available commands for each device
  - Sensors created as `sensor.commands_{device_name}`
  - Alphabetically sorted for easy browsing
  - Categorized as diagnostic entities
- **Enhanced MQTT Logging**: Added comprehensive DEBUG logs for all MQTT operations
  - Subscribe/Unsubscribe operations with topics
  - All received messages with payloads
  - All published messages with QoS and retain flags
  - Useful for troubleshooting and monitoring

#### 🔧 Technical Improvements
- **100% Event-Driven**: Removed all periodic polling
  - No more `scan_interval` configuration
  - Updates only via MQTT messages
  - Reduced network traffic and improved responsiveness
- **QoS Optimization**: Aligned with Haptique MQTT best practices
  - QoS 0 for monitoring (status, battery, keys, lists)
  - QoS 1 for control commands (macro/device triggers)
- **Macro Trigger Protocol**: Fixed MQTT retained message handling
  - Changed from `retain=True` to `retain=False` for macro triggers
  - Proper unsubscribe when macros are deleted
  - Automatic cleanup of retained messages on deletion
- **Dynamic Entity Management**: Improved add/remove of entities
  - Proper cleanup when macros/devices are deleted
  - Fixed race conditions in subscription management
  - Entities update in real-time

#### 🗑️ Removed Features
- **Removed Services**:
  - `haptique_rs90.refresh_data` (no longer needed with event-driven updates)
  - `haptique_rs90.get_diagnostics` (use DEBUG logs instead)
- **Removed Entities**:
  - Refresh Data button
  - Scan Interval slider

#### 🎨 UI/UX Improvements
- **Macro Switches**:
  - Blue (ON) / Gray (OFF) coloring via device_class
  - Better visual feedback
- **Connection Sensor**:
  - Dynamic icons: `mdi:connection` (connected) / `mdi:close-network-outline` (disconnected)
- **Running Macro Sensor**:
  - Dynamic icons: `mdi:play-circle` (active) / `mdi:circle-outline` (idle)

#### 🌐 Internationalization
- **Multi-language Support**:
  - English (default)
  - French
- **Service Descriptions**: Improved clarity
  - Better `device_id` explanation (Home Assistant ID vs MQTT ID)
  - Clear instructions: "find it in Settings > Devices & Services"
  - Examples with actual IDs
- **Translated Strings**: Complete translations for:
  - Configuration flow
  - Service names and descriptions
  - Field labels and descriptions

#### 🐛 Bug Fixes
- **MQTT Subscription Management**:
  - Fixed race condition causing macros not to unsubscribe properly
  - Proper tracking of subscription states
  - Synchronized `_subscribed_macros` and `_macro_subscriptions` dictionaries
  - Proper unsubscribe when macros are deleted
- **State Persistence**:
  - Removed `.storage` file-based persistence (was causing random triggers)
  - Now relies solely on MQTT retained messages from RS90 (single source of truth)

#### 📚 Documentation
- **Improved README**:
  - English as default language
  - Clear auto-discovery explanation
  - Prerequisites section added
  - Better screenshots examples
  - Acknowledgment to Cantata Communication Solutions
- **Service Documentation**:
  - Clear distinction between MQTT ID and Home Assistant device_id
  - Step-by-step guide to find device_id
  - Better examples

#### 🔒 Protocol Compliance
- **100% Haptique MQTT Compliant**:
  - Verified against official documentation
  - Correct QoS levels for all operations
  - Proper retained message handling
  - Subscribe-once pattern implemented

---

## [1.2.0] - 2024-12-XX

### Initial Features
- MQTT integration with Haptique RS90
- Basic sensors (battery, last key, running macro, device list)
- Binary sensor for connection status
- Macro switches with ON/OFF states
- Services for triggering macros and device commands
- Configurable scan interval (60s-3600s)
- Manual refresh button
- Diagnostic service

---

## Migration Guide: 1.2.6 → 1.2.8

### What's New
- ✅ Automatic device command discovery
- ✅ Automatic battery refresh (hourly)
- ✅ Improved `refresh_lists` service (now actually works)
- ✅ Fixed reload error
- ✅ 100% MQTT compliant

### Breaking Changes
**None!** This is a seamless upgrade.

### What You Need to Do
1. Update the integration (via HACS or manually)
2. Restart Home Assistant
3. That's it! Everything works automatically now.

### Benefits of Upgrading
- 🚀 New devices appear automatically with their commands
- 🔋 Battery level stays current (auto-refresh every hour)
- 🐛 No more reload errors
- ✅ Fully compliant with Haptique MQTT specification
- 📱 Better user experience (zero manual intervention)

---

## Migration Guide: 1.2.0 → 1.2.5+

### Breaking Changes
- ⚠️ **Removed entities**: `button.{name}_refresh_data` and `number.{name}_scan_interval`
- ⚠️ **Removed services**: `haptique_rs90.refresh_data` and `haptique_rs90.get_diagnostics`

### What You Need to Do
1. **Remove automations/scripts** that use removed services
2. **Update dashboards** to remove refresh button and scan interval entities
3. **Enable DEBUG logs** if you were using `get_diagnostics` service:
   ```yaml
   logger:
     logs:
       custom_components.haptique_rs90: debug
   ```

### What Stays the Same
- ✅ All macro switches work identically
- ✅ All sensors continue to function
- ✅ Services `trigger_macro` and `trigger_device_command` unchanged
- ✅ No configuration changes needed

### Benefits of Upgrading
- 🚀 Faster response times (event-driven vs polling)
- 📉 Reduced network traffic
- 🐛 No more random macro triggers
- 🎨 Better visual feedback (colors, icons)
- 🌐 Multi-language support
- 📋 Device command sensors for easy command discovery
