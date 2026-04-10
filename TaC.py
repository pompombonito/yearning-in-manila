import streamlit as st

# Custom CSS to match the app's aesthetic
style = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Times+New+Roman&display=swap');

.pink-text {
    color: #FFB6C1; /* Baby Pink */
    font-family: 'Times New Roman', Times, serif;
    font-size: 16px;
    line-height: 1.6;
    letter-spacing: 0.5px;
}

.highlight {
    font-style: italic;
    opacity: 0.9;
}
</style>
"""
st.markdown(style, unsafe_allow_html=True)

st.title("Terms & Conditions")

# NOTE: Keep the HTML tags pushed all the way to the left!
st.markdown(
"""
<div class="">
<p>Welcome to Yearning in Manila. By accessing and using this platform, you agree to the following terms and conditions. Please read them carefully, as they exist to keep this community safe, respectful, and true to its purpose.</p>

<br>
<strong>1. Purpose of the Platform</strong>
<p>This website is dedicated to the expression of unspoken feelings, appreciation, and innocent yearning. It is not a place for hate speech, cyberbullying, gossip, or malicious intent.</p>

<br>
<strong>2. Anonymity and Privacy</strong>
<ul style="list-style-type: disc; margin-left: 20px; margin-bottom: 15px;">
    <li>We use cryptographic hashing to differentiate users without ever storing raw IP addresses or personal tracking data. Your identity remains yours alone.</li>
    <li>In exchange for this anonymity, you must protect the privacy of others. You are strictly prohibited from posting the full names, phone numbers, home addresses, emails, or social media handles of any individual. First names, initials, or nicknames only.</li>
</ul>

<br>
<strong>3. Content Guidelines and Moderation</strong>
<ul style="list-style-type: disc; margin-left: 20px; margin-bottom: 15px;">
    <li>This is a moderated community. Every single submission is reviewed by an administrator before being published to the search or featured pages.</li>
    <li>The administrator reserves the absolute right to reject, ignore, or permanently delete any message that violates these guidelines, contains profanity, triggers our crisis filters, or risks the safety of others.</li>
    <li>Submissions that request to be on the "Featured" page are chosen at the administrator's sole discretion.</li>
</ul>

<br>
<strong>4. Third-Party Services (Spotify)</strong>
<p>Our soundtrack feature utilizes Spotify's official embedded web player. By attaching or playing a song on this site, you acknowledge that the music player itself is governed by Spotify's own Terms of Service and Privacy Policies.</p>

<br>
<strong>5. Non-Affiliation Disclaimer</strong>
<p class="highlight">This website is an independent, student-created project. It is strictly not affiliated with, endorsed by, funded by, or officially connected to Centro Escolar University (CEU) Manila or its administration in any capacity.</p>

<br>
<strong>6. Limitation of Liability</strong>
<p>While we actively moderate all submissions, the developer is not liable for any user-generated content submitted to the platform. By using this service, you agree to take full responsibility for the words you choose to send.</p>

<br>
<p>By submitting a message, you acknowledge that you have read, understood, and agreed to these terms. Thank you for helping us keep the art of expression beautiful.</p>
</div>
""", 
unsafe_allow_html=True
)