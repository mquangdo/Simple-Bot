import streamlit as st
import requests
import uuid
import os  # IMPORT ADDED

# 1. Configuration
st.set_page_config(page_title="Simple Bot", page_icon="🤖")
st.title("🤖 Simple Bot")
st.caption("Hệ thống Agent hỗ trợ nghiên cứu và thực thi tác vụ")

# 2. Session State (for storing chat history on UI)
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    # Generate unique ID for each session
    st.session_state.thread_id = str(uuid.uuid4())

# 3. Sidebar - Configuration area
with st.sidebar:
    st.header("Configuration")
    
    # 1. Lấy URL từ biến môi trường, mặc định là localhost nếu không tìm thấy
    # Trong docker-compose, BACKEND_URL nên là "http://backend:8000/chat"
    raw_backend_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000/chat")
    
    # 2. Đảm bảo URL luôn có đuôi /chat bất kể cấu hình môi trường ra sao
    if not raw_backend_url.endswith("/chat"):
        backend_url_to_use = f"{raw_backend_url}/chat"
    else:
        backend_url_to_use = raw_backend_url
    
    # 3. Cho phép chỉnh sửa trên giao diện (nếu cần)
    backend_url_input = st.text_input("Backend URL", value=backend_url_to_use)
    st.session_state.backend_url = backend_url_input
    
    # Hiển thị URL đang kết nối để bạn dễ kiểm tra (Debug)
    if "backend" in backend_url_input:
        st.success(f"🌐 Docker Mode: {backend_url_input}")
    else:
        st.warning(f"💻 Local Mode: {backend_url_input}")

    # Show current thread ID
    st.info(f"Thread ID: {st.session_state.thread_id}")
    
    if st.button("Clear chat history"):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

# 4. Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Input field for user
if prompt := st.chat_input("How can I help you?"):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 6. Send request to Backend FastAPI
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            try:
                payload = {
                    "message": prompt,
                    "thread_id": st.session_state.thread_id
                }

                response = requests.post(st.session_state.backend_url, json=payload)

                if response.status_code == 200:
                    answer = response.json().get("reply", "No response received.")
                    st.markdown(answer)
                    # Save to history
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"Backend Error: {response.status_code}")
                    st.error(response.text)

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to Backend. Ensure backend is running at the configured URL.")
                st.info("For Docker: use http://backend:8000/chat")
                st.info("For local: use http://127.0.0.1:8000/chat")
