import streamlit as st
from datetime import datetime
import pytz
import time

# Set page config
st.set_page_config(
    page_title="Digital Clock - Multiple Time Zones",
    page_icon="🕐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .clock-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin: 20px 0;
        text-align: center;
    }
    
    .clock-display {
        font-size: 48px;
        font-weight: bold;
        color: white;
        font-family: 'Courier New', monospace;
        letter-spacing: 2px;
        margin: 20px 0;
    }
    
    .timezone-label {
        font-size: 24px;
        color: #e0e0e0;
        margin-bottom: 10px;
        font-weight: 500;
    }
    
    .timezone-info {
        font-size: 14px;
        color: #b0b0b0;
        margin-top: 10px;
    }
    
    .timezone-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    .small-clock {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .small-clock-time {
        font-size: 36px;
        font-weight: bold;
        color: white;
        font-family: 'Courier New', monospace;
        margin: 10px 0;
    }
    
    .small-clock-tz {
        font-size: 16px;
        color: #e0e0e0;
        font-weight: 500;
    }
    
    .small-clock-date {
        font-size: 12px;
        color: #b0b0b0;
        margin-top: 5px;
    }
    
    h1 {
        color: #333;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .subtitle {
        color: #666;
        text-align: center;
        margin-bottom: 30px;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and subtitle
st.markdown("<h1>🕐 Digital Clock - Multiple Time Zones</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>View current time across different time zones around the world</p>", unsafe_allow_html=True)

# Sidebar for timezone selection
st.sidebar.header("⚙️ Settings")

# Common timezones
common_timezones = {
    "🌍 World":
    {
        "UTC/GMT": "UTC",
        "London": "Europe/London",
        "Paris": "Europe/Paris",
        "Dubai": "Asia/Dubai",
        "Tokyo": "Asia/Tokyo",
        "Sydney": "Australia/Sydney",
        "New York": "America/New_York",
        "Los Angeles": "America/Los_Angeles",
        "Mexico City": "America/Mexico_City",
        "São Paulo": "America/Sao_Paulo",
    },
    "🌏 Asia-Pacific": {
        "Hong Kong": "Asia/Hong_Kong",
        "Singapore": "Asia/Singapore",
        "Bangkok": "Asia/Bangkok",
        "Jakarta": "Asia/Jakarta",
        "Manila": "Asia/Manila",
        "Seoul": "Asia/Seoul",
        "Shanghai": "Asia/Shanghai",
        "Mumbai": "Asia/Kolkata",
        "Bangkok": "Asia/Bangkok",
        "New Zealand": "Pacific/Auckland",
    },
    "🌎 Americas": {
        "Toronto": "America/Toronto",
        "Vancouver": "America/Vancouver",
        "Denver": "America/Denver",
        "Chicago": "America/Chicago",
        "Anchorage": "America/Anchorage",
        "Honolulu": "Pacific/Honolulu",
        "Buenos Aires": "America/Argentina/Buenos_Aires",
        "Lima": "America/Lima",
        "Caracas": "America/Caracas",
    },
    "🌍 Europe & Africa": {
        "Athens": "Europe/Athens",
        "Moscow": "Europe/Moscow",
        "Istanbul": "Europe/Istanbul",
        "Cairo": "Africa/Cairo",
        "Johannesburg": "Africa/Johannesburg",
        "Lagos": "Africa/Lagos",
        "Nairobi": "Africa/Nairobi",
        "Berlin": "Europe/Berlin",
        "Rome": "Europe/Rome",
    }
}

# Allow user to add custom timezones
st.sidebar.subheader("Select Timezones to Display")

selected_timezones = {}
for region, zones in common_timezones.items():
    if st.sidebar.checkbox(region, value=True):
        selected_timezones.update(zones)

# Option to add custom timezone
st.sidebar.subheader("Add Custom Timezone")
custom_tz_input = st.sidebar.text_input(
    "Enter timezone (e.g., 'America/Toronto'):",
    help="Use IANA timezone format"
)

if custom_tz_input:
    try:
        pytz.timezone(custom_tz_input)
        selected_timezones[custom_tz_input] = custom_tz_input
    except pytz.exceptions.UnknownTimeZoneError:
        st.sidebar.error(f"Unknown timezone: {custom_tz_input}")

# Display options
display_format = st.sidebar.radio(
    "Time Format:",
    ["12-Hour (AM/PM)", "24-Hour"],
    index=0
)

show_date = st.sidebar.checkbox("Show Date", value=True)
show_offset = st.sidebar.checkbox("Show UTC Offset", value=True)
auto_refresh = st.sidebar.checkbox("Auto Refresh (updates every second)", value=True)

# Placeholder for clock updates
clock_placeholder = st.empty()

# Main display
if not selected_timezones:
    st.warning("👈 Select at least one timezone from the sidebar to display the clock")
else:
    # Create columns for main clock display
    if len(selected_timezones) == 1:
        # Single timezone - large display
        tz_name = list(selected_timezones.keys())[0]
        tz = pytz.timezone(selected_timezones[tz_name])
        
        while True:
            current_time = datetime.now(tz)
            
            # Format time
            if display_format == "12-Hour (AM/PM)":
                time_str = current_time.strftime("%I:%M:%S %p")
            else:
                time_str = current_time.strftime("%H:%M:%S")
            
            # Build display content
            with clock_placeholder.container():
                col1, col2, col3 = st.columns([1, 3, 1])
                with col2:
                    st.markdown(f"""
                        <div class="clock-container">
                            <div class="timezone-label">{tz_name}</div>
                            <div class="clock-display">{time_str}</div>
                    """, unsafe_allow_html=True)
                    
                    if show_date:
                        date_str = current_time.strftime("%A, %B %d, %Y")
                        st.markdown(f"<div class='timezone-info'>{date_str}</div>", unsafe_allow_html=True)
                    
                    if show_offset:
                        offset_str = current_time.strftime("%z")
                        offset_formatted = f"{offset_str[:3]}:{offset_str[3:]}"
                        st.markdown(f"<div class='timezone-info'>UTC {offset_formatted}</div>", unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
            
            if not auto_refresh:
                break
            
            time.sleep(1)
    else:
        # Multiple timezones - grid display
        while True:
            with clock_placeholder.container():
                st.subheader(f"📍 {len(selected_timezones)} Time Zones")
                
                # Create grid layout
                cols = st.columns(3)
                col_idx = 0
                
                for tz_name in sorted(selected_timezones.keys()):
                    tz = pytz.timezone(selected_timezones[tz_name])
                    current_time = datetime.now(tz)
                    
                    # Format time
                    if display_format == "12-Hour (AM/PM)":
                        time_str = current_time.strftime("%I:%M:%S %p")
                    else:
                        time_str = current_time.strftime("%H:%M:%S")
                    
                    with cols[col_idx % 3]:
                        st.markdown(f"""
                            <div class="small-clock">
                                <div class="small-clock-tz">{tz_name}</div>
                                <div class="small-clock-time">{time_str}</div>
                        """, unsafe_allow_html=True)
                        
                        if show_date:
                            date_str = current_time.strftime("%m/%d/%Y")
                            st.markdown(f"<div class='small-clock-date'>{date_str}</div>", unsafe_allow_html=True)
                        
                        if show_offset:
                            offset_str = current_time.strftime("%z")
                            offset_formatted = f"{offset_str[:3]}:{offset_str[3:]}"
                            st.markdown(f"<div class='small-clock-date'>UTC {offset_formatted}</div>", unsafe_allow_html=True)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    col_idx += 1
            
            if not auto_refresh:
                break
            
            time.sleep(1)

# Footer with helpful information
st.divider()
st.markdown("""
### ℹ️ How to Use
1. **Select Timezones**: Use the checkbox groups in the sidebar to choose which regions to display
2. **Add Custom Timezone**: Enter any valid IANA timezone (e.g., 'Asia/Bangkok', 'America/Toronto')
3. **Customize Display**: Choose 12-hour or 24-hour format, show/hide date and UTC offset
4. **Auto Refresh**: Toggle automatic updates (refreshes every second)

### 🌐 Common IANA Timezone Examples
- `America/New_York` - Eastern Time
- `America/Chicago` - Central Time
- `America/Denver` - Mountain Time
- `America/Los_Angeles` - Pacific Time
- `Europe/London` - UK Time
- `Europe/Paris` - Central European Time
- `Asia/Tokyo` - Japan Time
- `Asia/Shanghai` - China Time
- `Australia/Sydney` - Australian Eastern Time
- `Pacific/Auckland` - New Zealand Time

**Tip**: Use the sidebar to customize your clock display!
""")
