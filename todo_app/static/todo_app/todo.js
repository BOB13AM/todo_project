//Waiting for the DOM to Load 
document.addEventListener('DOMContentLoaded', function() {

    //by default load the home page content
    load_home();
    
    //onsubmiting the form fetch the create view and then reload the page to 
    document.querySelector('#todo-form').onsubmit = () =>{
        new_task = document.querySelector('#task').value
        // fetch the create view function 
        fetch('/create',{
            //send the request using the POST method 
            method:'POST',
            //send the data to the function in the body after stringify it 
            body: JSON.stringify({
            //send the data thru the task     
            task: new_task
        })
     })
     //loading the home content after receiving the promise to get the latest task entered
    .then(response => response.json())
    .then(result => {
        console.log(result);
        load_home();
      }); 
    }

    //load the home page for admin/normal users 
    function load_home(){
        //clear the todo-content field
        document.querySelector('#todo-content').innerHTML= ''
        //clear the admin content field
        document.querySelector('#admin-content').innerHTML= ''
        //hide the user page div 
        document.querySelector('#user-div').style.display = 'none'
        
        //fetch the content view 
         fetch('/content')
        //wait for the response 
        .then(response => response.json())
        //accessing the returned json format tasks one by one 
        .then(content => {
            content.forEach(element => {
                //if statment to check if the user is admin or normal user to display the content accordingly
                if(element.username){
                    //filling up the admin-content div with the data for admin users
                    document.querySelector('#admin-content').innerHTML += 
                    `
                        <div class="col marg_btm">
                        <button onclick="userpage(this.value)" class="card btn btn-outline-secondary box" value="${element.userid}">
                            <div class="card-body" style="">
                                <h5 class="card-title">${element.username}</h5>
                                <p class="card-text">User Email: ${element.email}</p>
                            </div>
                        </button>
                        </div>
                    `
                }
                else{
                    //create the ul element
                    const li = document.createElement('li')
                    //fill up the li class
                    li.setAttribute("class", "todo_li")
                    //filling up an html var to add it to the li innerHTML
                    let html=`
                        <div class="card" style="width:100%;">
                        <div class="card-body">
                        <div class="card-title"><h5 style="float:right;"><small>${element.timestamp}</small></h5><h5 class="card-content" data-content="${element.body}">${element.body}</h5></div>
                        <button class="btn btn-primary translate-btn" style="margin-top:1%;" value="${element.id}">Translate</a>
                        </div>
                        </div>
                    `
                    //adding the html to the li
                    li.innerHTML=html;
                    //appending the li to ul as a child 
                    document.querySelector('#todo-content').appendChild(li);
                    
                    //get all the buttons with translate class 
                    let all = document.querySelectorAll(".translate-btn")
                    //get all the content of the cards to translate 
                    let title = document.querySelectorAll(".card-content")
                   
                    //loop over all the button to detect which one is pressed 
                        for(let i=0; i<all.length; i++){               
                         all[i].addEventListener('click', function(){
                               //change the attributes of the button  
                                all[i].innerHTML='Done'
                                all[i].disabled = true
                                all[i].setAttribute("class", "btn btn-secondary")
                                let target_content = title[i].dataset.content
                                //fetch the content view 
                                fetch(`/translation/${target_content}`)
                                //wait for the response 
                                .then(response => response.json())
                                //accessing the returned json format tasks one by one
                                .then(new_content =>{
                                    //get the content of the exact element and translate it
                                title[i].innerHTML = `${new_content}`
                                }) 

                                //ge the id value of the task and then send it to the js translated_update function
                                let id = all[i].value
                                translated_update(id);
                        });        
                     }
                     
                }
                
            })

      });
    }    
    
});


//This function is to load the user history for the admin
function userpage(id){
    //clear the todo-content field
    document.querySelector('#todo-content').innerHTML= ''
    //clear the admin content field
    document.querySelector('#admin-content').innerHTML= ''
    //show the user page div 
    document.querySelector('#user-div').style.display = 'block'
    //default title incase no data found
    document.querySelector('#user-name').innerHTML = 'No History Yet'

    //fetching from the view
    fetch(`/userpage/${id}`)
    //get the promise from the 
    .then(response=>response.json())
    //accessing the returned json format user tasks one by one 
    .then(all_content => {
        all_content.forEach(element => {
            //checking if i received a user (data) to change the title accordingly 
            if(element.user !== undefined){
                document.querySelector('#user-name').innerHTML = `${element.user} History`
            } 
            //checking if the user translate this task 
            if(element.translated){
            //fill up the user-content field
            document.querySelector('#user-content').innerHTML +=
            `
            <li class="todo_li">
                <div class="card">
                <div class="card-header" style="background-color: lightgreen;">
                    <b>User translated this task at least once</b>
                </div>
                <div class="card-body">
                <h5 class="card-title">${element.body} <small style="float:right;">${element.timestamp}</small></h5>
                </div>
                </div>
             </li>
            `
            }
            else{
            //fill up the user-content field
            document.querySelector('#user-content').innerHTML +=
            `
            <li class="todo_li">
                <div class="card">
                <div class="card-body">
                <h5 class="card-title">${element.body} <small style="float:right;">${element.timestamp}</small></h5>
                </div>
                </div>
             </li>
            `
            }
        })
    });
    
}

//This function is to update the translated field in the task model using the PUT method 
function translated_update(id){
    //fetching fromthe view 
    fetch(`/update/${id}`,{
        //send the request using the POST method 
        method:'PUT',
        //send the data to the function in the body after stringify it 
        body: JSON.stringify({
        //send the data thru the task     
        translate: true
     })
 })
}