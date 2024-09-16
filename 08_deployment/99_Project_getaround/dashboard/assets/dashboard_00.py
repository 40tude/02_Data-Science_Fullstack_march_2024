import os
import streamlit as st


def main():
    st.title("Streamlit")
    st.write("Blablabla...")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    main()
    os.system(f"streamlit run dashboard.py --server.port={port} --server.enableCORS=true")
