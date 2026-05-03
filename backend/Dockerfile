FROM python:3.12-slim

WORKDIR /app

# Cập nhật bảo mật và cài uv
RUN pip install uv && apt-get update && apt-get upgrade -y

# COPY từ thư mục gốc (Context) vào container
# Lưu ý: Khi build, ta đứng ở gốc nên đường dẫn vẫn là .
COPY . .

RUN uv sync --frozen

EXPOSE 8000

CMD ["uv", "run", "python", "-m", "backend.app"]
