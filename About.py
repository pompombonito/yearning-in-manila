import streamlit as st

# Custom CSS for the styling
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

st.title("About Us")

# NOTE: The text below must stay pushed all the way to the left side of the screen!
# If you press 'Tab' or 'Space' to indent these lines, it will turn into a grey box again.
st.markdown(
"""
<div class="">
<p>I know what it feels like to hold onto words you cannot say. That heavy, quiet feeling of yearning and longing for someone from afar, waiting for a moment that might never arrive.</p>

<p>This website was created because there are those who carry unsaid feelings. This platform is a safe space for anyone who feels the same way to finally express what is truly in their heart. And for those who are simply curious—yes, you can search your name. You never know who might be looking for you.</p>

<p>My greatest hope is that this site helps build beautiful connections, sparks courage, or at the very least, provides a way to unburden the weight of things left unsaid. We believe deeply in the beauty of expression, so long as it remains kind, respectful, and rooted in our community's ethical standards.</p>

<br>
<strong>About the Developer</strong>
<p></p>
<p>An undergraduate technology student. Like some or many of you using this site, I built this with the quiet hope of reaching a certain someone in whatever way I can.</p>

<p class="highlight">Every line of code in this project was written with someone specific in mind—someone from the Psychology Department, School of Science and Technology.</p>

<p>May your messages find their way through the rain.</p>
<br>
<p>Sincerely,<br>The Developer</p>
</div>
""", 
unsafe_allow_html=True
)