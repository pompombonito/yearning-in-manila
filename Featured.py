import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
import streamlit.components.v1 as components

# Copy over the theme so it looks consistent
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