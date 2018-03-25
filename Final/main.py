import os

#Regular checkup for new video entries
os.system("ls User_videos/> list.txt")
print('\nVideo entries updated')
print('---------------------')
for line in open('list.txt'):
	line = line.rstrip('\n') 
	print line
print('=====================')


#for automating the process
#for line in open('list.txt'):
#	line = line.rstrip('\n') 
#	print line
#	video_name=line

print('\n\n --------AUTO ATTENDANCE SYSTEM-------\n1.Train face of a new student')
print('2.Take attendance of students')
choice = int(raw_input())

if choice == 1:
	print '1 is choosen'
	os.system("python dataSetGenerator.py")
	os.system("python trainer.py")
	print('\nTraining is completed\n')
	os.system("python main.py")
elif choice==2:
	print('\n--------CHECKING FOR LIVE DETECTION-------\n\n')
	print('Enter student registration number')
	video_name = raw_input()
	os.system("python detect_blinks.py --shape-predictor shape_predictor_68_face_landmarks.dat \
		--video User_videos/"+video_name+".mp4")













