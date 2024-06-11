
function post_succesful_visible_2(response){

  console.log(response.status)
  console.log(response.body)
  console.log(response.text)

  setTimeout(() => {
    document.getElementById("succesful_post").classList.add("hidden_div");
    document.getElementById("failed_post").classList.add("hidden_div");
  }, "50000");

  const status = ((response.status).toString()).substring(0, 1);
  let text= ""
  if (status ==="2") {
    document.getElementById("succesful_post").classList.remove("hidden_div")
    document.getElementById("succesful_post").classList.remove("red_text")
    document.getElementById("succesful_post").classList.add("green_text")
    document.getElementById("succesful_post").innerHTML="Succesful Login"
    // document.location.href = "https://apiportalfreelancer.lat/tableau/tableau_extension_api_html/?response="+text;

  } else {
    
    document.getElementById("succesful_post").classList.remove("hidden_div")
    document.getElementById("succesful_post").classList.remove("green_text")
    document.getElementById("succesful_post").classList.add("red_text")
    document.getElementById("succesful_post").innerHTML="Failed Login"

  }

}

function post_failed_visible(error){
  console.log(error.detail)
  document.getElementById("failed_post").classList.remove("hidden_div")

  
}

async function postLogIn() {

  document.getElementById("button_post_log_in").disabled = true;

  btn=document.querySelector(".submission_button_login");
  btn.classList.toggle("submission_button_login--loading");

  oFormObject = document.forms['form6'];

  email=oFormObject.elements["email"].value
  password=oFormObject.elements["password"].value

  const body = new FormData
  body.append("email", email)
  body.append("", "\\")
  body.append("password", password)
  body.append("", "\\")
  body.append("only_cookie", "si")


  await fetch("https://apiportalfreelancer.lat/auth/login_talent_firm", {
    body,
    headers: {
    Accept: "application/json"
    },
    method: "POST"
  })
  .then((response) => post_succesful_visible_2(response))
  .catch((error) => post_failed_visible(error));


  btn.classList.remove("submission_button_login--loading");

  document.getElementById("button_post_log_in").disabled = false;

  setTimeout(() => {
    document.getElementById("succesful_post").classList.add("hidden_div");
    document.getElementById("failed_post").classList.add("hidden_div");
  }, "5000");
  


} 