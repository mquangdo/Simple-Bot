import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from src.workflow import build_graph

# 1. Khởi tạo FastAPI
app = FastAPI(title="Simple Bot")

# 2. Khởi tạo Graph (chỉ chạy 1 lần khi server start)
# Điều này giúp tiết kiệm tài nguyên và tăng tốc độ phản hồi
agent_app = build_graph()

# 3. Định nghĩa cấu trúc dữ liệu gửi từ Client (Frontend) lên
class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = "1"

# 4. Tạo địa chỉ (Endpoint) nhận tin nhắn
@app.post("/chat")
async def chat_with_agent(request: ChatRequest):
    try:
        # Cấu hình thread_id để Agent nhận diện phiên làm việc
        config = {"configurable": {"thread_id": request.thread_id}}
        
        # State ban đầu (Chỉ gửi tin nhắn mới nhất vào)
        # Lưu ý: Nếu bạn muốn lưu lịch sử, bạn cần dùng Checkpointer 
        # (như MemorySaver) khi build_graph.
        input_state = {"messages": [("user", request.message)]}
        
        # Thực thi Agent
        output = agent_app.invoke(input_state, config=config)
        
        # Lấy phản hồi cuối cùng
        final_message = output["messages"][-1]
        
        return {
            "reply": final_message.content,
            "thread_id": request.thread_id,
            "status": "success"
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# 5. Endpoint kiểm tra xem backend có đang sống không
@app.get("/health")
def health():
    return {"status": "running"}

if __name__ == "__main__":
    # Chạy server tại http://127.0.0.1:8000
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)