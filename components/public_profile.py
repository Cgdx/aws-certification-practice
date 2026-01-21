import streamlit as st
from auth import AuthManager, User
from datetime import datetime


def render_public_profile_page(user: User, auth_manager: AuthManager):
    """Render a public profile page for viewing other users."""
    # Get the profile ID to view
    profile_id = st.session_state.get('view_profile_id')

    if not profile_id:
        st.error("No profile selected")
        if st.button("Back to Leaderboard"):
            st.session_state.page = "leaderboard"
            st.rerun()
        return

    # Get public profile data
    profile = auth_manager.get_public_profile(profile_id)

    if not profile:
        st.error("This profile is not public or does not exist")
        if st.button("Back to Leaderboard"):
            st.session_state.page = "leaderboard"
            st.rerun()
        return

    # Back button
    if st.button("← Back to Leaderboard"):
        st.session_state.page = "leaderboard"
        st.rerun()

    st.markdown("---")

    # Profile header
    col1, col2 = st.columns([2, 1])

    with col1:
        st.title(f"👤 {profile['display_name']}")

        # Check if viewing own profile
        if profile_id == user.id:
            st.caption("This is your public profile")

        # Experience and level
        level = profile['experience'] // 100 + 1
        st.markdown(f"""
        <div style="
            display: inline-block;
            padding: 10px 20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 20px;
            color: white;
            margin: 10px 0;
        ">
            <span style="font-size: 1.2em; font-weight: bold;">{profile['experience']:,} XP</span>
            <span style="opacity: 0.9;"> • Level {level}</span>
        </div>
        """, unsafe_allow_html=True)

        # Member since
        if profile.get('member_since'):
            member_date = profile['member_since']
            if isinstance(member_date, str):
                member_date = datetime.fromisoformat(member_date)
            st.caption(f"Member since {member_date.strftime('%B %Y')}")

    with col2:
        # Stats card
        st.markdown(f"""
        <div style="
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
            text-align: center;
        ">
            <div style="font-size: 2em; font-weight: bold; color: #28a745;">
                {profile['avg_score']:.1f}%
            </div>
            <div style="color: #666;">Average Score</div>
            <hr style="margin: 10px 0;">
            <div style="font-size: 1.5em; font-weight: bold; color: #007bff;">
                {profile['best_score']:.1f}%
            </div>
            <div style="color: #666;">Best Score</div>
            <hr style="margin: 10px 0;">
            <div style="font-size: 1.5em; font-weight: bold; color: #6c757d;">
                {profile['exams_taken']}
            </div>
            <div style="color: #666;">Exams Taken</div>
        </div>
        """, unsafe_allow_html=True)

    # Credly link
    if profile.get('credly_url'):
        st.markdown("---")
        st.link_button("🔗 View Credly Profile", profile['credly_url'], use_container_width=False)

    # Certifications
    st.markdown("---")
    st.subheader("🎖️ AWS Certifications")

    certifications = profile.get('certifications', [])

    if certifications:
        cert_cols = st.columns(4)
        for i, cert in enumerate(certifications):
            with cert_cols[i % 4]:
                render_public_cert_badge(cert)
    else:
        st.info("No certifications displayed")


def render_public_cert_badge(cert):
    """Render a certification badge for public view."""
    # Badge colors based on certification level
    badge_colors = {
        "CLF": "#6c757d",  # Gray - Foundational
        "SAA": "#28a745",  # Green - Associate
        "SOA": "#28a745",
        "DVA": "#28a745",
        "SAP": "#fd7e14",  # Orange - Professional
        "DOP": "#fd7e14",
        "ANS": "#dc3545",  # Red - Specialty
        "SCS": "#dc3545",
        "MLS": "#dc3545",
        "DBS": "#dc3545",
        "PAS": "#dc3545",
        "AIF": "#6c757d"   # Gray - Foundational
    }

    prefix = cert.code[:3] if cert.code else ""
    color = badge_colors.get(prefix, "#007bff")

    # Determine badge status
    status_badge = ""
    if cert.expiry_date:
        if cert.expiry_date < datetime.now():
            status_badge = "<div style='color: #dc3545; font-size: 0.7em;'>Expired</div>"
        else:
            status_badge = "<div style='color: #28a745; font-size: 0.7em;'>Active</div>"

    st.markdown(f"""
    <div style="
        padding: 15px;
        background: linear-gradient(135deg, {color}22, {color}44);
        border: 2px solid {color};
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: center;
    ">
        <div style="font-size: 1.5em; font-weight: bold; color: {color};">{cert.code}</div>
        <div style="font-size: 0.8em; margin: 5px 0; color: #333;">{cert.name}</div>
        {status_badge}
    </div>
    """, unsafe_allow_html=True)

    if cert.credly_badge_url:
        st.link_button("View Badge", cert.credly_badge_url, use_container_width=True)
