from Dxr_video.VideoStreamer import VideoStreamer
import cv2

# 设置别名和视频流URL
alias = "stream"
pull_stream_url = 0

# 打开视频流
cap = cv2.VideoCapture(pull_stream_url)
# 获取视频的宽度和高度
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# 创建VideoStreamer对象
streamer = VideoStreamer(alias, width=width, height=height, ip="10.10.8.43")

while True:
    # 循环读取视频帧，并推送到RTMP服务器
    ret, frame = cap.read()
    if ret:
        streamer.push_frame(frame)
    else:
        break