from config.graph import create_graph
import streamlit as st
import os

# Streamlit page setup
st.set_page_config(page_title="AI README Generator", layout="centered")
st.title("📘 AI README Generator")
st.markdown("Enter the path to the folder you want to analyze. You can copy it or drag the folder into the text box (on macOS/Windows).")

# Manual input for folder path
folder_path = st.text_input("📂 Enter folder path:")

# Validate and display selected folder
if folder_path:
    if os.path.isdir(folder_path):
        st.success(f"✅ Using folder: `{folder_path}`")
    else:
        st.error("❌ Invalid folder path. Please check the path and try again.")

# Button to generate README
if st.button("🚀 Generate README"):
    if folder_path and os.path.isdir(folder_path):
        with st.spinner("Analyzing folder contents with AI..."):
            try:
                app = create_graph()
                result = app.invoke({"route": folder_path})
                readme = result["readme"]

                if result:
                    st.success("✅ README successfully generated!")
                    st.markdown("---")
                    st.markdown("### ✨ README Preview")
                    st.markdown(readme if isinstance(readme, str) else str(readme))
                else:
                    st.error("❌ No content returned by the AI generator.")
            except Exception as e:
                st.error("⚠️ An error occurred:")
                st.code(str(e))
    else:
        st.warning("⚠️ Please enter a valid folder path before generating.")
