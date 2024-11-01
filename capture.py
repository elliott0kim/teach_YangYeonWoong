import cv2
import requests
import smtplib
import re
from email.mime.text import MIMEText

# 여기서 메일전송하기
import smtplib
from email.mime.text import MIMEText

# *------------------------------ 메일 전송 쪽 초기화 코드 ------------------------------ *
# 메일 전송 파라미터
send_info = dict(
    {"send_server" : "smtp.naver.com", # SMTP서버 주소
     "send_port" : 587, # SMTP서버 포트
     "send_user_id" : "maitsuji7@naver.com",
     "send_user_pw" : "mait2624141"
    }
)

# 전송할 메일 정보 작성
sender = send_info["send_user_id"]
receiver = "maitsuji7@gmail.com"

def send_email(send_info, to_email):
    title = "양연웅님의 라이브 방송이 시작되었습니다."
    content = "양연웅님의 라이브 방송이 시작되었습니다! 지금 보러 가실까요?"
    message = MIMEText(_text = content, _charset = "utf-8") # 메일 내용
    message['subject'] = title # 메일 제목
    message['from'] = sender # 보낸사람
    message['to'] = to_email # 받는사람
    
    # SMTP 세션 생성
    with smtplib.SMTP(send_info["send_server"], send_info["send_port"]) as server:
        # TLS 보안 연결
        server.starttls()
        # 보내는사람 계정으로 로그인
        server.login(send_info["send_user_id"], send_info["send_user_pw"])
        # 로그인 된 서버에 이메일 전송
        response = server.sendmail(message['from'], message['to'], message.as_string())
        # 이메일 전송 성공시
        if not response:
            print('이메일을 정상적으로 보냈습니다.')
        else:
            print(response)

# 이메일 주소 추출 및 메일 전송 함수
def extract_emails_and_send(filename):
    # 텍스트 파일 열기
    with open(filename, 'r') as file:
        text = file.read()
    # 이메일 주소 추출 (정규 표현식 사용)
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    # 추출된 이메일 주소에 메일 전송
    for email in emails:
        print(email)
        send_email(send_info, email)

# 텍스트 파일에서 이메일 추출 및 전송 시작
extract_emails_and_send('email_list.txt')


# *----------------------------------------------------------------------------------------- *


# 서버 URL 설정
url = 'http://127.0.0.1:5000/video'

# 웹캠 초기화
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # 이미지를 JPEG 형식으로 인코딩
    _, img_encoded = cv2.imencode('.jpg', frame)

    # 바이너리 형태로 변환하여 전송
    files = {'file': img_encoded.tobytes()}
    response = requests.post(url, files=files)

    # ESC 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break

# 웹캠 해제
cap.release()
