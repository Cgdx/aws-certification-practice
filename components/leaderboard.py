import streamlit as st
from auth import AuthManager, User
from typing import List, Dict, Any


def render_leaderboard_page(user: User, auth_manager: AuthManager):
    """Render the leaderboard page with weekly and all-time tabs."""
    st.title("🏆 Leaderboard")
    st.markdown("---")

    # Tabs for weekly and all-time
    tab_weekly, tab_alltime = st.tabs(["📅 This Week", "🌟 All Time"])

    with tab_weekly:
        render_leaderboard_tab(user, auth_manager, weekly=True)

    with tab_alltime:
        render_leaderboard_tab(user, auth_manager, weekly=False)


def render_leaderboard_tab(user: User, auth_manager: AuthManager, weekly: bool = False):
    """Render a leaderboard tab (weekly or all-time)."""
    leaderboard = auth_manager.get_leaderboard_users(weekly=weekly)

    period_text = "this week" if weekly else "all time"
    tab_prefix = "weekly" if weekly else "alltime"

    if not leaderboard:
        st.info(f"No users have opted into the leaderboard yet for {period_text}. Be the first!")
        st.markdown("Go to your **Profile** page and enable 'Appear in the leaderboard' to see your name here.")
        return

    # Top 3 Podium
    if len(leaderboard) >= 1:
        st.subheader("Top Performers")

        # Create podium display
        podium_cols = st.columns([1, 1, 1])

        # Second place (left)
        with podium_cols[0]:
            if len(leaderboard) >= 2:
                render_podium_card(leaderboard[1], user.id, auth_manager, tab_prefix=tab_prefix)
            else:
                st.empty()

        # First place (center)
        with podium_cols[1]:
            render_podium_card(leaderboard[0], user.id, auth_manager, is_first=True, tab_prefix=tab_prefix)

        # Third place (right)
        with podium_cols[2]:
            if len(leaderboard) >= 3:
                render_podium_card(leaderboard[2], user.id, auth_manager, tab_prefix=tab_prefix)
            else:
                st.empty()

        st.markdown("---")

    # Full leaderboard table
    st.subheader("Full Rankings")

    # Check if current user is in leaderboard
    if not user.show_in_leaderboard:
        st.info("You are not appearing in the leaderboard. Enable it in your Profile settings.")

    # Create table header
    header_cols = st.columns([1, 3, 2, 2])
    header_cols[0].markdown("**Rank**")
    header_cols[1].markdown("**Player**")
    header_cols[2].markdown("**Avg Score**")
    header_cols[3].markdown("**Experience**")

    st.markdown("---")

    # Create table rows
    for entry in leaderboard:
        is_current_user = entry['user_id'] == user.id

        row_cols = st.columns([1, 3, 2, 2])

        # Rank with trophy for top 3
        rank = entry['rank']
        rank_display = get_rank_display(rank)

        if is_current_user:
            row_cols[0].markdown(f"**{rank_display}**")
            # Make player name clickable
            if row_cols[1].button(f"**{entry['display_name']}** (You)", key=f"profile_{tab_prefix}_{entry['user_id']}"):
                st.session_state.view_profile_id = entry['user_id']
                st.session_state.page = "public_profile"
                st.rerun()
            row_cols[2].markdown(f"**{entry['avg_score']:.1f}%**")
            row_cols[3].markdown(f"**{entry['experience']:,} XP**")
        else:
            row_cols[0].markdown(rank_display)
            # Make player name clickable
            if row_cols[1].button(entry['display_name'], key=f"profile_{tab_prefix}_{entry['user_id']}"):
                st.session_state.view_profile_id = entry['user_id']
                st.session_state.page = "public_profile"
                st.rerun()
            row_cols[2].markdown(f"{entry['avg_score']:.1f}%")
            row_cols[3].markdown(f"{entry['experience']:,} XP")


def render_podium_card(entry: Dict[str, Any], current_user_id: int, auth_manager: AuthManager, is_first: bool = False, tab_prefix: str = ""):
    """Render a podium card for top 3 users."""
    is_current_user = entry['user_id'] == current_user_id
    rank = entry['rank']

    # Trophy colors and icons
    trophy_info = {
        1: {"color": "#FFD700", "trophy": "🥇", "bg": "linear-gradient(135deg, #FFD700, #FFA500)"},
        2: {"color": "#C0C0C0", "trophy": "🥈", "bg": "linear-gradient(135deg, #C0C0C0, #A0A0A0)"},
        3: {"color": "#CD7F32", "trophy": "🥉", "bg": "linear-gradient(135deg, #CD7F32, #8B4513)"}
    }

    info = trophy_info.get(rank, {"color": "#666", "trophy": f"#{rank}", "bg": "#666"})

    # Card height based on rank
    height = "200px" if is_first else "170px"

    player_name = entry['display_name']
    if is_current_user:
        player_name += " (You)"

    st.markdown(f"""
    <div style="
        text-align: center;
        padding: 20px;
        background: {info['bg']};
        border-radius: 15px;
        height: {height};
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    ">
        <div style="font-size: 3em;">{info['trophy']}</div>
        <div style="font-size: 1.1em; font-weight: bold; margin: 10px 0; color: white; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
            {player_name}
        </div>
        <div style="font-size: 1.3em; color: white; font-weight: bold;">
            {entry['avg_score']:.1f}%
        </div>
        <div style="font-size: 0.9em; color: rgba(255,255,255,0.9);">
            {entry['experience']:,} XP
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Clickable button to view profile
    if st.button("View Profile", key=f"podium_{tab_prefix}_{entry['user_id']}", use_container_width=True):
        st.session_state.view_profile_id = entry['user_id']
        st.session_state.page = "public_profile"
        st.rerun()


def get_rank_display(rank: int) -> str:
    """Get display string for rank with trophy emoji."""
    if rank == 1:
        return "🥇 1st"
    elif rank == 2:
        return "🥈 2nd"
    elif rank == 3:
        return "🥉 3rd"
    else:
        return f"#{rank}"
