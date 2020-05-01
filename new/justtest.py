import loadFrames
import detect

loadFrames.loadFrame("/Users/brayb/Downloads/videos/bear.mp4")
labels=detect.detect()
print(labels)

