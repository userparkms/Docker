# 베이스 이미지: 경량 Python 3.11
FROM python:3.11-slim

# 작업 디렉터리 설정
WORKDIR /app

# 의존성 먼저 복사 (레이어 캐시 최적화)
COPY requirements.txt .

# 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 복사
COPY main.py .
COPY courses.json .

# 컨테이너 내부 포트 노출 (문서 목적)
EXPOSE 8000

# FastAPI 서버 실행 (0.0.0.0으로 외부 접근 허용)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]