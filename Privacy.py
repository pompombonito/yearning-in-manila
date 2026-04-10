import streamlit as st

# Custom CSS for the styling
style = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Times+New+Roman&display=swap');

.pink-text {
    color: #FFB6C1; /* Baby Pink */
    font-family: 'Times New Roman', Times, serif;
    font-size: 16px;
    line-height: 1.5;
}
</style>
"""
st.markdown(style, unsafe_allow_html=True)

st.title("Privacy Protection & Anonymity")

st.markdown(
    """
    <div class="">
        <strong>1. Data Minimization</strong>
        <ul style="list-style-type: disc; margin-left: 20px;">
            We believe in collecting only what is strictly necessary to keep this community running.
            <li><strong>No Account Required:</strong> You do not need to provide an email, phone number, or social media profile to post a confession.</li>
            <li><strong>No Personal Identifiers:</strong> We do not ask for your name, age, or location. Your identity remains known only to you.</li>
        </ul>
        <strong>2. IP Anonymization (Hashing)</strong>
        <ul style="list-style-type: disc; margin-left: 20px;">
            To prevent spam and maintain site integrity without tracking your physical location:
            <li>We do not store your raw IP address.</li>
            <li>Instead, we use a one-way cryptographic hash. This turns your IP into a random string of characters that allows our system to recognize unique sessions without ever knowing who you are or where you are connecting from.</li>
            <li>This hash cannot be reversed to reveal your original IP address.</li>
        </ul>
        <strong>3. Protecting the Community</strong>
        <ul style="list-style-type: disc; margin-left: 20px;">
            While we protect your identity, we also protect the privacy of others:
            <li>No Full Names: We strictly prohibit the disclosure of full names. Please use initials, first names, or nicknames.</li>
            <li>No Sensitive Data: Do not enter addresses, contact details, or private information.</li>
            <li>Moderation: Posts containing doxxing or sensitive personal information will be removed to ensure the safety of the community.</li>
        </ul>
        <strong>4. Data Encryption</strong>
        <ul style="list-style-type: disc; margin-left: 20px;">
        Your connection to this site is encrypted via SSL (Secure Sockets Layer). This ensures that any message you send is encrypted between your device and our server, preventing third parties from "eavesdropping" on your messages while they are being sent.
        </ul>
        <strong>5. Your Responsibility</strong>
        <ul style="list-style-type: disc; margin-left: 20px;">
        Anonymity is a two-way street. To remain truly anonymous:
        <li>Avoid including over-specific details in your messages that could easily identify you (e.g., "I sat next to you in the 3rd row of Tuesday's 9 AM lecture wearing my red jacket", unless you really wish to be identified by your target audience).</li>
        <li>Be mindful that while we protect your digital footprint, the content you write is what keeps you hidden.</li>
        </ul>
    </div>
    """, 
    unsafe_allow_html=True
)