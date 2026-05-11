function voice(){
let r=new webkitSpeechRecognition();
r.start();

r.onresult=async e=>{
let text=e.results[0][0].transcript;

let res=await fetch("http://127.0.0.1:5000/chat",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({message:text})
});

let d=await res.json();
voiceOut.innerText=d.reply;

let s=new SpeechSynthesisUtterance(d.reply);
speechSynthesis.speak(s);
};
}