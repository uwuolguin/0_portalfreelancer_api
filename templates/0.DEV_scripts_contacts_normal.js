
function post_succesful_visible_2(response){


  const status = ((response.status).toString()).substring(0, 1);

  if (status ==="2") {
    document.getElementById("succesful_post").classList.remove("hidden_div")
    document.getElementById("succesful_post").classList.remove("red_text")
    document.getElementById("succesful_post").classList.add("green_text")
    document.getElementById("succesful_post").innerHTML="Succesful Request"

  } else {
    
    document.getElementById("succesful_post").classList.remove("hidden_div")
    document.getElementById("succesful_post").classList.remove("green_text")
    document.getElementById("succesful_post").classList.add("red_text")
    document.getElementById("succesful_post").innerHTML="Failed Request. You can send and receive 1 email per day. We support the sending of 300 emails per day. Only Companies/Employers can contact Professionals"

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

  oFormObject = document.forms['form7'];

  email_sent=oFormObject.elements["email_sent"].value


  const body = new FormData
  body.append("email_sent",  email_sent)



  await fetch("https://apiportalfreelancer.lat/complaints/complaint_post/", {
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