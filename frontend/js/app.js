const API="http://127.0.0.1:5000";

async function login(){
let r=await fetch(API+"/login",{method:"POST",
headers:{"Content-Type":"application/json"},
credentials:"include",
body:JSON.stringify({username:username.value,password:password.value})});
let d=await r.json();
if(d.msg==="ok") location="/dashboard";
}

async function register(){
await fetch(API+"/register",{method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({username:username.value,password:password.value})});
alert("done");
}

async function plan(){

    let weight = weight.value;
    let height = height.value;
    let goal = goal.value;

    let bmi = weight / (height * height);

    let w = await fetch(API+"/api/workout",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({goal:goal})
    });

    let workout = await w.json();

    let d = await fetch(API+"/api/diet",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({weight:weight,goal:goal})
    });

    let diet = await d.json();

    out.innerHTML = `
    BMI: ${bmi.toFixed(2)} <br>
    Workout: ${workout.plan} <br>
    Diet: ${diet.diet}
    `;
}


async function sendMessage(){
let msg = chatInput.value;

let r = await fetch(API+"/api/chat",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({message:msg})
});

let d = await r.json();

chatBox.innerHTML += `<p>You: ${msg}</p><p>AI: ${d.reply}</p>`;
}


async function addCalories(){
await fetch(API+"/api/add-calories",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({calories:cal.value})
});
alert("Saved");
}


function loadChart(){
let ctx=document.getElementById("chart");

new Chart(ctx,{
type:"line",
data:{
labels:["Mon","Tue","Wed","Thu","Fri"],
datasets:[{
label:"Weight",
data:[75,74,73,72,71]
}]
}
});
}

async function logout(){
await fetch(API+"/logout",{credentials:"include"});
location="/";
}