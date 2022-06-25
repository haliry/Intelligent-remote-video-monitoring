
# import the necessary packages
from pyimagesearch.motion_detection import SingleMotionDetector
from pyimagesearch import send_mail
#from picamera import PiCamera
from imutils.video import VideoStream
from flask import Response,session,redirect,url_for,request
from flask import Flask
from flask import render_template
#from flask_cors import *
import threading
import argparse
import datetime
import imutils
import time
import cv2
import sys
import inspect
import ctypes

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful for multiple browsers/tabs
# are viewing tthe stream)

outputFrame = None
lock = threading.Lock()
a=0
fc=0

# initialize a flask object

app = Flask(__name__)
app.secret_key='gakki'
#CORS(app, supports_credentials=True)

@app.route("/", methods=["GET", "POST"])
def index():
    username = session.get("username")

    if username:
        return redirect(url_for("demo_url_for"))

    if request.method == "GET":
        return render_template("index.html")
    # 获取参数
    username = request.form.get("username")
    password = request.form.get("password")
    # 校验参数
    if not all([username, password]):
        return render_template("index.html", errmsg="参数不足")

    # 校验对应的管理员用户数据
    if username == "xxx" and password == "xxx":
        # 验证通过
        session["username"] = username
        return redirect(url_for("demo_url_for"))

    return render_template("index.html", errmsg="用户名或密码错误")


@app.route('/demo')
def demo_url_for():
    return render_template("demo.html")

@app.route('/open',methods=['GET','POST'])
def open():
    global t, args, a, fc
    if request.method=='GET':
        return render_template("demo.html")
    else:
        if a==0:
            fc=0
            t = threading.Thread(target=detect_motion, args=(args["frame_count"],))
            t.daemon = True
            t.start()
            a=1
        return render_template("demo.html")

@app.route('/close',methods=['GET','POST'])
def close():
    global t, vs, a
    if request.method=='GET':
        return render_template("demo.html")
    else:
        if a==1:
            stop_thread(t)
            vs.stop()
            a=0
        return render_template("demo.html")

def _async_raise(tid, exctype):
    #"""raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

def resize(image, width=None, height=None):
    dim = None
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    resized = cv2.resize(image, dim, cv2.INTER_AREA)
    return resized


def detect_motion(frameCount):
    # grab global references to the video stream, output frame, and
    # lock variables
    global vs, outputFrame, lock, fc
    
    vs = VideoStream(usePiCamera=1).start()
    time.sleep(2.0)

    # initialize the motion detector and the total number of frames
    # read thus far
    md = SingleMotionDetector(accumWeight=0.1)
    total = 0
    
    # loop over frames from the video stream
    while True:
        # read the next frame from the video stream, resize it,
        # convert the frame to grayscale, and blur it
        frame = vs.read()
        #frame = imutils.resize(frame, width=400)
        frame = resize(frame, width=800, height=800)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        
        # grab the current timestamp and draw it on the frame
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.60, (255, 255, 255), 1)

        # if the total number of frames has reached a sufficient
        # number to construct a reasonable background model, then
        # continue to process the frame
        if total > frameCount:
            # detect motion in the image
            motion = md.detect(gray)

            # check to see if motion was found in the frame
            if motion is not None:
                # unpack the tuple and draw the box surrounding the
                # "motion area" on the output frame
                (thresh, (minX, minY, maxX, maxY)) = motion
                cv2.rectangle(frame, (minX, minY), (maxX, maxY),
                    (0, 0, 255), 2)
                fc += 1
                if fc==100:
                    cv2.imwrite("/home/pi/Downloads/stream-video-browser/img/p.jpg",frame)
                    send_mail.send()
                if fc>1000:
                    fc=0
        
        # update the background model and increment the total number
        # of frames read thus far
        md.update(gray)
        total += 1

        # acquire the lock, set the output frame, and release the
        # lock
        with lock:
            outputFrame = frame.copy()

        
def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock

    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue

            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
        mimetype = "multipart/x-mixed-replace; boundary=frame")

#GPIO.add_event_detect(input_flame, GPIO.RISING, callback=callback_flame)

# check to see if this is the main thread of execution
if __name__ == '__main__':
    # construct the argument parser and parse command line arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
        help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, required=True,
        help="ephemeral port number of the server (1024 to 65535)")
    ap.add_argument("-f", "--frame-count", type=int, default=16,
        help="# of frames used to construct the background model")
    args = vars(ap.parse_args())


    # start the flask app
    app.run(host=args["ip"], port=args["port"], debug=True,
        threaded=True, use_reloader=False)

# release the video stream pointer
#vs.stop()
