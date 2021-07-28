document.addEventListener('DOMContentLoaded',()=>{

     let msg=document.querySelector('#user_message');
     msg.addEventListener('keyup', Event =>{
         Event.preventDefault();
         if(Event.keyCode ==13){
             document.querySelector('#send_message').click();
         }
     })
})