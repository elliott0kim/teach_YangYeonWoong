from flask import Flask, request, render_template, Response, jsonify
import numpy as np
import cv2
import openai

app = Flask(__name__)

is_streaming = False

# 글로벌 변수로 이미지를 저장하기 위한 변수
global_frame = None

@app.route('/video', methods=['POST'])
def receive_video():
    global global_frame
    # 클라이언트에서 전송한 파일 받기
    file = request.files['file'].read()

    # 이미지를 디코딩
    np_img = np.frombuffer(file, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    # 받은 이미지를 저장
    global_frame = img

    return 'Video Received', 200

@app.route('/video_feed')
def video_feed():
    def generate():
        global global_frame
        while True:
            if global_frame is not None:
                # 프레임을 JPEG로 인코딩
                ret, buffer = cv2.imencode('.jpg', global_frame)
                frame = buffer.tobytes()
                # 클라이언트에 전송
                yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/card1')
def card1():
    return render_template('card1.html')

@app.route('/card2')
def card2():
    return render_template('card2.html')

@app.route('/card3')
def card3():
    return render_template('card3.html')

@app.route('/live')
def live():
    return render_template('live.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    messages = data['messages']  # 대화 기록 받기

    try:
        # GPT API에 요청
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        gpt_message = response['choices'][0]['message']['content']
        
        # GPT의 응답을 대화 기록에 추가
        messages.append({"role": "assistant", "content": gpt_message})
        
        return jsonify({"message": gpt_message, "history": messages})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/quiz')
def index():
    return render_template('quiz_gpt.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
