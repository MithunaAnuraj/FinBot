import streamlit as st
from dotenv import load_dotenv
from doc_processing import get_retrievertools
from tool_list import get_repl
from agent import create_agent_chase_way
from PIL import Image
# from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
import textwrap

# Initialize tools and agent
session_state = st.session_state
if 'tools' not in session_state:
    session_state.tools = []
if 'agent' not in session_state:
    session_state.agent = None

def initialize_tools():
    if not session_state.tools:
        session_state.tools = get_repl(session_state.tools)

def re_initialize_agent():
    session_state.tools = get_repl(session_state.tools)
    session_state.agent = create_agent_chase_way(session_state.tools)

def initialize_agent():
    if not session_state.agent:
        initialize_tools()  # Ensure tools are initialized
        session_state.agent = create_agent_chase_way(session_state.tools)

def main():
    #load_dotenv()
    st.set_page_config(page_title="Fin bot", page_icon="🕵️‍♀️", menu_items={
        'About': "**Your AI-powered financial assistant.** Analyze reports, compare metrics, and gain insights with ease!"
    })
    st.title("Fin Bot")

    if 'files' not in session_state:
        session_state.files = []

    image = Image.open("Des3.png")

    files = st.sidebar.file_uploader(label="Upload your pdfs here", accept_multiple_files=True, type="pdf")
    st.sidebar.image(image)
    if files:
        # new_files = [file for file in files if file not in session_state.files]
        new_files = [file for file in files if file.name not in [f.name for f in session_state.files if f is not None]]
        if new_files:
            session_state.files.extend(new_files)
            new_tools = get_retrievertools(new_files)
            if new_tools:
                session_state.tools.extend(new_tools)
                re_initialize_agent()  # Reinitialize agent when tools are updated

    if prompt := st.chat_input():
        st.chat_message("user").write(prompt)
        with st.chat_message("assistant", avatar="bot.png"):
            initialize_agent()
            # container = st.container()
            # st_callback = StreamlitCallbackHandler(container)
            # response = session_state.agent.invoke(
            #     {"input": prompt}, {"callbacks": [st_callback]}
            # )
            response = session_state.agent.invoke({"input": prompt})
            #st.write(response["output"].replace("$", "/$"))
            #st.markdown("""response["output"].replace("$", "/$")""")
            st.write(response["output"])
            output_text = response["output"]
            wrapped_text = "\n".join(textwrap.wrap(output_text, width=80))
            #styled_text = f'<span style="font-family: Arial, sans-serif;">{wrapped_text}</span>'
            #st.markdown(styled_text, unsafe_allow_html=True)
            #st.text(styled_text)

if __name__ == "__main__":
    main()
