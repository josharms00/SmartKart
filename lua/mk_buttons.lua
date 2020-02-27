local client = require("luaclient")
output = {}
inputs = {}

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

while 1 do
	output = input.get()

	client.send(buttons[1])

	data = client.receive()

	print(data)

	-- if data ~= nil then
	-- 	for i=1,

	emu.frameadvance()
end
