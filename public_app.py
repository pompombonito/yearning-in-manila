import streamlit as st
import gspread
import hashlib
from datetime import datetime, timedelta
import re
import pandas as pd
from google.oauth2.service_account import Credentials
import streamlit.components.v1 as components 

# --- 1. INITIAL CONFIG ---
st.set_page_config(page_title="Yearning in Manila | CEU Manila", page_icon="💌")

# <-- NEW: THE GLOBAL BANNER -->
st.markdown(
    "<p style='text-align: center; color: #FFB6C1; font-style: italic; font-family: \"Times New Roman\", Times, serif;'>"
    "✨ Welcome to Yearning in Manila v1.0! More features are coming soon, so stay tuned... ✨</p>", 
    unsafe_allow_html=True
)
st.divider() # Adds a nice faded line under the banner

def show_confession_page():
    # --- 3. THEME & UI ---
    style = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Times+New+Roman&display=swap');

    .pink-text {
        color: #FFB6C1; 
        font-family: 'Times New Roman', Times, serif;
        font-size: 16px;
        line-height: 1.5;
    }
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        border-radius: 10px;
        width: 100%;
    }
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

    st.title("Yearning in Manila | CEU Manila")

    st.markdown(
        '<p class="pink-text">We are not in any way affiliated with the university. '
        'All content shared here is independent and user-generated. '
        'Submissions will be reviewed by the admin for approval. </p>', 
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p class="pink-text">
        Please be kind and respectful. To protect privacy, do not disclose 
        full names or enter sensitive personal information. The main purpose of this website 
        is for messages/confessions of love, affection, and appreciation.
        </p>
        """, 
        unsafe_allow_html=True
    )

    # --- 4. SAFETY ENGINE & HELPER FUNCTIONS ---
    PROFANITY_WORDS = ["bobo", "gago", "tanga", "putangina", "pota", "ulol", "putaningamo",
                       "tangina", "puta", "hayup", "hayop", "kantot"] 
    CRISIS_WORDS = ["suicide", "kill myself", "mamatay", "ayoko na", "patayin niyo"]

    def get_hashed_ip():
        headers = st.context.headers
        ip = headers.get("X-Forwarded-For", "Local_User")
        return hashlib.sha256((ip + "CEU_Salt").encode()).hexdigest()

    def categorize_entry(message):
        msg = message.lower()
        if re.search(r"(09|\+639)\d{9}|[\w\.-]+@[\w\.-]+", msg): return "Sensitive Info"
        if any(w in msg for w in CRISIS_WORDS): return "Crisis Risk"
        if any(w in msg for w in PROFANITY_WORDS): return "Profanity"
        return "Safe"
        
    # <-- NEW: SPOTIFY VALIDATOR -->
    def is_valid_spotify_link(link):
        """Checks if the link is a valid Spotify Track URL"""
        if not link: 
            return True # Empty links are allowed since the soundtrack is optional
            
        # This Regex ensures the link starts with open.spotify.com/track/ followed by an ID
        pattern = r"^https?://open\.spotify\.com/track/[a-zA-Z0-9]+"
        return bool(re.match(pattern, link.strip()))

    def get_spotify_embed_url(link):
        if isinstance(link, str) and "open.spotify.com/track/" in link:
            try:
                # Extracts the track ID and ignores extra tracking tags like "?si=123"
                track_id = link.split("track/")[1].split("?")[0]
                return f"https://open.spotify.com/embed/track/{track_id}"
            except:
                return None
        return None

    # --- 5. DATABASE CONNECTION ---
    @st.cache_resource
    def connect_to_sheet():
        try:
            scopes = ["https://www.googleapis.com/auth/spreadsheets"]
            creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scopes)
            client = gspread.authorize(creds)
            return client.open_by_key("1cx__6k5O3s3FocpYWkuUc_sYso4mDexKxaXvie5jrSo").sheet1
        except Exception as e:
            st.error("Database Connection Error. Please check your Secrets or Spreadsheet ID.")
            return None

    sheet = connect_to_sheet()

    # --- 6. TABS ---
    tab1, tab2 = st.tabs(["📝 Submit a Message", "🔍 Search Messages"])

    # --- TAB 1: SUBMISSION ---
    with tab1:
        st.subheader("Send a Message")
        if sheet is None:
            st.warning("Database not connected.")
        else:
            with st.form("submission_form", clear_on_submit=True):
                target = st.text_input("To (First Name/Nickname, School or Dept.[optional]): (e.g., Juan, Dent)")
                msg_body = st.text_area("Your message:")
                song_link = st.text_input("Soundtrack (Optional):", placeholder="Paste a Spotify track link here...")
                
                wants_featured = st.checkbox("🌟 I want this to be considered for the Featured page")
                
                submitted = st.form_submit_button("Send Anonymously")

                if submitted:
                    if target and msg_body:
                        # <-- NEW: INTERCEPT INVALID SPOTIFY LINKS -->
                        if song_link and not is_valid_spotify_link(song_link):
                            st.error("❌ Invalid Spotify link detected. Please check for typos and ensure you are sharing a 'Song' link, not a playlist or album. (Example: https://open.spotify.com/track/...)")
                        else:
                            cat = categorize_entry(msg_body)
                            featured_val = "Requested" if wants_featured else "No"
                            
                            sheet.append_row([
                                (datetime.utcnow() + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S"), 
                                get_hashed_ip(), 
                                target, 
                                msg_body, 
                                "Pending", 
                                cat,
                                song_link.strip() if song_link else "", # Clean up accidental spaces
                                featured_val 
                            ])
                            
                            if cat == "Safe":
                                st.success("✨ Sent! It will appear once approved by the admin.")
                            else:
                                st.warning("⚠️ Submitted. Please keep entries wholesome; admins will review this strictly.")
                    else:
                        st.error("Fields cannot be empty.")

    # --- TAB 2: SEARCH / READ ---
    with tab2:
        st.subheader("Find messages for you")
        search_query = st.text_input("Search by Name/School/Dept.:", placeholder="Type a name...")
        
        st.caption("💡 *Tip: If your name/nickname is only 1-2 letters long (e.g., 'AJ', 'Bo'), or if you want to find your exact name without seeing similar ones (e.g., searching 'Dan' without seeing 'Daniel'), toggle the checkbox below.*")
        exact_match = st.checkbox("☑️ Exact name match")
        
        if st.button("Search"):
            search_query = search_query.strip()
            
            if not search_query:
                st.warning("⚠️ Please type a name to search.")
                
            elif not exact_match and len(search_query) < 3:
                st.warning("⚠️ Please enter at least 3 characters. For shorter names, please check the 'Exact name match' box above.")
                
            else:
                if sheet is None:
                    st.error("Database unavailable.")
                else:
                    raw_data = sheet.get_all_values()
                    if len(raw_data) > 1:
                        df = pd.DataFrame(raw_data[1:], columns=raw_data[0])
                        approved_data = df[df["Status"] == "Approved"]
                        
                        if exact_match:
                            results = approved_data[approved_data["Target_Name"].str.contains(rf"\b{re.escape(search_query)}\b", case=False, na=False, regex=True)]
                        else:
                            results = approved_data[approved_data["Target_Name"].str.contains(search_query, case=False, na=False)]
                        
                        if not results.empty:
                            st.write(f"Found {len(results)} message(s):")
                            for _, row in results.iterrows():
                                with st.container(border=True):
                                    st.info(f"💌 **To: {row['Target_Name']}**")
                                    st.write(row['Message'])
                                    
                                    if 'Song_Link' in row and pd.notna(row['Song_Link']) and str(row['Song_Link']).strip():
                                        embed_url = get_spotify_embed_url(str(row['Song_Link']))
                                        if embed_url:
                                            components.html(
                                                f'<iframe style="border-radius:12px" src="{embed_url}?utm_source=generator&theme=0" width="100%" height="80" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>',
                                                height=90
                                            )
                                            
                                    st.caption(f"Posted on: {row['Timestamp']}")
                        else:
                            st.info("No approved messages found for this name yet.")
                    else:
                        st.write("The board is currently empty.")


# --- EXECUTION LOGIC ---
try:
    pages = {
        "Confessions": st.Page(show_confession_page, title="Yearning in Manila", default=True),
        "Featured": st.Page("Featured.py", title="🌟 Featured Entries 🌟"), 
        "About": st.Page("About.py", title="About Us"),
        "Terms": st.Page("TaC.py", title="Terms & Conditions"),
        "Privacy": st.Page("Privacy.py", title="Privacy Protection")
    }
    pg = st.navigation(list(pages.values()))
    pg.run()
except Exception as e:
    show_confession_page()


style = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Times+New+Roman&display=swap');
.pink-text { color: #FFB6C1; font-family: 'Times New Roman', Times, serif; font-size: 16px; line-height: 1.5; }
</style>
"""
st.markdown(style, unsafe_allow_html=True)

st.title("Featured Entries")

# Spotify Helper
def get_spotify_embed_url(link):
    if isinstance(link, str) and "spotify.com" in link and "track/" in link:
        try:
            return f"https://open.spotify.com/embed/track/{link.split('track/')[1].split('?')[0]}"
        except:
            return None
    return None

# Connect to database
@st.cache_resource
def get_featured_data():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scopes)
    client = gspread.authorize(creds)
    return client.open_by_key("1cx__6k5O3s3FocpYWkuUc_sYso4mDexKxaXvie5jrSo").sheet1

sheet = get_featured_data()
raw_data = sheet.get_all_values()

if len(raw_data) > 1:
    df = pd.DataFrame(raw_data[1:], columns=raw_data[0])
    
    # SAFETY: Only show entries that are Approved AND marked as "Yes" for Featured
    if "Status" in df.columns and "Featured" in df.columns:
        featured_df = df[(df["Status"] == "Approved") & (df["Featured"] == "Yes")]
        
        if not featured_df.empty:
            # We reverse the order so the newest featured posts show at the top!
            for _, row in featured_df.iloc[::-1].iterrows():
                with st.container(border=True):
                    st.info(f"💌 **To: {row.get('Target_Name', 'Unknown')}**")
                    st.write(row.get('Message', ''))
                    
                    # Embed Song if it has one
                    song_link = row.get('Song_Link', '')
                    if pd.notna(song_link) and str(song_link).strip():
                        embed_url = get_spotify_embed_url(str(song_link))
                        if embed_url:
                            components.html(
                                f'<iframe style="border-radius:12px" src="{embed_url}?utm_source=generator&theme=0" width="100%" height="80" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>',
                                height=90
                            )
                    st.caption(f"Posted on: {row.get('Timestamp', '')}")
        else:
            st.write("No featured entries yet. Keep checking back!")

st.markdown(
        '<p class="pink-text">All submissions are anonymous. Any submission that contains sensitive data will be flagged by the system and therefore rejected. </p>'
        '<p class="pink-text">For comments, suggestions, and takedown requests, use the "Send a Message" feature. (To: ADMIN; then state your message) </p>',
        unsafe_allow_html=True
    )
