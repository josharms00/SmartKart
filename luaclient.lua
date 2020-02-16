local luaclient = {}

luaclient.connect = 
function()
    local socket = require("socket")

    local socket = require("socket")
    local hostname = "LAPTOP-47C8K4N3"
    local port = 120

    luaclient.client = socket.connect(hostname, port)
end

luaclient.send =
function(data)
    luaclient.client:send(data)
end

return luaclient
