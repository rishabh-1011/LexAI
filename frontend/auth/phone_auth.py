"""
frontend/auth/phone_auth.py
Phone OTP authentication using Twilio Verify.
"""

import requests
import streamlit as st
from backend.config import _get_secret

TWILIO_ACCOUNT_SID = _get_secret("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN  = _get_secret("TWILIO_AUTH_TOKEN")
TWILIO_VERIFY_SID  = _get_secret("TWILIO_VERIFY_SID")


def send_otp(phone_number: str) -> bool:
    """Send OTP to phone number via Twilio Verify."""

    url = (
        f"https://verify.twilio.com/v2/Services/"
        f"{TWILIO_VERIFY_SID}/Verifications"
    )

    try:
        response = requests.post(
            url,
            data={
                "To": phone_number,
                "Channel": "sms",
            },
            auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
            timeout=10,
        )

        st.write("Status Code:", response.status_code)
        st.write("Response:", response.text)

        return response.status_code == 201

    except Exception as e:
        st.exception(e)
        return False


def verify_otp(phone_number: str, code: str) -> bool:
    """Verify OTP code entered by user."""
    url = (
        f"https://verify.twilio.com/v2/Services/"
        f"{TWILIO_VERIFY_SID}/VerificationCheck"
    )
    try:
        response = requests.post(
            url,
            data={"To": phone_number, "Code": code},
            auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
            timeout=10,
        )
        data = response.json()
        return data.get("status") == "approved"
    except Exception:
        return False


def show_phone_login(key_prefix: str = "login"):
    """Render Phone OTP login form."""
    st.markdown("#### 📱 Phone OTP")

    phone = st.text_input(
        "Enter your phone number (with country code):",
        placeholder="+91XXXXXXXXXX",
        key=f"phone_input_{key_prefix}",
    )

    if st.button(
        "Send OTP",
        use_container_width=True,
        key=f"send_otp_btn_{key_prefix}",
    ):
        if not phone or not phone.startswith("+"):
            st.error("Please enter a valid phone number with country code.")
            return

        with st.spinner("Sending OTP..."):
            success = send_otp(phone)

        if success:
            st.success(f"✅ OTP sent to **{phone}**!")
            st.session_state[f"otp_phone_{key_prefix}"] = phone
        else:
            st.error("❌ Failed to send OTP. Please check the number and try again.")

    if f"otp_phone_{key_prefix}" in st.session_state:
        st.markdown("---")
        otp_code = st.text_input(
            "Enter the 6-digit OTP:",
            placeholder="123456",
            max_chars=6,
            key=f"otp_input_{key_prefix}",
        )

        if st.button(
            "Verify OTP",
            use_container_width=True,
            key=f"verify_otp_btn_{key_prefix}",
        ):
            if not otp_code or len(otp_code) != 6:
                st.error("Please enter a valid 6-digit OTP.")
                return

            with st.spinner("Verifying OTP..."):
                verified = verify_otp(
                    st.session_state[f"otp_phone_{key_prefix}"],
                    otp_code,
                )

            if verified:
                st.session_state["user"] = {
                    "phone":  st.session_state[f"otp_phone_{key_prefix}"],
                    "name":   "User",
                    "method": "phone",
                }
                st.session_state["logged_in"] = True
                del st.session_state[f"otp_phone_{key_prefix}"]
                st.rerun()
            else:
                st.error("❌ Invalid OTP. Please try again.")