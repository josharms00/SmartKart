local client = require("luaclient")
output = {}
inputs = {}

client.connect()

while 1 do
	output = input.get()
 
	if output["W"] == true then
		inputs["P1 A"] = true
		joypad.set(inputs)
	end

	client.send('A')

	emu.frameadvance()
end
