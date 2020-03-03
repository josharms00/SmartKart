local filename = "data.txt"

file = io.open(filename, "a")

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

buttons = {
	NumberPad5 = "P1 A",
	S = "P1 A Down",
	A = "P1 A Left",
	D = "P1 A Right",
	W = "P1 A Up",
	NumberPad1 = "P1 B",
    NumberPad8 = "P1 C Down",
	NumberPad7 = "P1 C Left",
	NumberPad9 = "P1 C Right",
	NumberPadSlash = "P1 C Up",
	DownArrow = "P1 DPad D",
	LeftArrow = "P1 DPad L",
	RightArrow = "P1 DPad R",
	UpArrow = "P1 DPad U",
	NumberPad4 = "P1 L",
	NumberPad6 = "P1 R",
	NumberPadEnter = "P1 Start",
	NumberPad0 = "P1 Z"
}

function refresh_position ()
	kart.x = mainmemory.readfloat(kart.x_addr, true)
	kart.xv = mainmemory.readfloat(kart.xv_addr, true)
	kart.y = mainmemory.readfloat(kart.y_addr, true)
	kart.yv = mainmemory.readfloat(kart.yv_addr, true)
	kart.z = mainmemory.readfloat(kart.z_addr, true)
	kart.zv = mainmemory.readfloat(kart.zv_addr, true)
end

while 1 do
    refresh_position()

    output = input.get()

    if output ~= nil then 
        file:write(kart.x .. "#" ..
                kart.xv .. "#" ..
                kart.y .. "#" ..
                kart.yv .. "#" ..
                kart.z .. "#" ..
                kart.zv .. "#") 

        for k, v in pairs(output) do
            if k == "WMouse L" || k == "Start" then
                break
            end
            file:write(buttons[k] .. "#")
        end
    end
    
    emu.frameadvance()
end