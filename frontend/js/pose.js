let count=0,stage="up";

function angle(a,b,c){
let r=Math.atan2(c.y-b.y,c.x-b.x)-Math.atan2(a.y-b.y,a.x-b.x);
let ang=Math.abs(r*180/Math.PI);
if(ang>180) ang=360-ang;
return ang;
}

function startPose(){
let video=document.getElementById("video");
navigator.mediaDevices.getUserMedia({video:true})
.then(s=>video.srcObject=s);

const pose=new Pose({
locateFile:f=>`https://cdn.jsdelivr.net/npm/@mediapipe/pose/${f}`
});

pose.onResults(r=>{
if(!r.poseLandmarks) return;
let h=r.poseLandmarks[24],k=r.poseLandmarks[26],a=r.poseLandmarks[28];
let ang=angle(h,k,a);

if(ang<90) stage="down";
if(ang>160 && stage==="down"){
stage="up";count++;
document.getElementById("rep").innerText=count;
}
});

new Camera(video,{
onFrame:async()=>await pose.send({image:video}),
width:640,height:480}).start();
}