# What's New in v1.7.0

**Release Date:** January 2026  
**Type:** Major Feature Release  
**Breaking Changes:** None ✅

---

## 🎯 Top Features

### 1. Event-Based Button Detection ⚡

**Problem solved:** Pressing the same button twice didn't trigger automations.

**Now:** Every button press fires an event, even repeated presses!

```yaml
automation:
  trigger:
    - platform: event
      event_type: haptique_rs90_key_pressed
      event_data:
        button: 13
```

**Benefits:**
- ✅ Works with repeated button presses
- ✅ Dual functionality: RS90 macro + HA automation simultaneously
- ✅ Full event data: remote_id, device_id, button, timestamp

---

### 2. Device Triggers (No YAML Needed!) 🎮

**Create automations visually** in the Home Assistant UI:

1. Add Automation → Add Trigger → **Device**
2. Select **RS90 Remote**
3. Choose **Button pressed** → Select button (1-24)
4. Add actions → Save

**That's it!** No YAML, no complexity.

**Benefits:**
- ✅ 24 buttons available in dropdown
- ✅ Native Home Assistant automation builder
- ✅ Perfect for beginners

---

### 3. Macro Status Synchronization 🔄

**Problem solved:** Macro switches didn't update when triggered from RS90 remote.

**Now:** Switches accurately show macro state from any trigger source!

**Technical:**
- New MQTT topic: `macro/{name}/status` (published by RS90)
- Clean command/state separation
- Requires upcoming RS90 firmware update

**⚠️ Note:** Contact Haptique support for firmware availability.

---

### 4. Smart Battery Refresh 🔋

**Multiple improvements:**

**Automatic refresh on reconnection:**
- RS90 wakes from sleep → Battery level requested immediately
- Up to 6x more frequent updates when off charging dock

**Throttle protection:**
- Minimum 5 minutes between refreshes
- Prevents spam during unstable connections

**Reduced interval:**
- Periodic refresh: Every 30 minutes (was 60 minutes)

**Refresh frequency:**
- On dock (always online): Every 30 min
- Off dock (sleep/wake ~10 min): Every ~10 min on wake
- Unstable (<5 min reconnect): Max 1 per 5 min (throttled)

---

### 5. MQTT RemoteID Exposed 📍

**Easy access for debugging:**

```yaml
sensor.rs90_info_summary:
  rs90_id: "9b974..."              # HA Device ID
  rs90_remote_id: "3d5d95aa3a7f7b20"  # MQTT RemoteID ✨
```

Find your MQTT RemoteID instantly for manual MQTT operations.

---

## 🎉 Game-Changer: Dual Functionality

**A single RS90 button press now does TWO things:**

1. ✅ **Executes RS90 macro** (IR/RF control)
2. ✅ **Triggers Home Assistant automation** (smart home control)

**Example:** Press Button 13
- 📺 Turns on TV via IR (RS90 macro)
- 💡 Dims lights (HA automation)
- 🔊 Sets Sonos mode (HA automation)
- 🌡️ Adjusts thermostat (HA automation)

**All from ONE button press!**

---

## 🔧 Other Improvements

- ✅ Battery refresh added to `refresh_lists` service
- ✅ Enhanced logging for battery updates
- ✅ Improved coordinator with device_id tracking
- ✅ Better error messages

---

## ⚠️ Breaking Changes

**None!** This release is fully backward compatible with v1.5.1.

All existing automations, scripts, and configurations continue to work.

---

## 📋 Requirements

- **Home Assistant:** 2024.1.0 or newer
- **MQTT:** Configured and working
- **RS90 Firmware:** Latest version recommended
  - Macro status sync requires upcoming firmware update
  - All other features work with current firmware

---

## 🚀 Upgrade Steps

### If using HACS:

1. Open **HACS** → **Integrations**
2. Find **Haptique RS90**
3. Click **Update**
4. Restart Home Assistant

### If using manual installation:

1. Download [v1.7.0](https://github.com/daangel27/haptique_rs90/releases/tag/v1.7.0)
2. Extract to `/config/custom_components/haptique_rs90/`
3. Restart Home Assistant

**That's it!** No configuration changes needed.

---

## 💡 Getting Started with New Features

### Try Device Triggers (Easy)

1. **Settings** → **Automations** → **Add Automation**
2. **Add Trigger** → **Device** → Select RS90
3. **Button pressed** → Choose button number
4. Add action → Save
5. Press button on RS90 → Automation triggers! 🎉

### Try Events (Advanced)

```yaml
automation:
  - alias: "Multi-action button"
    trigger:
      - platform: event
        event_type: haptique_rs90_key_pressed
        event_data:
          button: 13
    action:
      - service: light.toggle
        target:
          entity_id: light.living_room
      - service: notify.mobile_app
        data:
          message: "Button 13 pressed!"
```

### Monitor Battery Better

Battery now updates:
- ✅ Every 30 minutes (automatic)
- ✅ On RS90 wake from sleep (automatic)
- ✅ Via service call (manual)

No action needed - just enjoy more frequent updates!

---

## 📚 Documentation

- **[README.md](README.md)** - Complete integration guide
- **[CHANGELOG.md](CHANGELOG.md)** - Detailed technical changes
- **[GitHub Releases](https://github.com/daangel27/haptique_rs90/releases)** - Download and release notes

---

## 🙏 Credits

Special thanks to:
- **Haptique Support** for implementing the `/status` topic and excellent collaboration
- **@Benz63Amg** for reporting issue #35 and validating the solution
- **Home Assistant Community** for feedback and testing

---

## 🆘 Need Help?

- 📖 [Full Documentation](README.md)
- 🐛 [Report Issues](https://github.com/daangel27/haptique_rs90/issues)
- 💬 [Discussions](https://github.com/daangel27/haptique_rs90/discussions)

---

**Enjoy v1.7.0!** 🎉
