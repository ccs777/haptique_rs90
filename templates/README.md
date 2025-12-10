# Device Buttons Card Template

Generate a beautiful remote control dashboard card with all available commands for any device controlled by your Haptique RS90.

![Device Buttons Card Example](../documentation/screenshots/device_buttons_card.png)
*Example: Full remote control card for Canal Plus*

---

## 🎯 What This Template Does

This template automatically generates a **grid card** containing **one button for each command** available on your device. When you press a button:

1. 🖱️ **Button pressed** in Home Assistant dashboard
2. 📡 **Service called**: `haptique_rs90.trigger_device_command`
3. 📤 **MQTT message sent** to your Haptique RS90 remote
4. 📻 **IR command transmitted** from RS90 to your actual device

**Result**: Your TV, receiver, or any IR device responds instantly!

---

## 📋 Prerequisites

Before using this template, you need:

1. ✅ **Haptique RS90 integration** installed and configured
2. ✅ **Device commands sensor** available (automatically created by the integration)
3. ✅ **card-mod** frontend plugin installed (for the 3D button styling)

### Installing card-mod (Optional but Recommended)

The template uses **card-mod** for beautiful 3D button styling. Without it, buttons will still work but look basic.

Install via HACS:
1. Open HACS → Frontend
2. Search for "card-mod"
3. Install and restart Home Assistant

**Note**: The template works without card-mod, but buttons won't have the 3D effect.

---

## 🔍 Finding Your Required Information

You need **3 pieces of information** to use this template:

### 1. Device Commands Sensor

**Where to find it**:
- Go to **Settings** → **Devices & Services**
- Click on **Haptique RS90**
- Click on your RS90 remote
- Look in the **Diagnostic** section
- Find sensors named: `Commands - {Device Name}`

**Example**: `sensor.commands_canal_g9_4k`

**Format**: `sensor.commands_{device_name}` (spaces replaced by underscores, lowercase)

### 2. RS90 Device ID (Home Assistant)

**Where to find it**:
- Same device page as above
- Look at the browser URL: `http://homeassistant.local:8123/config/devices/device/6e99751e77b5a07de72d549143e2875a`
- Copy the long ID at the end: `6e99751e77b5a07de72d549143e2875a`

**Alternative method**: Use the UI selector in Services (see [GUIDE_DEVICE_ID.md](../documentation/GUIDE_DEVICE_ID.md))

### 3. Device Name (Exact)

**Where to find it**:
- Go to the device commands sensor (from step 1)
- Click on it to see details
- Look at the **Attributes** section
- Find **Device name**: `Canal - G9 4K`

**Important**: Use the **exact name** including spaces, capitals, and special characters!

---

## 🚀 Step-by-Step Guide

### Step 1: Copy the Template

Copy the template code from [`templates/device_buttons_card.yaml`](device_buttons_card.yaml)

### Step 2: Replace the Values

You need to replace **3 values** in the template:

```yaml
{% for cmd in state_attr('sensor.commands_your_device_name', 'commands') %}
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                              1️⃣ Replace with YOUR sensor name
```

```yaml
device_id: "YOUR_RS90_DEVICE_ID_HERE"
            ^^^^^^^^^^^^^^^^^^^^^^^^^
            2️⃣ Replace with YOUR device ID
```

```yaml
device_name: "Your Device Name"
              ^^^^^^^^^^^^^^^^^
              3️⃣ Replace with YOUR exact device name
```

**Example with real values**:

```yaml
# Before (template with placeholders)
{% for cmd in state_attr('sensor.commands_your_device_name', 'commands') %}
  device_id: "YOUR_RS90_DEVICE_ID_HERE"
  device_name: "Your Device Name"

# After (with your actual values)
{% for cmd in state_attr('sensor.commands_canal_g9_4k', 'commands') %}
  device_id: "6e99751e77b5a07de72d549143e2875a"
  device_name: "Canal - G9 4K"
```

### Step 3: Generate the Card Code

1. Go to **Developer Tools** → **Template** (URL: `/developer-tools/template`)
2. **Paste your modified template** in the left editor
3. Wait for the result to appear in the **Result** panel on the right
4. **Copy the entire result code** (it will be much longer than the template)

![Template Editor](../documentation/screenshots/template_editor.png)
*The template editor generates the final card code*

### Step 4: Add to Your Dashboard

1. Go to any dashboard
2. Click **Edit Dashboard** (top right)
3. Click **Add Card**
4. Scroll down and select **Manual** (at the bottom)
5. **Paste the code** you copied from the Template Result
6. Click **Save**

Done! 🎉 You now have a beautiful remote control card!

---

## 🎨 Customization

### Change Grid Layout

Modify the `columns` value to change button layout:

```yaml
columns: 4  # 4 columns (default, good for mobile)
columns: 5  # 5 columns (more compact)
columns: 3  # 3 columns (larger buttons)
```

### Change Colors

Modify the CSS variables:

```yaml
--mdc-theme-primary: #1e3a8a;      # Main button color (blue)
--mdc-theme-secondary: #0f172a;    # Button gradient end (dark blue)
```

**Popular color schemes**:

**Red theme** (for power/media devices):
```yaml
--mdc-theme-primary: #dc2626;
--mdc-theme-secondary: #7f1d1d;
```

**Green theme** (for eco/home devices):
```yaml
--mdc-theme-primary: #16a34a;
--mdc-theme-secondary: #14532d;
```

**Purple theme** (for entertainment):
```yaml
--mdc-theme-primary: #9333ea;
--mdc-theme-secondary: #581c87;
```

### Remove 3D Effect

If you don't have card-mod or want flat buttons, simply delete the entire `card_mod:` section from the template.

---

## 🔧 Troubleshooting

### Buttons Don't Appear

**Problem**: Template generates empty result
**Solution**: 
- Check sensor name is correct (must start with `sensor.commands_`)
- Verify the sensor exists in **Developer Tools** → **States**

### Buttons Don't Work

**Problem**: Clicking buttons does nothing
**Solution**:
- Verify `device_id` is correct (check URL in device page)
- Verify `device_name` is **exact** (case-sensitive, include spaces/dashes)
- Check your RS90 is online (Connection sensor = ON)

### Buttons Look Basic (No 3D Effect)

**Problem**: Buttons work but look flat
**Solution**: Install **card-mod** via HACS → Frontend

### Wrong Commands Appear

**Problem**: Buttons show commands for wrong device
**Solution**: You used the wrong sensor name. Each device has its own `sensor.commands_{device}`.

---

## 📸 Screenshots

### Generated Card Examples

<table>
<tr>
<td width="50%">
<img src="../documentation/screenshots/device_buttons_card.png" alt="Canal Plus Remote" />
<p align="center"><em>Canal Plus - Full remote with 31 buttons</em></p>
</td>
<td width="50%">
<p><strong>Features:</strong></p>
<ul>
<li>✅ 4-column grid layout</li>
<li>✅ 3D button effect</li>
<li>✅ Press animation</li>
<li>✅ Auto-generated from sensor</li>
<li>✅ Works with any device</li>
</ul>
</td>
</tr>
</table>

---

## 💡 Tips & Best Practices

### Organize Multiple Devices

Create **one card per device** and organize them in **tabs** or **vertical stacks**:

```yaml
type: vertical-stack
title: Living Room Entertainment
cards:
  - type: markdown
    content: "## TV Remote"
  - # Your TV buttons card here
  
  - type: markdown
    content: "## Sound System"
  - # Your sound system buttons card here
```

### Add Card Title

Wrap your card in a vertical stack with a title:

```yaml
type: vertical-stack
cards:
  - type: markdown
    content: "# 📺 Canal Plus"
    card_mod:
      style: |
        ha-card {
          background: none;
          box-shadow: none;
          text-align: center;
        }
  - # Your buttons card here
```

### Use Conditional Cards

Show different remotes based on what's playing:

```yaml
type: conditional
conditions:
  - entity: media_player.tv
    state: "on"
card:
  # Your TV remote card here
```

---

## 🎬 Example: Complete Setup

Here's a complete example for a "Canal - G9 4K" device:

**1. My information**:
- Sensor: `sensor.commands_canal_g9_4k`
- Device ID: `6e99751e77b5a07de72d549143e2875a`
- Device name: `Canal - G9 4K`

**2. Template with my values** (paste in Template Editor):

```yaml
type: grid
columns: 4
square: false
cards:
  {% for cmd in state_attr('sensor.commands_canal_g9_4k', 'commands') %}
  - type: button
    name: "{{ cmd.replace('_', ' ') }}"
    tap_action:
      action: call-service
      service: haptique_rs90.trigger_device_command
      data:
        device_id: "6e99751e77b5a07de72d549143e2875a"
        device_name: "Canal - G9 4K"
        command_name: "{{ cmd }}"
    # ... rest of styling ...
  {% endfor %}
```

**3. Result**: Copy generated code 

**4. Add to dashboard**: Paste in Manual card

**5. Done!** 🎉

---

## 📦 Files

- **Template**: [`device_buttons_card.yaml`](device_buttons_card.yaml)
- **Example**: [`example_canal_plus.yaml`](example_canal_plus.yaml) (with real values)
- **Screenshot**: [device_buttons_card.png](../documentation/screenshots/device_buttons_card.png)

---

## 🆘 Need Help?

- 📖 [Main Documentation](../README.md)
- 🔍 [How to Find Device ID](../documentation/GUIDE_DEVICE_ID.md)
- 🐛 [Report Issues](https://github.com/daangel27/haptique_rs90/issues)
- 💬 [Discussions](https://github.com/daangel27/haptique_rs90/discussions)

---

**Template Version**: 1.0  
**Compatible with**: Haptique RS90 Integration v1.2.5+
**Last Updated**: December 2025
