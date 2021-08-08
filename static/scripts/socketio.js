
document.addEventListener('DOMContentLoaded', () => {
     
        var socket = io(); 
        const username = document.querySelector('#get-username').innerHTML;
        
        let room="c++";
        joinRoom("c++");
        
        //send message
         document.querySelector('#send_message').onclick = () => {
            socket.send({'msg': document.querySelector('#user_message').value,   'username':username,'room':room});
            document.querySelector('#user_message').value= '';

         } ;

        socket.on ('message',data => {
        if(data.msg !=''){

            
            // Display user's own message
            if(typeof (data.username ) !== 'undefined'){
                const p = document.createElement('p');
                const span_username = document.createElement('span');
                const span_timestamp = document.createElement('span');
                const br = document.createElement('br')

                if (data.username == username ) {
                    p.setAttribute("class", "my-msg");


                    // Username
                    span_username.setAttribute("class", "my-username"); 
                    span_username.innerText = data.username;

                    // Timestamp
                     span_timestamp.setAttribute("class", "timestamp");
                    span_timestamp.innerText = data.time_stamp;

                    // HTML to append
                    p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;

                    //Append
                    document.querySelector('#display-message-section').append(p);
            }
            
            // Display other users' messages
            else{
                
                p.setAttribute("class", "others-msg");

                // Username
               span_username.setAttribute("class", "other-username");
                span_username.innerText = data.username;
                
                // Timestamp
                span_timestamp,setAttribute("class","timestamp")
                span_timestamp.innerText = data.time_stamp;

                // HTML to append
                p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;

                //Append
                document.querySelector('#display-message-section').append(p);
            }
           }
            else{
                   printSysMsg(data.msg);
            }
        
        }
          
    
          scrollDownChatWindow() 
        });


        

         document.querySelectorAll('.select-room').forEach(p=>{
             p.onclick=() =>{
                 let newRoom=p.innerHTML;
                 if(newRoom==room){
                     
                     msg=`yor alredy in the ${room} room`;
                     printSysMsg(msg);
                 }
                 else{

                     leaveRoom(room);
                     joinRoom(newRoom);
                     room=newRoom;
                     p.setAttribute("class","current-room")
                 }

             };
         });

         //leaving the rom ---------
         function leaveRoom(room) {
             socket.emit('leave',{'username':username,'room' :room});

             document.querySelectorAll('.select-room').forEach(p => {
             p.style.color = "black";
            });
        }
         
         //joining the room ---------
         function joinRoom(room) {
             socket.emit('join',{'username':username,'room':room});
             document.querySelector('#display-message-section').innerHTML='';
              
             // Highlight selected room
            
             //Autofocus
              document.querySelector('#user_message').focus();

         }

         // LOGOUT from chat applicatio 
         document.querySelector("#logout-btn").onclick= () => { leaveRoom(room) } ;

         //create new room
         document.querySelector("#new-rooms").onclick = () => {
             document.querySelector('#get-rooms').innerHTML="{{ rooms.append('ghxz') }}";
         };

         //messege printing
         function printSysMsg(msg) {
             const p=document.createElement('p');
           
             p.innerHTML=msg;
             document.querySelector('#display-message-section').append(p);
             // Autofocus on text box
             document.querySelector("#user_message").focus();      
         }

         // Scroll chat window down
    function scrollDownChatWindow() {
        const chatWindow = document.querySelector("#display-message-section");
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

});
    