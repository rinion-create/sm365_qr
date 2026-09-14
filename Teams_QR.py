"""Streamlit app: turn a Teams meeting link into a QR code.

Run:
    pip install streamlit qrcode[pil]
    streamlit run app.py
"""

import io
from urllib.parse import urlparse

import qrcode
import streamlit as st

st.set_page_config(page_title="Teams Link → QR", page_icon="🔗", layout="centered")


def is_valid_url(value: str) -> bool:
    parsed = urlparse(value.strip())
    return bool(parsed.scheme) and bool(parsed.netloc)


def is_teams_link(value: str) -> bool:
    host = urlparse(value.strip()).netloc.lower()
    return "teams.microsoft.com" in host or "teams.live.com" in host


def build_qr_image(link: str, box_size: int = 10):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")


st.title("Teams link → QR code")
st.caption("Paste a Microsoft Teams meeting link and get a scannable QR code instantly. Nothing leaves your machine.")

link = st.text_input("Teams meeting link", placeholder="https://teams.microsoft.com/l/meetup-join/…")

box_size = st.slider("QR size (box size)", min_value=4, max_value=20, value=10)

if link:
    link = link.strip()
    if not is_valid_url(link):
        st.error("That doesn't look like a valid URL.")
    else:
        if not is_teams_link(link):
            st.warning("This doesn't look like a teams.microsoft.com or teams.live.com link — generating anyway.")

        img = build_qr_image(link, box_size=box_size)

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        st.image(buf, caption="Scan to join", width=box_size * 33)

        st.download_button(
            "Download PNG",
            data=buf,
            file_name="teams-meeting-qr.png",
            mime="image/png",
        )
else:
    st.info("Enter a link above to generate its QR code.")