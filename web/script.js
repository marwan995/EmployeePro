const notif_btn = document.getElementsByClassName("notification")[0];
const s_btn = document.getElementsByClassName("notification")[1];

const performanceIdInput = document.getElementById("performanceId");
const passwordInput = document.getElementById("password");
const Overlay =document.getElementsByClassName('overlay_message_box')[0]
const error_list = Overlay.getElementsByTagName('ul')[0];
const ok_btn = document.getElementsByClassName('ok-button')[0]
const loadingOverlay = document.getElementById('loadingOverlay');

document.getElementsByTagName('form')[0].addEventListener('submit',  e => {
    
    e.preventDefault()
    
    if (passwordInput.value === "123456"||passwordInput.value ==="ngv123") {
        showLoading()
        document.cookie=passwordInput.value
        eel.login(performanceIdInput.value)().then(async e=>{
            if(passwordInput.value ==="ngv123")
              flag=  await eel.setFlag()()
            
            eel.getErrorLog()().then(async error_log=>{
                hideLoading()
               
                Overlay.style.display ='flex'
                error_log.forEach(err=>{
                    let li = document.createElement('li')
                    li.innerText=err
                    error_list.appendChild(li)
                })
                ok_btn.addEventListener('click',()=>{
                    window.location.href = 'home.html';
                })
            })
          
          
        })
       
    } else {
        // Password is incorrect, clear inputs and show error message
        performanceIdInput.value = "";
        alert("Wrong Password")
        passwordInput.value = "";
    }
})
function showLoading() {
    loadingOverlay.style.display = 'flex';

    const loadingText = document.getElementById('loadingText');
    const originalText = loadingText.textContent;
    loadingText.textContent = ''; // Clear the original text

    const characters = originalText.split('');
    let charIndex = 0;

    const interval = setInterval(() => {
        if (charIndex < characters.length) {
            loadingText.textContent += characters[charIndex];
            charIndex++;
        } else {
            clearInterval(interval);
        }
    }, 130);
}
function hideLoading(){
    loadingOverlay.style.display='none'
}
notif_btn.addEventListener('click',()=>{
    if (passwordInput.value === "ngv123") {
    window.location.href='alerts.html';
    }
    else {
        // Password is incorrect, clear inputs and show error message
        performanceIdInput.value = "";
        alert("Please enter your Password")
        passwordInput.value = "";
    }
})
s_btn.addEventListener('click',()=>{
    if (passwordInput.value === "ngv123") {
    window.location.href='solfa.html';
    }
    else {
        // Password is incorrect, clear inputs and show error message
        performanceIdInput.value = "";
        alert("Please enter your Password")
        passwordInput.value = "";
    }
})
window.addEventListener('load',async()=>{

    if(document.cookie){
        console.log(document.cookie)
        passwordInput.value=document.cookie
    }
    let alerts = [
        ['المؤهل الدراسي للعاملين', 'تاريخ الانتهاء'],
         ['بطاقات شخصية', 'تاريخ الانتهاء']
        , ['المؤهل الدراسي للعاملين', 'قياس مستوي المهارة']
        , ['اقرار ذمة مالية', 'تاريخ التعيين']
    ]
    let alertcount=0
    for(let i=0; i<alerts.length;i++)
    {
        let sheet_name = alerts[i][0]
        let column_name =alerts[i][1]
        let x=await eel.all_alerts(sheet_name,column_name)()
           
            alertcount+=x.length
    }
    
    document.getElementsByClassName('badge')[0].textContent=alertcount
  
})
