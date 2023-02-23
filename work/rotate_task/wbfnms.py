import cv2
import os
import pdb
import sys
from pprint import pprint
import numpy as np
from math import atan,pi,cos,sin
from pysl import path2filename,cv2_imread,show_points,join_list,mvdir
from ensemble_boxes import weighted_boxes_fusion
from ensemble_boxes import *
import empty


global lendata
lendata=200

def f2(num):
    return eval('%.2f'%float(num))

def label2num(label):
    return int(label[-1])-1

def absdis(a,b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5

def inteval(st):
    try:
        return (eval(st))
    except :
        return st

def drawtri(img, pt1, pt2, pt3, pt4, color=(255,0,255), lineWidth=2):
    # cv2.line(img, pt1, pt2, color, lineWidth)
    cv2.line(img, pt2, (pt2[0],pt3[1]), (0,0,255), lineWidth)
    cv2.line(img, pt2, pt3, (0,0,255), lineWidth)
    cv2.line(img, (pt2[0],pt3[1]), pt3, color, lineWidth)                    
                    

def xyhwa24p(box):
    x,y,h,w,a=box
    # print(box)
    k=((h/2)**2+(w/2)**2)**0.5
    p3=[x+k*cos(a),y+k*sin(a)]
    p1=[x-k*cos(a),y-k*sin(a)]
    p4=[x+k*sin(a),y+k*cos(a)]
    p2=[x-k*sin(a),y-k*cos(a)]
    # print(box,p1+p2+p3+p4,'\n')
    return p1+p2+p3+p4

def get_box_o(anno_path):
    
    box=[[] for i in range(lendata)]
    for i in range(1,lendata+1):
        try:
            txt_path=anno_path+'{:0>4}.txt'.format(i)
            with open(txt_path) as fp:
                txt=fp.read()
                txt_list=txt.split('\n')
                for n,line in enumerate(txt_list[1:]):
                    if line:
                        
                        line=line.split(' ')
                        line=list(map(inteval,line))
                        line[8]=int(line[8][-1])-1
                        
                        box[i-1].append(     line           )
        except :
            pass
    # pdb.set_trace()
    return box   

def fourpoint2two(path):
    boxes4=get_box_o(path)
    boxes2=[[] for i in range(lendata)]
    angles=[[] for i in range(lendata)]
    # pdb.set_trace()
    for n,box in enumerate(boxes4):
        if box:
            for bo in box:
                a,b,c,d,e,f,g,h=bo[0],bo[1],bo[2],bo[3],bo[4],bo[5],bo[6],bo[7]
                po1=(a,b)
                po2=(c,d)
                po3=(e,f)
                po4=(g,h)
                
                # if a>
                
                # try:
                #     angle=180-180*atan((f-d)/(e-c))/pi
                # except:
                #     angle=0
                # if angle>180:
                #     angle-=180

                    
                # print(angle)
                    
                h=absdis(po1,po3)
                w=absdis(po2,po4)
                if h<w:
                    h,w=w,h
     
                center=((po1[0]+po3[0])/2,(po1[1]+po3[1])/2)
                
                # lt=(center[0]-h/2,center[1]-w/2)
                # rb=(center[0]+h/2,center[1]+w/2)
                
      
                minx,miny=min(a,c,e,g),min(b,d,f,h)
                maxx,maxy=max(a,c,e,g),max(b,d,f,h)
                
                # show_points((bo[0],bo[1]),(bo[2],bo[3]),(bo[4],bo[5]),(bo[6],bo[7]) ,resize=(1024,1024))
                
                boxes2[n].append( list(map(f2,[ minx,miny,maxx,maxy])) +[bo[-2],bo[-1] ]   )
    
    
    
    return boxes2
  
def enpointed(po1,po2,po3,po4):
    a,b,c,d,e,f,g,h=po1[0],po1[1],po2[0],po2[1],po3[0],po3[1],po4[0],po4[1]
    po1=(a,b)
    po2=(c,d)
    po3=(e,f)
    po4=(g,h)
    
    try:
        angle=180-180*atan((f-d)/(e-c))/pi
    except:
        angle=0
    if angle>180:
        angle-=180
    center=((po1[0]+po3[0])/2,(po1[1]+po3[1])/2)
    h=absdis(po1,po2)/2
    w=absdis(po2,po3)/2
    
    
    p1=(center[0]-h,center[1]-w)
    p2=(center[0]+h,center[1]+w)
    
    return p1,p2,angle

def depointed(p1,p2,angles):
    h=-p1[0]+p1[0]
    w=p2[1]-p1[1]
    center=(p1[0]+p1[0]/2,p1[1]+p1[1]/2)
    
def softnms_rotate_cpu(boxes, scores, iou_threshold, final_threshold=0.001):
    """
    :param boxes: format [x_c, y_c, w, h, theta(degrees)]
    :param scores: scores of boxes
    :param iou_threshold: iou threshold (usually 0.7 or 0.3)
    :param final_threshold: usually 0.001, if weighted score less than this value, discard the box

    :return: the remaining INDEX of boxes

    Note that this function changes 
    """

    EPSILON = 1e-5      # a very small number
    pos = 0             # a position index

    N = boxes.shape[0]  # number of input bounding boxes
    
    for i in range(N):

        maxscore = scores[i]
        maxpos   = i

        tbox   = boxes[i,:]    
        tscore = scores[i]

        pos = i + 1

        # get bounding box with maximum score
        while pos < N:
            if maxscore < scores[pos]:
                maxscore = scores[pos]
                maxpos = pos
            pos = pos + 1

        # Add max score bounding box as a detection result
        boxes[i,:] = boxes[maxpos,:]
        scores[i]  = scores[maxpos]
        # swap ith box with position of max box
        boxes[maxpos,:] = tbox
        scores[maxpos]  = tscore

        tbox   = boxes[i,:]
        tscore = scores[i]
        tarea  = tbox[2] * tbox[3]

        pos = i + 1

        # NMS iterations, note that N changes if detection boxes fall below final_threshold
        while pos < N:
            box   = boxes[pos, :]
            score = scores[pos]
            area  = box[2] * box[3]
            try:
                int_pts = cv2.rotatedRectangleIntersection(((tbox[0], tbox[1]), (tbox[2], tbox[3]), tbox[4]), ((box[0], box[1]), (box[2], box[3]), box[4]))[1]
                if int_pts is not None:
                    order_pts = cv2.convexHull(int_pts, returnPoints=True)
                    int_area  = cv2.contourArea(order_pts)
                    inter     = int_area * 1.0 / (tarea + area - int_area + EPSILON)  # compute IoU
                else:
                    inter = 0
            except:
                """
                  cv2.error: /io/opencv/modules/imgproc/src/intersection.cpp:247:
                  error: (-215) intersection.size() <= 8 in function rotatedRectangleIntersection
                """
                inter = 0.9999

            # Soft NMS, weight computation.
            if inter > iou_threshold:
                weight = 1 - inter
            else:
                weight = 1
            scores[pos] = weight * scores[pos]

            # if box score fall below final_threshold, discard it by swapping with last box
            # also, update N
            if scores[pos] < final_threshold:
                boxes[pos, :] = boxes[N-1, :]
                scores[pos]   = scores[N-1]
                N = N - 1
                pos = pos - 1 

            pos = pos + 1

    keep = [i for i in range(N)]
    return np.array(keep, np.int64)  
    
    
# path=r'D:\Desktop\.py\dataset\unknow\boats\train_data/' ##################
# anno_path=r'D:\Desktop\.py\work/'+'result/'           ## txt 8
anno_path=r'D:\Desktop\.py\work/'+'results/result_100ep/'      #pkl 4
jpeg_path=r'D:\360极速浏览器下载\验证集\验证集/'+'JPEGImages/'
# output_xml_dir=path+'new_Annotations/'

txt_names=os.listdir(anno_path)
txt_paths=[anno_path+_ for _ in txt_names]
jpg_paths=[jpeg_path+_.strip('txt')+'jpg' for _ in txt_names]
save_dir='nmsresult/'

boxlen=len(txt_paths)
boxes=fourpoint2two(anno_path)

def get_box(boxes):
    
    boxlen=len(boxes)
    label_list=[[] for i in range(boxlen)]
    score_list=[[] for i in range(boxlen)]
    box_list=[[] for i in range(boxlen)]
    
    for n,box in enumerate(boxes):
        if box:
            for index,bo in enumerate(box):
                box_list[n].append(   list(map(lambda x:x/1024, bo[:4])))
                label_list[n].append(index)
                score_list[n].append(bo[-1])
    # for N,txt_path in enumerate(txt_paths[:]):
    #     with open(txt_path) as fp:
    #         txt=fp.read()
    #         txt_list=txt.split('\n')
    #         for n,line in enumerate(txt_list[1:]):
    #             if line:
    #                 # pdb.set_trace()
    #                 box_list[N].append([eval(i) for i in (line.split(' '))[:-2]])
    #                 score_list[N].append(  eval(  (line.split(' '))[-1] ) )
    #                 label_list[N].append( label2num(((line.split(' '))[-2:-1][0]) ))

    # print(len(box_list),len(score_list),len(label_list) ,'\n\n' )
    return box_list,score_list,label_list,None 

def get_box_noempty(boxes):
    
    boxlen=len(boxes)
    # label_list=[[] for i in range(boxlen)]
    # score_list=[[] for i in range(boxlen)]
    # box_list=[[] for i in range(boxlen)]
    box_list=[]
    score_list=[]
    label_list=[]
    record_list=[0 for i in range(boxlen)]
    n=0
    m=0
    for box in boxes:
        if box:
            record_list[m]=1
            box_list.append([])
            score_list.append([])
            label_list.append([])
            for index,bo in enumerate(box):
                box_list[n].append(        list(map(lambda x:x/1024, bo[:4]))       )
                label_list[n].append(bo[-2])
                # label_list[n].append(index)
                score_list[n].append(bo[-1])
        if box:
            n+=1
        m+=1
    print(len(box_list),len(score_list),len(label_list) ,'\n\n' )
    return box_list,score_list,label_list ,record_list


box_o=get_box_o(anno_path)
box_lists,score_lists,label_lists,record_list=get_box(boxes)

results=[]
# boxesnms, scores, labels=[],[],[]
for box_list,score_list in zip(box_lists,score_lists):
     if box_list:
    
        # boxesnm, score, label=weighted_boxes_fusion(        [box_list],   
        #                                                     [score_list],  
        #                                                     [label_list],
        #                                                     weights=None,
        #                                                     iou_thr=0.3,
        #                                                     skip_box_thr=0.0,
        #                                                     conf_type='max',
        #                                                     allows_overflow=True
        #                                             )
        result=softnms_rotate_cpu(np.array(box_list), np.array(score_list), 0.3)
        
        
        
    #     boxesnms.append(boxesnm)
    #     scores.append(score)
    #     labels.append(label)
    # else:
    #     boxesnms.append([])
    #     scores.append([])
    #     labels.append([])
        
    
for n,i in enumerate(boxesnms):
    if type(i)==type([]):
        pass
    else:
        boxesnms[n]*=1024.0
    
boxfinal=list(zip(boxesnms, scores, labels))




# pprint(box_list[:2])
# pprint(score_list[:2])
# pprint(label_list[:2])

# boxesnms, scores, labels=nms_method( box_list[:2], score_list[:2], label_list[:2], method=3, weights=None, iou_thr=0.3, sigma=0.05, thresh=0.0001)

print(str(len(boxesnms))+' results')

mp=0.36
boxfinally=[[] for i in range(lendata)]
for n,file in enumerate(boxfinal):
    if file:
        for m,p in enumerate(file[1]):
            if p>mp:
                # print(box_o[n][  int(file[2][m]) ][:8] , box_o[n][  int(file[2][m]) ][8] )
                boxfinally[n].append( box_o[n][  int(file[2][m]) ][:8] + [box_o[n][  int(file[2][m]) ][8]]  )
                
for n,file in enumerate(boxfinally):
    if file:
        pass
    else:
        if box_o[n]:
            p=0
            
            for m,i in enumerate(box_o[n]):
                if i[-1]>p:
                    p=i[-1]
                    M=m
            if p>0.1:
                boxfinally[n].append( box_o[n][  m ][:8] + [box_o[n][  m ][8]]  )
        
                
sumlen=0
for i in boxfinally:
    sumlen+=len(i)
print(sumlen,' results')


for n,rdata in enumerate(boxfinally):  
    if rdata:
        try:
            f.close()
        except :
            pass
        f=open(save_dir+'{:0>4}.txt'.format(n+1),'w')
        f.write('Team: 1000000\n')
        for r in rdata:
            r[-1]='S'+str(r[-1]+1)
            f.write(join_list(r,' ')+'\n')
f.close()

rem=os.listdir(save_dir)
for pa in rem:
    os.remove(save_dir+pa)
print('源文件清除')

empty.main()  
mvdir(save_dir,'NUDT/NUDT/',showdetail=0)