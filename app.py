import streamlit as st
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# 1. UI Setup
st.set_page_config(page_title="SOP V2 Single Auditor", page_icon="🔍")
st.title("🔍 Single Link SOP Auditor")
st.info("Paste a branded link below to extract Shipping & Return attributes.")

# 2. Sidebar for your API Key
with st.sidebar:
    st.header("Setup")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.caption("Get your key at aistudio.google.com")

# 3. Input Field
url = st.text_input("Branded Website URL", placeholder="https://example.com/shipping-policy")

if st.button("Analyze Link"):
    if not api_key or not url:
        st.error("Please provide both the API Key and a URL.")
    else:
        with st.spinner("🔍 Reading website..."):
            try:
                # Scrape the page text
                res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
                soup = BeautifulSoup(res.text, 'html.parser')
                clean_text = soup.get_text(separator=' ', strip=True)

                # Configure AI
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')

                # Strict SOP Prompt
                prompt = f"""
                Analyze the following text strictly based on 'Shipping Attributes SOP V2'.
                
                Mandatory Checks:
                1. Q1: Does it ship to US 48 states? If no, stop and report 'Does not ship to US'.
                2. Extract: Shipping Threshold, Shipping Cost, Shipping Days, Return Cutoff, Window Type, and Return Fee.
                
                Site Text: {clean_text[:10000]}
                """

                response = model.generate_content(prompt)

                # 4. Display Results in a Clean Layout
                st.subheader("Audit Results")
                st.markdown(response.text)
                
                # Add a 'Copy' helper
                st.button("Done", on_click=lambda: st.success("Audit Reviewed!"))

            except Exception as e:

                st.error(f"Error: {e}")
