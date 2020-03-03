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
	"P1 C Down",
	"P1 C Left",
	"P1 C Right",
	"P1 C Up",
	"P1 DPad D",
	"P1 DPad L",
	"P1 DPad R",
	"P1 DPad U",
	"P1 L",
	"P1 R",
	"P1 Start",
	"P1 Z"
}

kart = {}
kart.x_addr = 0x0F69A4
kart.xv_addr = 0x0F69C4
kart.y_addr = 0xF69A8
kart.yv_addr = 0x0F69C8
kart.z_addr = 0x0F69AC
kart.zv_addr = 0x0F69CC
dist_addr = 0x16328A
kart.sin = 0xF6B04
kart.cos = 0xF6B0C

client.connect()

function refresh_position ()
	kart.x = mainmemory.readfloat(kart.x_addr, true)
	kart.xv = mainmemory.readfloat(kart.xv_addr, true)
	kart.y = mainmemory.readfloat(kart.y_addr, true)
	kart.yv = mainmemory.readfloat(kart.yv_addr, true)
	kart.z = mainmemory.readfloat(kart.z_addr, true)
	kart.zv = mainmemory.readfloat(kart.zv_addr, true)
end

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

function create_packet ()

	packet = tostring(kart.x) .. " " ..
	tostring(kart.xv) .. " " ..
	tostring(kart.y) .. " " ..
	tostring(kart.yv) .. " " ..
	tostring(kart.z) .. " " ..
	tostring(kart.zv) .. "\n"

	return packet

end

while 1 do
	refresh_position()

	packet = create_packet()

	client.send(packet)

	button_choice = str_split(client.receive(), "%s")

	for i = 1, #button_choice do
		inputs[buttons[tonumber(button_choice[i])]] = true
	end

	joypad.set(inputs)

	emu.frameadvance()
end
