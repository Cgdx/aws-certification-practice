import streamlit as st
from auth import AuthManager, User
from auth.models import AWS_CERTIFICATIONS
from datetime import datetime


def render_profile_page(user: User, auth_manager: AuthManager):
    """Render the user profile page."""
    st.title("👤 My Profile")
    st.markdown("---")

    # Refresh user data to get latest experience
    updated_user = auth_manager.get_user_by_id(user.id)
    if updated_user:
        user = updated_user
        st.session_state.user = user

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Profile Information")

        with st.form("profile_form"):
            nickname = st.text_input(
                "Nickname (Display Name)",
                value=user.nickname or "",
                help="This name will be shown in the leaderboard if you opt in"
            )

            st.text_input(
                "Username",
                value=user.username,
                disabled=True,
                help="Username cannot be changed"
            )

            st.text_input(
                "Email",
                value=user.email,
                disabled=True,
                help="Email cannot be changed"
            )

            phone = st.text_input(
                "Phone (optional)",
                value=user.phone or ""
            )

            credly_url = st.text_input(
                "Credly Profile URL (optional)",
                value=user.credly_url or "",
                help="Link to your Credly profile to showcase your badges",
                placeholder="https://www.credly.com/users/your-username"
            )

            st.markdown("---")

            show_in_leaderboard = st.checkbox(
                "Appear in the leaderboard",
                value=user.show_in_leaderboard,
                help="If enabled, your nickname and scores will be visible to other users"
            )

            if show_in_leaderboard and not nickname:
                st.warning("A nickname is required to appear in the leaderboard")

            submitted = st.form_submit_button("Save Profile", use_container_width=True)

            if submitted:
                # Validate: nickname required if opting into leaderboard
                if show_in_leaderboard and not nickname.strip():
                    st.error("Please enter a nickname to appear in the leaderboard")
                else:
                    success, message = auth_manager.update_user_profile(
                        user_id=user.id,
                        nickname=nickname.strip() if nickname.strip() else None,
                        phone=phone.strip() if phone.strip() else None,
                        show_in_leaderboard=show_in_leaderboard,
                        credly_url=credly_url.strip() if credly_url.strip() else None
                    )

                    if success:
                        st.success(message)
                        # Update session state user
                        user.nickname = nickname.strip() if nickname.strip() else None
                        user.phone = phone.strip() if phone.strip() else None
                        user.show_in_leaderboard = show_in_leaderboard
                        user.credly_url = credly_url.strip() if credly_url.strip() else None
                        st.session_state.user = user
                        st.rerun()
                    else:
                        st.error(message)

    with col2:
        st.subheader("Account Details")

        # Experience display
        st.markdown(f"""
        <div style="
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 10px;
            color: white;
            margin-bottom: 20px;
        ">
            <div style="font-size: 0.9em; opacity: 0.9;">Experience</div>
            <div style="font-size: 2em; font-weight: bold;">{user.experience:,} XP</div>
            <div style="font-size: 0.9em; opacity: 0.9;">Level {user.level}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        **Account Type:** {user.auth_provider.title()}

        **Member Since:** {user.created_at.strftime('%B %d, %Y')}

        **Last Login:** {user.last_login.strftime('%B %d, %Y at %H:%M') if user.last_login else 'N/A'}
        """)

        if user.credly_url:
            st.markdown(f"[View Credly Profile]({user.credly_url})")

        # Password change section - only for email users
        if user.auth_provider == 'email':
            st.markdown("---")
            st.subheader("Change Password")

            with st.form("password_form"):
                current_password = st.text_input(
                    "Current Password",
                    type="password"
                )

                new_password = st.text_input(
                    "New Password",
                    type="password"
                )

                confirm_password = st.text_input(
                    "Confirm New Password",
                    type="password"
                )

                st.caption("Password must be at least 8 characters with uppercase, lowercase, and a digit.")

                pwd_submitted = st.form_submit_button("Change Password", use_container_width=True)

                if pwd_submitted:
                    if not current_password or not new_password or not confirm_password:
                        st.error("Please fill in all password fields")
                    elif new_password != confirm_password:
                        st.error("New passwords do not match")
                    else:
                        success, message = auth_manager.change_password(
                            user_id=user.id,
                            current_password=current_password,
                            new_password=new_password
                        )

                        if success:
                            st.success(message)
                        else:
                            st.error(message)
        else:
            st.info(f"You signed in with {user.auth_provider.title()}. Password management is handled by your {user.auth_provider.title()} account.")

    # Certifications Section
    st.markdown("---")
    st.subheader("🎖️ My AWS Certifications")

    certifications = auth_manager.get_user_certifications(user.id)

    if certifications:
        cert_cols = st.columns(3)
        for i, cert in enumerate(certifications):
            with cert_cols[i % 3]:
                render_certification_badge(cert, auth_manager, user.id)
    else:
        st.info("No certifications added yet. Add your AWS certifications below!")

    # Add new certification
    st.markdown("---")
    st.subheader("Add Certification")

    with st.form("add_cert_form"):
        cert_col1, cert_col2 = st.columns(2)

        with cert_col1:
            cert_code = st.selectbox(
                "Certification",
                options=list(AWS_CERTIFICATIONS.keys()),
                format_func=lambda x: f"{x} - {AWS_CERTIFICATIONS[x]}"
            )

            issued_date = st.date_input(
                "Issue Date",
                value=None
            )

        with cert_col2:
            credential_id = st.text_input(
                "Credential ID (optional)",
                placeholder="e.g., ABC123XYZ"
            )

            expiry_date = st.date_input(
                "Expiry Date (optional)",
                value=None
            )

        credly_badge = st.text_input(
            "Credly Badge URL (optional)",
            placeholder="https://www.credly.com/badges/..."
        )

        add_cert = st.form_submit_button("Add Certification", use_container_width=True)

        if add_cert:
            cert_name = AWS_CERTIFICATIONS.get(cert_code, cert_code)
            success, message = auth_manager.add_certification(
                user_id=user.id,
                name=cert_name,
                code=cert_code,
                issued_date=datetime.combine(issued_date, datetime.min.time()) if issued_date else None,
                expiry_date=datetime.combine(expiry_date, datetime.min.time()) if expiry_date else None,
                credential_id=credential_id.strip() if credential_id else None,
                credly_badge_url=credly_badge.strip() if credly_badge else None
            )

            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)


def render_certification_badge(cert, auth_manager: AuthManager, user_id: int):
    """Render a certification badge card."""
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

    expiry_text = ""
    if cert.expiry_date:
        if cert.expiry_date < datetime.now():
            expiry_text = "<span style='color: #dc3545;'>Expired</span>"
        else:
            expiry_text = f"Expires: {cert.expiry_date.strftime('%b %Y')}"

    st.markdown(f"""
    <div style="
        padding: 15px;
        background: linear-gradient(135deg, {color}22, {color}44);
        border: 2px solid {color};
        border-radius: 10px;
        margin-bottom: 10px;
    ">
        <div style="font-weight: bold; color: {color};">{cert.code}</div>
        <div style="font-size: 0.9em; margin: 5px 0;">{cert.name}</div>
        <div style="font-size: 0.8em; color: #666;">
            {f"Issued: {cert.issued_date.strftime('%b %Y')}" if cert.issued_date else ""}
        </div>
        <div style="font-size: 0.8em;">{expiry_text}</div>
    </div>
    """, unsafe_allow_html=True)

    # Actions
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if cert.credly_badge_url:
            st.link_button("View Badge", cert.credly_badge_url, use_container_width=True)
    with btn_col2:
        if st.button("Delete", key=f"del_cert_{cert.id}", use_container_width=True):
            auth_manager.delete_certification(cert.id, user_id)
            st.rerun()
