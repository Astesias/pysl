import cv2
import sys
  
def videocapture(n):
    cap=cv2.VideoCapture(n)     
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
    fps = cap.get(cv2.CAP_PROP_FPS) 
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))    

    #writer = cv2.VideoWriter("video_result.mp4", fourcc, fps, (width, height))
    
    while cap.isOpened():
        ret, frame = cap.read() 
        cv2.imshow('teswell', frame)
        key = cv2.waitKey(24)
        
        #writer.write(frame)  
   
        if key == ord('q'):
            break
    cap.release()        
    cv2.destroyAllWindows() 
  
if __name__ == '__main__' :
    if len(sys.argv)==1:
      videocapture(1)
    else:
      videocapture(sys.argv[1])
      
def SysInput(func,default):
    if len(sys.argv)==1:
        func(default)
    else:
        func(*sys.argv[1:])