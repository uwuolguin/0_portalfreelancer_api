
function post_succesful_visible(response){


  const status = ((response.status).toString()).substring(0, 1);

  if (status ==="2") {
    document.getElementById("succesful_post").classList.remove("hidden_div")
    document.getElementById("succesful_post").classList.remove("red_text")
    document.getElementById("succesful_post").classList.add("green_text")
    document.getElementById("succesful_post").innerHTML="Your user was Created"
    document.location.href = "https://apiportalfreelancer.lat/auth/logIn/";
  } else {
    
    document.getElementById("succesful_post").classList.remove("hidden_div")
    document.getElementById("succesful_post").classList.remove("green_text")
    document.getElementById("succesful_post").classList.add("red_text")
    document.getElementById("succesful_post").innerHTML="User was not Created"
    document.location.reload()
  }

}

function post_failed_visible(error){
  console.log(error.detail)
  document.getElementById("failed_post").classList.remove("hidden_div")
  document.location.reload()
  
}

async function postTalent() {

  document.getElementById("button_post").disabled = true;

  btn=document.querySelector(".custom-file-upload-2");
  btn.classList.toggle("custom-file-upload-2--loading");

  oFormObject = document.forms['form7'];

  email=oFormObject.elements["email"].value
  password=oFormObject.elements["password"].value

  full_name=oFormObject.elements["full_name"].value
  contact_email=oFormObject.elements["contact_email"].value
  contact_phone=oFormObject.elements["contact_phone"].value
  email_template_to_send=oFormObject.elements["email_template_to_send"].value

  linkedin=oFormObject.elements["linkedin"].value
  instagram=oFormObject.elements["instagram"].value

  const body = new FormData
  body.append("email", email)
  body.append("", "\\")
  body.append("password", password)
  body.append("", "\\")
  body.append("full_name", full_name)
  body.append("", "\\")
  body.append("contact_email", contact_email)
  body.append("", "\\")
  body.append("contact_phone", parseInt(contact_phone))
  body.append("", "\\")
  body.append("email_template_to_send", email_template_to_send)
  body.append("", "\\")
  body.append("instagram", instagram)
  body.append("", "\\")
  body.append("linkedin", linkedin)

  await fetch("https://apiportalfreelancer.lat/firm/firm_post/", {
    body,
    headers: {
    Accept: "application/json"
    },
    method: "POST"
  })
  .then((response) => post_succesful_visible(response))
  .catch((error) => post_failed_visible(error));


  btn.classList.remove("custom-file-upload-2--loading");

  document.getElementById("button_post").disabled = false;

  setTimeout(() => {
    document.getElementById("succesful_post").classList.add("hidden_div");
    document.getElementById("failed_post").classList.add("hidden_div");
  }, "5000");

} 