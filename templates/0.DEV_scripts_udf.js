
function post_succesful_visible(response){


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
    document.getElementById("succesful_post").innerHTML="Failed Request"

  }

}

function post_failed_visible(error){
  console.log(error.detail)
  document.getElementById("failed_post").classList.remove("hidden_div")
  
}

async function updateTalent() {

  document.getElementById("button_post_update").disabled = true;

  btn=document.querySelector(".custom-file-upload-2");
  btn.classList.toggle("custom-file-upload-2--loading");

  oFormObject = document.forms['form7'];

  password=oFormObject.elements["password"].value

  full_name=oFormObject.elements["full_name"].value
  contact_email=oFormObject.elements["contact_email"].value
  contact_phone=oFormObject.elements["contact_phone"].value
  email_template_to_send=oFormObject.elements["email_template_to_send"].value

  linkedin=oFormObject.elements["linkedin"].value
  instagram=oFormObject.elements["instagram"].value

  const body = new FormData
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

  await fetch("https://apiportalfreelancer.lat/firm/firm_put/", {
    body,
    headers: {
    Accept: "application/json"
    },
    method: "PUT"
  })
  .then((response) => post_succesful_visible(response))
  .catch((error) => post_failed_visible(error));


  btn.classList.remove("custom-file-upload-2--loading");

  document.getElementById("button_post_update").disabled = false;

  setTimeout(() => {
    document.getElementById("succesful_post").classList.add("hidden_div");
    document.getElementById("failed_post").classList.add("hidden_div");
  }, "5000");

} 

async function deleteTalent() {

  document.getElementById("button_post_delete").disabled = true;

  btn=document.querySelector(".custom-file-upload-2");
  btn.classList.toggle("custom-file-upload-2--loading");

  

  await fetch("https://apiportalfreelancer.lat/firm/firm_delete/id/", {
    headers: {
      Accept: "*/*"
    },
    method: "DELETE"
  })
  .then((response) => post_succesful_visible(response))
  .catch((error) => post_failed_visible(error));


  await fetch("https://apiportalfreelancer.lat/auth/logout", {
    headers: {
      Accept: "application/json"
    },
    method: "DELETE"
  })
  .then((response) => console.log(response))
  .catch((error) => console.log(error));


  btn.classList.remove("custom-file-upload-2--loading");

  document.getElementById("button_post_delete").disabled = false;

  setTimeout(() => {
    document.getElementById("succesful_post").classList.add("hidden_div");
    document.getElementById("failed_post").classList.add("hidden_div");
  }, "5000");

} 