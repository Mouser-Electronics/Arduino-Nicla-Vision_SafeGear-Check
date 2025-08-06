import sensor, image, time, ml, math, uos, gc, pyb
from machine import Pin, I2C
from vl53l1x import VL53L1X
from pyb import UART
CHECK_DURATION_S = 5
RESULT_DISPLAY_S = 5
COOLDOWN_S = 2
NAME_INPUT_TIMEOUT_S = 15
LOG_FILE = "system_log.txt"
GREEN_LIGHT_PIN = 'PG12'
YELLOW_LIGHT_PIN = 'D3'
RED_LIGHT_PIN = 'D2'
BUTTON_HELMET_PIN = 'PE13'
BUTTON_VEST_PIN = 'PE14'
BUTTON_MASK_PIN = 'PE11'
BUTTON_GLOVES_PIN = 'PF3'
PROXIMITY_THRESHOLD_MM = 1000
START_BYTE = 0x7E
VERSION_BYTE = 0xFF
COMMAND_LENGTH = 0x06
END_BYTE = 0xEF
ACKNOWLEDGE = 0x00
uart = UART(9, 9600)
uart.init(9600, bits=8, parity=None, stop=1, timeout_char=1000)
MIN_CONFIDENCE = 0.6
rtc = pyb.RTC()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((240, 240))
sensor.skip_frames(time=2000)
net = None
labels = None
try:
	net = ml.Model("trained.tflite")
except Exception as e:
	raise Exception('Failed to load "trained.tflite": ' + str(e))
try:
	labels = [line.rstrip('\n') for line in open("labels.txt")]
except Exception as e:
	raise Exception('Failed to load "labels.txt": ' + str(e))
REQUIRED_GEAR = ["HELMET", "VEST", "MASK"]
green_led = Pin("PG12", Pin.OUT)
yellow_led = Pin("D3", Pin.OUT)
red_led = Pin("D2", Pin.OUT)
green_led.low()
yellow_led.low()
red_led.low()
button_helmet = Pin(BUTTON_HELMET_PIN, Pin.IN)
button_vest = Pin(BUTTON_VEST_PIN, Pin.IN)
button_mask = Pin(BUTTON_MASK_PIN, Pin.IN)
button_gloves = Pin(BUTTON_GLOVES_PIN, Pin.IN)
last_gear_list_sent = ""
print("INFO: Nicla Vision ready. Final list-sending mode.")
tof = None
try:
	tof_i2c = I2C(2)
	tof = VL53L1X(tof_i2c)
	print("INFO: Proximity sensor initialized.")
except Exception as e:
	print(f"ERROR: Proximity sensor not found. Error: {e}")
usb = pyb.USB_VCP()
def fomo_post_process(model, inputs, outputs):
	threshold_list = [(math.ceil(MIN_CONFIDENCE * 255), 255)]
	ob, oh, ow, oc = model.output_shape[0]; x_scale, y_scale = (inputs[0].roi[2] / ow), (inputs[0].roi[3] / oh); scale = min(x_scale, y_scale); x_offset = ((inputs[0].roi[2] - (ow * scale)) / 2) + inputs[0].roi[0]; y_offset = ((inputs[0].roi[3] - (ow * scale)) / 2) + inputs[0].roi[1]; l = [[] for i in range(oc)];
	for i in range(oc):
		img = image.Image(outputs[0][0, :, :, i] * 255); blobs = img.find_blobs(threshold_list, x_stride=1, y_stride=1, area_threshold=1, pixels_threshold=1);
		for b in blobs:
			rect = b.rect(); x, y, w, h = rect; score = (img.get_statistics(thresholds=threshold_list, roi=rect).l_mean() / 255.0); x = int((x * scale) + x_offset); y = int((y * scale) + y_offset); w = int(w * scale); h = int(h * scale); l[i].append((x, y, w, h, score))
	return l
def log_event(username, message):
	try:
		dt = rtc.datetime()
		timestamp = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(dt[0], dt[1], dt[2], dt[4], dt[5], dt[6])
		log_entry = f"{timestamp},{username},{message}\n"
		with open(LOG_FILE, "a") as f:
			f.write(log_entry)
	except Exception as e:
		print(f"ERROR: Failed to write to log file: {e}")
def send_command(command, parameter_high, parameter_low):
		checksum = -(VERSION_BYTE + COMMAND_LENGTH + command + ACKNOWLEDGE + parameter_high + parameter_low)
		checksum_high = checksum >> 8
		checksum_low = checksum & 0xFF
		command_packet = bytearray([
			START_BYTE,
			VERSION_BYTE,
			COMMAND_LENGTH,
			command,
			ACKNOWLEDGE,
			parameter_high,
			parameter_low,
			checksum_high,
			checksum_low,
			END_BYTE
			])
		uart.write(command_packet)
		print("Sent command: " + " ".join(hex(b) for b in command_packet))
def run_ppe_check(username):
	print(f"INFO: Starting PPE check for '{username}'.")
	found_gear_status = {gear.upper(): False for gear in REQUIRED_GEAR}
	all_gear_found = False
	start_time_ms = time.ticks_ms()
	end_time_ms = time.ticks_add(start_time_ms, CHECK_DURATION_S * 1000)
	yellow_led.high()
	time.sleep_ms(2000)
	yellow_led.low()
	while time.ticks_diff(end_time_ms, time.ticks_ms()) > 0:
		img = sensor.snapshot()
		for i, detection_list in enumerate(net.predict([img], callback=fomo_post_process)):
			if i >= len(labels) or len(detection_list) == 0: continue
			detected_label = labels[i].upper()
			if detected_label in found_gear_status:
				found_gear_status[detected_label] = True
		if all(found_gear_status.values()):
			all_gear_found = True
			break
	if __name__ == '__main__':
		print("DFPlayer Mini Test Script")
		time.sleep_ms(1000)
		print("Setting volume")
		send_command(0x06, 0x00, 30)
		time.sleep_ms(500)
	if all_gear_found:
		final_result_message = "All clear. Please proceed to the site."
		green_led.high()
		send_command(0x03, 0x00, 0x02)
		print(f"RESULT:{final_result_message}")
		time.sleep_ms(500)
	else:
		missing_items = [gear for gear, found in found_gear_status.items() if not found]
		if not missing_items:
			 final_result_message = "No PPE detected. Please wear all required safety gear."
		else:
			 final_result_message = "MISSING GEAR: {}. Please wear all required safety gear before entering the site.".format(", ".join(missing_items))
		red_led.high()
		send_command(0x03, 0x00, 0x01)
		print(f"RESULT:{final_result_message}")
		time.sleep_ms(500)
	log_event(username, final_result_message)
	time.sleep_ms(RESULT_DISPLAY_S * 1000)
	green_led.low()
	red_led.low()
	print("INFO: Check complete. System resetting.")
	time.sleep_ms(COOLDOWN_S * 1000)
print("INFO: Nicla Vision ready. Waiting for person ")
while(True):
	is_helmet_pressed = (button_helmet.value() == 1)
	is_vest_pressed = (button_vest.value() == 1)
	is_mask_pressed = (button_mask.value() == 1)
	is_gloves_pressed = (button_gloves.value() == 1)
	required_items = []
	if is_helmet_pressed:
		required_items.append("Helmet")
	if is_vest_pressed:
		required_items.append("Vest")
	if is_mask_pressed:
		required_items.append("Mask")
	if is_gloves_pressed:
		required_items.append("Gloves")
	current_gear_list = ",".join(required_items)
	if current_gear_list != last_gear_list_sent:
		print(f"GEAR_LIST:{current_gear_list}")
		last_gear_list_sent = current_gear_list
	if tof:
		try:
			distance = tof.read()
			if 0 < distance < PROXIMITY_THRESHOLD_MM:
				print(f"INFO: Proximity trigger! Object detected at {distance}mm.")
				run_ppe_check('username')
		except Exception as e:
			pass
	time.sleep_ms(100)