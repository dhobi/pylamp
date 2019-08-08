# used in jenkins: 
# pylamp.ps1 -isStart 1 -color '{"r":0, "g": 255, "b": 0}'
# pylamp.ps1 -isStart 0 -color '{"r":0, "g": 255, "b": 0}'

param(
$isStart = 1,
$color = '{"r":0, "g": 255, "b": 0}'
)

$WS = New-Object System.Net.WebSockets.ClientWebSocket                                                
$CT = New-Object System.Threading.CancellationToken   
	
function connect {
	$Conn = $WS.ConnectAsync("wss://connect.websocket.in/pylamp?room_id=1", $CT)                                                  
	While (!$Conn.IsCompleted) { Start-Sleep -Milliseconds 100 }
}

function close {
}

function updateLamp {
    param( $Reply )

	$Array = @()
	$Reply.ToCharArray() | ForEach { $Array += [byte]$_ }          
	$Reply = New-Object System.ArraySegment[byte]  -ArgumentList @(,$Array)
		
	$task = $WS.SendAsync($Reply, [System.Net.WebSockets.WebSocketMessageType]::Text, [System.Boolean]::TrueString, $CT)
	do { Start-Sleep -Milliseconds 100 }
    until ($task.IsCompleted)
}

function startBuild {
	param( $startColor )
	updateLamp('{"message":"color","value":' + $startColor + '}')
	updateLamp('{"message":"period","value":{"period":0.5}}')
	updateLamp('{"message":"type","value":{"name":"pulsating"}}')
}

function endBuild {
	param( $endColor )
	updateLamp('{"message":"color","value":' + $endColor + '}')
	updateLamp('{"message":"type","value":{"name":"off"}}')
}

connect
if($isStart -eq 1)
{
startBuild($color)
} else {
endBuild($color)
}
close