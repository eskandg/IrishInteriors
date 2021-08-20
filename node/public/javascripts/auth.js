let signedOut = document.getElementById("signed-out");
let signedIn = document.getElementById("signed-in");
let profileName = document.getElementById("profile");

// function to change user if already logged in
function changeProfile() { 
    changeContent(document.getElementById("contentID-login"));
}

// function to log user out when clicked in navbar
function logout() { 
    localStorage.clear(); // clear credentials from storage
    profileName.innerHTML = "";
    signedIn.style.display = "none";
    signedOut.style.display = "";
    changeContent(index);
}

function checkLogin(alert, data, user) {
    window.token = data['token']
    errors = data['non_field_errors']; // if we login correctly this should be undefined

    if (window.token != null && errors == undefined) {
        alert.style.display = "none";
        signedOut.style.display = "none";
        signedIn.style.display = "";

        // helps keep us logged in after refresh
        localStorage.profile = user;
        localStorage.token = window.token;

        // display profile name
        let profileName = document.getElementById("profile");
        profileName.innerHTML = "Signed in as: " + user;

        changeContent(index);

    } else {
        alert.style.display = ""; // alert the user for entering wrong details
    }
}

// Shows name of logged in user in navbar
if (localStorage.token) {
    profileName.innerHTML = "Signed in as: " + localStorage.profile;
    signedOut.style.display = "none";
}
else {
    signedIn.style.display = "none";
}


// event listener for Registration form
let registerform = document.getElementById("register-form");
    registerform.addEventListener("submit", (event) => {
    event.preventDefault();

    let user = document.getElementById("id_username1").value;
    let pass = document.getElementById("id_password1").value;
    let confirm_pass = document.getElementById("id_password2").value;

    // console.log(user);
    // console.log(pass);
    // console.log(confirm_pass);

    fetch("http://127.0.0.1:8000/api-registration/?format=json", {
        method: 'POST',
        headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        },
        body: JSON.stringify({username: user, password1: pass, password2: confirm_pass})
    }).then(response => response.json()).then(function(registrationData) {
        console.log(registrationData) 
        
        let signupAlert = document.getElementById("signup-alert");
        signupAlert.style.display = "none" 
        if ("error" in registrationData) { 
            signupAlert.style.display = "";
            let errorMessage = document.getElementById("signup-error");
            errorMessage.innerHTML = "Error: " + registrationData["error"];
        } 
        else {
            // login if registered

            let user1 = registrationData['username'];
            let passw1 = registrationData['password1']; 
            let passw2 = registrationData['password2'];   
            
            fetch("http://127.0.0.1:8000/token/", {
                method:'POST',
                headers:{
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                },
                body: JSON.stringify( { username:user1, password:passw1 })
            }).then(response => response.json()).then(function(loginData){
                let signupAlert = document.getElementById("signup-alert");
                checkLogin(signupAlert, loginData, user1);
            })

        }


    });
    }, true);


// event listener for Login Form
let loginform = document.getElementById("login-form")
    loginform.addEventListener("submit", (event)=> {
    event.preventDefault();
    // get data from form
    let user = document.getElementById("id_username").value 
    let pass = document.getElementById("id_password").value

    // build POST request to /token/ 
    fetch("http://127.0.0.1:8000/token/", { 
        method:'POST',
        headers:{
        'Accept': 'application/json',
        'Content-Type': 'application/json', 
        },
        body: JSON.stringify( { username:user, password:pass })
    }).then(response => response.json()).then(function(data){
        let loginAlert = document.getElementById("login-alert");
        checkLogin(loginAlert, data, user)
    }) 
    }, true)

