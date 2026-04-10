import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import streamlit.components.v1 as components 

st.set_page_config(page_title="Admin | Yearning in Manila", page_icon="🔒")

def get_spotify_embed_url(link):
    if isinstance(link, str) and "spotify.com" in link and "track/" in link:
        try:
            track_id = link.split("track/")[1].split("?")[0]
            return f"https://open.spotify.com/embed/track/{track_id}"
        except:
            return None
    return None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- UPDATED AUTHENTICATION LOGIC ---
def check_credentials():
    # Checks both username and password against your secrets file
    if (st.session_state.username_input == st.secrets["admin"]["username"] and 
        st.session_state.password_input == st.secrets["admin"]["password"]):
        st.session_state.logged_in = True
        # Clear the inputs so they don't linger in the background
        st.session_state.username_input = ""
        st.session_state.password_input = "" 
    else:
        st.error("Incorrect username or password.")

if not st.session_state.logged_in:
    st.title("🔒 Admin Access")
    st.text_input("Enter Username:", key="username_input")
    st.text_input("Enter Password:", type="password", key="password_input")
    st.button("Login", on_click=check_credentials) # Uses a button instead of hitting Enter
    st.stop() 
# ------------------------------------

@st.cache_resource
def get_sheet():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scopes)
    client = gspread.authorize(creds)
    return client.open_by_key("1cx__6k5O3s3FocpYWkuUc_sYso4mDexKxaXvie5jrSo").sheet1 

sheet = get_sheet()

st.title("🛡️ Moderation Dashboard")

records = sheet.get_all_records()
df = pd.DataFrame(records)

if not df.empty and "Status" in df.columns:
    pending_df = df[df["Status"] == "Pending"]
else:
    pending_df = pd.DataFrame()

st.subheader(f"Pending Messages: {len(pending_df)}")

if pending_df.empty:
    st.success("All caught up! No pending messages.")
else:
    for index, row in pending_df.iterrows():
        is_risk = row.get('Category') in ['Profanity', 'Sensitive Info', 'Crisis Risk']
        
        with st.container(border=True):
            if is_risk:
                st.error(f"⚠️ Flagged: {row.get('Category')}")
            else:
                st.success("✅ Safe")
            
            # Show if they requested to be featured
            if row.get('Featured') == "Requested":
                st.warning("🌟 User requested this to be Featured!")
                
            st.caption(f"Time: {row.get('Timestamp', 'Unknown')}")
            st.write(f"**To:** {row.get('Target_Name', 'Unknown')}")
            st.write(f"**Message:** {row.get('Message', 'Unknown')}")
            
            song_link = row.get('Song_Link', '')
            if pd.notna(song_link) and str(song_link).strip():
                embed_url = get_spotify_embed_url(str(song_link))
                if embed_url:
                    st.write("**Attached Soundtrack:**")
                    components.html(
                        f'<iframe style="border-radius:12px" src="{embed_url}?utm_source=generator&theme=0" width="100%" height="80" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>',
                        height=90
                    )
            
            # --- THE 3 NEW BUTTONS ---
            col1, col2, col3 = st.columns(3)
            sheet_row = index + 2 
            
            if col1.button("✅ Approve Normal", key=f"app_{index}"):
                sheet.update_cell(sheet_row, 5, "Approved") # Column 5 is Status
                sheet.update_cell(sheet_row, 8, "No")       # Column 8 is Featured
                st.rerun()
                
            if col2.button("🌟 Approve & Feature", key=f"feat_{index}"):
                sheet.update_cell(sheet_row, 5, "Approved")
                sheet.update_cell(sheet_row, 8, "Yes")
                st.rerun()
                
            if col3.button("🚫 Reject", key=f"rej_{index}"):
                sheet.update_cell(sheet_row, 5, "Rejected")
                sheet.update_cell(sheet_row, 8, "No")
                st.rerun()

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
