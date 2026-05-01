import speech_recognition as speech

def stt():
	recognizer = speech.Recognizer()

	try:
		with speech.Microphone() as mic:

			recognizer.adjust_for_ambient_noise(mic, duration=0.8)
			print("Listening...")			
			voice = recognizer.listen(mic)			
			inputText = recognizer.recognize_google(voice)
			return inputText
		#	print("You Said : "+inputText)
						
	except speech.UnknownValueError:
		error = "Not regognized, try again..."
		return error
		