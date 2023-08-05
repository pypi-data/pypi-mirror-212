import face_recognition as fr
import cv2
import dlib
class Face:
    video_capture = cv2.VideoCapture(0)
    dect=dlib.get_frontal_face_detector()
    def Capture_face_vid(self):
        ret, frame = self.video_capture.read()
        rgb_frame = frame[:, :, ::-1]
        rgb_frame = frame[:, :, ::-1]
        faces = self.dect(rgb_frame)
        face_num=len(faces)
        face_locations = fr.face_locations(rgb_frame)
        face_encodings = fr.face_encodings(rgb_frame, face_locations)
        return faces,face_num,face_locations,face_encodings,frame