## loading the saved model ##

model=load_model(r"path for the saved model with good accuracy.")

model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

model.summary()

## face- mask detection ##

face_classifier=cv2.CascadeClassifier(r" path for haar-cascade-classifier")
labels_dict={0:'NO MASK',1:'MASK'}
color_dict={0:(0,0,255),1:(0,255,0)}
number = 0

while(number < 5):
    source = cv2.VideoCapture(0)
    ret,img=source.read()
    #img = cv2.add(img,np.array([50.0]))
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=face_classifier.detectMultiScale(gray,1.5,5) 
    number +=(len(faces))
    label = 0
    for (x,y,w,h) in faces:

        face_img=gray[y:y+w,x:x+w]
        resized=cv2.resize(face_img,(100,100))
        normalized=resized/255.0
        reshaped=np.reshape(normalized,(1,100,100,1))
        result=model.predict(reshaped)
        print(result)
        label = np.argmax(result,axis=1)[0]
        cv2.rectangle(img,(x,y),(x+w,y+h),color_dict[label],2)
        cv2.rectangle(img,(x,y-40),(x+w,y),color_dict[label],-1)
        cv2.putText(img, labels_dict[label], (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
    cv2.imshow('photo',img)
    key=cv2.waitKey(2)
    if label:
        playsound(r"path for speech.mp3") # voice for wearing a face mask
    else:
        playsound(r"path for crazy.mp3") # voice for not wearing a face mask.

if number >= 5:
    #voice indicates that the room is full.
    playsound(r"path speech (2).mp3")

cv2.destroyAllWindows()
source.release()
