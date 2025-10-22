import os
import time

from dotenv import load_dotenv   # dotenv 패키지 사용
load_dotenv()  # 호출하면 .env 설정파일 읽어옴.

print(f'✅ {os.path.basename( __file__ )} 실행됨 {time.strftime('%Y-%m-%d %H:%M:%S')}')  # 실행파일명, 현재시간출력
print(f'\tOPENAI_API_KEY={os.getenv("OPENAI_API_KEY")[:20]}...') # OPENAI_API_KEY 필요!
