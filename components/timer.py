import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import time


def render_timer(start_time: datetime, duration_minutes: int):
    """Render a real-time countdown timer using JavaScript."""
    if duration_minutes <= 0:
        return False, 0

    elapsed = datetime.now() - start_time
    total_seconds = duration_minutes * 60
    remaining_seconds = max(0, total_seconds - int(elapsed.total_seconds()))

    time_expired = remaining_seconds <= 0

    # JavaScript-based real-time countdown timer
    timer_html = f"""
    <div id="timer-container" style="text-align: center; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
        <div style="font-size: 14px; color: #666; margin-bottom: 5px;">Time Remaining</div>
        <div id="timer" style="font-size: 32px; font-weight: bold; font-family: monospace;"></div>
    </div>
    <script>
        var remainingSeconds = {remaining_seconds};
        var timerElement = document.getElementById('timer');
        var containerElement = document.getElementById('timer-container');

        function updateTimer() {{
            if (remainingSeconds <= 0) {{
                timerElement.innerHTML = "00:00:00";
                containerElement.style.backgroundColor = "#ffcccc";
                timerElement.style.color = "#cc0000";
                return;
            }}

            var hours = Math.floor(remainingSeconds / 3600);
            var minutes = Math.floor((remainingSeconds % 3600) / 60);
            var seconds = remainingSeconds % 60;

            var display = "";
            if (hours > 0) {{
                display = String(hours).padStart(2, '0') + ":" +
                          String(minutes).padStart(2, '0') + ":" +
                          String(seconds).padStart(2, '0');
            }} else {{
                display = String(minutes).padStart(2, '0') + ":" +
                          String(seconds).padStart(2, '0');
            }}

            timerElement.innerHTML = display;

            // Change color based on remaining time
            if (remainingSeconds <= 60) {{
                containerElement.style.backgroundColor = "#ffcccc";
                timerElement.style.color = "#cc0000";
            }} else if (remainingSeconds <= 300) {{
                containerElement.style.backgroundColor = "#fff3cd";
                timerElement.style.color = "#856404";
            }} else {{
                containerElement.style.backgroundColor = "#cce5ff";
                timerElement.style.color = "#004085";
            }}

            remainingSeconds--;
        }}

        updateTimer();
        setInterval(updateTimer, 1000);
    </script>
    """

    components.html(timer_html, height=100)

    return time_expired, int(elapsed.total_seconds())


def get_elapsed_time(start_time: datetime) -> int:
    """Get elapsed time in seconds."""
    elapsed = datetime.now() - start_time
    return int(elapsed.total_seconds())


def format_time(seconds: int) -> str:
    """Format seconds into MM:SS or HH:MM:SS format."""
    if seconds >= 3600:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"
