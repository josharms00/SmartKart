
output = {}
inputs = {}

while 1 do
	output = input.get()
 
	if output["W"] == true then
		inputs["P1 A"] = true
		joypad.set(inputs)
	end

	emu.frameadvance()
end
