let canv = document.querySelector('#canvas');
let context = canv.getContext('2d');
// $('input').click();
let color = $('input').val();
let canvasWidth = canv.width;
let canvasHeight = canv.height;
let canvasData = context.getImageData(0, 0, canvasWidth, canvasHeight);

function drawPixel (x, y, r, g, b, a) {
    let index = (x + y * canvasWidth) * 4;

    canvasData.data[index + 0] = r;
    canvasData.data[index + 1] = g;
    canvasData.data[index + 2] = b;
    canvasData.data[index + 3] = a;
}

function updateCanvas() {
    context.putImageData(canvasData, 0, 0);
}



let socket = io.connect("http://10.0.0.39:5000/draw");
socket.on('connect', _ => {
        socket.emit('');
});

$('input').on('change', _ =>{
    color = $('input').val();
});

let isMouseDown = false;

$('#canvas').on('mousedown', event =>{
    isMouseDown = true;
    socket.emit('drawTrigger', {'x':event.originalEvent.clientX,'y':event.originalEvent.clientY,'x1':event.originalEvent.clientX, 'y1':event.originalEvent.clientY, 'color':color});
});
$('#canvas').on('mouseup', _ =>{
    isMouseDown = false;
});

$('#canvas').on('mousemove', event =>{
    if(isMouseDown){
        //console.log(event);
        socket.emit('drawTrigger', {'x':event.originalEvent.clientX,'y':event.originalEvent.clientY, 'x1':event.originalEvent.clientX+event.originalEvent.movementX, 'y1':event.originalEvent.clientY+event.originalEvent.movementY, 'color':color});
    }

});

$('#saveBtn').on('clicked', _ =>{
    socket.emit('saveImage', {'img':canv.toDataURL("image/png")})
});


socket.on('drawAction', coords => {
    //drawPixel(coords['x'], coords['y'], 0, 0, 0, 255);
    //updateCanvas();

    context.beginPath();

    context.moveTo(coords['x'],coords['y']);
    context.lineTo(coords['x1'],coords['y1']);
    context.strokeStyle = coords['color'];
    context.stroke();

});

socket.on('debug', _ => {alert('!')})