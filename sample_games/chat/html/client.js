txtInput = document.getElementById("txtInput")
txtOutput = document.getElementById("txtOutput")
btnSend = document.getElementById("btnSend")

btnSend.onclick = ()=>{
    alert("sending")
}

ws = new WebSocket("ws://127.0.0.1/user/login")//"ws://127.0.0.1/waiting_list")

ws.send("hello")
console.log(ws)
