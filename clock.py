import streamlit as st
from datetime import datetime
import pytz
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="World Clock - Multi-Timezone Display",
    page_icon="🕐",
    layout="wide"
)

# Custom CSS for clock styling
st.markdown("""
<style>
    .clock-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        text-align: center;
        color: white;
    }
    
    .timezone-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .timezone-time {
        font-size: 48px;
        font-weight: bold;
        font-family: 'Courier New', monospace;
        margin: 15px 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .timezone-date {
        font-size: 16px;
        opacity: 0.9;
        margin-bottom: 10px;
    }
    
    .timezone-offset {
        font-size: 14px;
        opacity: 0.8;
        background: rgba(255, 255, 255, 0.2);
        padding: 5px 10px;
        border-radius: 10px;
        display: inline-block;
    }
    
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
    }
    
    .header {
        text-align: center;
        margin: 30px 0 20px 0;
        color: #333;
    }
    
    .header h1 {
        font-size: 48px;
        margin: 0 0 10px 0;
        color: #667eea;
    }
    
    .header p {
        font-size: 16px;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <h1>🌍 World Clock</h1>
    <p>Real-time display of current time across multiple time zones</p>
</div>
""", unsafe_allow_html=True)

# Create two columns for sidebar and main content
col1, col2 = st.columns([1, 4])

with col1:
    st.subheader("⚙️ Settings")
    
    # Display format selector
    display_format = st.radio(
        "Time Format",
        ["12-hour (AM/PM)", "24-hour"]
    )
    
    # Clock style selector
    clock_style = st.radio(
        "Display Style",
        ["Grid", "List"]
    )
    
    # Sort preference
    sort_by = st.selectbox(
        "Sort by",
        ["UTC Offset", "Alphabetical", "Custom Order"]
    )
    
    # Refresh rate
    auto_refresh = st.checkbox("Auto-refresh (5 sec)", value=True)
    
    st.divider()
    st.subheader("📍 Add Custom Timezone")
    
    custom_tz = st.text_input(
        "Enter timezone (e.g., Asia/Tokyo, Europe/London)",
        placeholder="Type timezone name..."
    )
    
    if custom_tz and st.button("✅ Add Timezone"):
        if 'custom_timezones' not in st.session_state:
            st.session_state.custom_timezones = []
        
        try:
            # Validate timezone
            pytz.timezone(custom_tz)
            if custom_tz not in st.session_state.custom_timezones:
                st.session_state.custom_timezones.append(custom_tz)
                st.success(f"✅ Added {custom_tz}!")
                st.rerun()
            else:
                st.warning(f"⚠️ {custom_tz} is already added!")
        except pytz.exceptions.UnknownTimeZoneError:
            st.error(f"❌ Unknown timezone: {custom_tz}")

with col2:
    # Popular timezones
    popular_timezones = [
        'UTC',
        'America/New_York',
        'America/Los_Angeles',
        'Europe/London',
        'Europe/Paris',
        'Asia/Tokyo',
        'Asia/Shanghai',
        'Asia/Dubai',
        'Asia/Singapore',
        'Australia/Sydney',
        'Asia/Kolkata',
        'America/Toronto',
    ]
    
    # Add custom timezones if they exist
    if 'custom_timezones' in st.session_state:
        all_timezones = popular_timezones + st.session_state.custom_timezones
    else:
        all_timezones = popular_timezones
    
    # Sort timezones
    if sort_by == "UTC Offset":
        # Sort by UTC offset
        tz_data = []
        for tz_name in all_timezones:
            tz = pytz.timezone(tz_name)
            offset = datetime.now(tz).utcoffset().total_seconds() / 3600
            tz_data.append((tz_name, offset))
        tz_data.sort(key=lambda x: x[1])
        sorted_timezones = [item[0] for item in tz_data]
    elif sort_by == "Alphabetical":
        sorted_timezones = sorted(all_timezones)
    else:  # Custom Order
        sorted_timezones = all_timezones
    
    # Get current time for all timezones
    current_time_utc = datetime.now(pytz.UTC)
    
    # Create clock data
    clock_data = []
    for tz_name in sorted_timezones:
        try:
            tz = pytz.timezone(tz_name)
            local_time = current_time_utc.astimezone(tz)
            
            # Format time based on user preference
            if display_format == "12-hour (AM/PM)":
                time_str = local_time.strftime("%I:%M:%S %p")
            else:
                time_str = local_time.strftime("%H:%M:%S")
            
            date_str = local_time.strftime("%A, %B %d, %Y")
            
            # Calculate UTC offset
            offset = local_time.utcoffset()
            offset_hours = offset.total_seconds() / 3600
            offset_sign = "+" if offset_hours >= 0 else ""
            offset_str = f"UTC {offset_sign}{offset_hours:+.0f}:00" if offset_hours % 1 == 0 else f"UTC {offset_sign}{offset_hours:+.1f}"
            
            clock_data.append({
                'timezone': tz_name,
                'time': time_str,
                'date': date_str,
                'offset': offset_str,
                'city': tz_name.split('/')[-1].replace('_', ' ')
            })
        except Exception as e:
            st.error(f"Error with timezone {tz_name}: {e}")
    
    # Display clocks based on style
    if clock_style == "Grid":
        st.subheader("⏰ Current Times")
        cols = st.columns(3)
        
        for idx, clock_info in enumerate(clock_data):
            col = cols[idx % 3]
            with col:
                st.markdown(f"""
                <div class="clock-container">
                    <div class="timezone-title">{clock_info['city']}</div>
                    <div class="timezone-time">{clock_info['time']}</div>
                    <div class="timezone-date">{clock_info['date']}</div>
                    <div class="timezone-offset">{clock_info['offset']}</div>
                </div>
                """, unsafe_allow_html=True)
    
    else:  # List view
        st.subheader("⏰ Current Times")
        
        # Create a nicely formatted list
        for clock_info in clock_data:
            col1_list, col2_list, col3_list = st.columns([2, 2, 1])
            
            with col1_list:
                st.markdown(f"**{clock_info['city']}**")
                st.markdown(f"<small>{clock_info['timezone']}</small>", unsafe_allow_html=True)
            
            with col2_list:
                st.markdown(f"<h3>{clock_info['time']}</h3>", unsafe_allow_html=True)
                st.markdown(f"<small>{clock_info['date']}</small>", unsafe_allow_html=True)
            
            with col3_list:
                st.markdown(f"<small><strong>{clock_info['offset']}</strong></small>", unsafe_allow_html=True)
            
            st.divider()
    
    # Display table
    st.subheader("📊 Timezone Data Table")
    
    df = pd.DataFrame(clock_data)[['city', 'timezone', 'time', 'offset']]
    df.columns = ['City', 'Timezone', 'Current Time', 'UTC Offset']
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Show custom timezones info
    if 'custom_timezones' in st.session_state and st.session_state.custom_timezones:
        st.divider()
        st.subheader("🗑️ Manage Custom Timezones")
        
        col_remove1, col_remove2 = st.columns([3, 1])
        
        with col_remove1:
            tz_to_remove = st.selectbox(
                "Select timezone to remove:",
                st.session_state.custom_timezones,
                key="remove_tz_select"
            )
        
        with col_remove2:
            if st.button("❌ Remove", key="remove_tz_btn"):
                st.session_state.custom_timezones.remove(tz_to_remove)
                st.success(f"Removed {tz_to_remove}")
                st.rerun()

# Auto-refresh functionality
if auto_refresh:
    import time
    st.markdown("""
    <script>
        setTimeout(function() {
            window.location.reload();
        }, 5000);
    </script>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 12px;">
    <p>🌐 World Clock - Keep track of time across the globe</p>
    <p>Powered by Streamlit and Pytz</p>
</div>
""", unsafe_allow_html=True)
