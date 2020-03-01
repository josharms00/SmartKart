local client = require("luaclient")
output = {}
inputs = {}
state = {}
button_choice = {}

buttons = {
	"P1 A",
	"P1 A Down",
	"P1 A Left",
	"P1 A Right",
	"P1 A Up",
	"P1 B",
	"C Down",
	"C Left",
	"C Right",
	"C Up",
	"DPad D",
	"DPad L",
	"DPad R",
	"DPad U",
	"L",
	"R",
	"Start",
	"Z"
}

client.connect()

function str_split (istr, del)
	if del == nil then
			del = "%s"
	end
	local t={}
	for str in string.gmatch(istr, "([^"..del.."]+)") do
		if str ~= "\n" then
			table.insert(t, str)
		end
	end
	return t
end

while 1 do
	output = input.get()

	client.send("P1 A")

	button_choice = str_split(client.receive(), "%s")

	for i = 1, #button_choice do
		print(buttons[tonumber(button_choice[i])])
	end

	-- for button, val in button_choice do:
	-- 	joypad.set(buttons[button_choice])

	-- if data ~= nil then
	-- 	for i=1,

	emu.frameadvance()
end
