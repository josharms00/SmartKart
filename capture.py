import autopy

def take_screenshot():
	capture = autopy.bitmap.capture_screen()

	capture.save("cap0.png")


take_screenshot()