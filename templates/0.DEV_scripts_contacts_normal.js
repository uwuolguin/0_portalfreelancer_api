
function post_succesful_visible_2(response,id){

  let id_text = id.toString();
  suc_tex_id="succesful_post_"+id_text
  const status = ((response.status).toString()).substring(0, 1);

  if (status ==="2") {
    document.getElementById(suc_tex_id).classList.remove("hidden_div")
    document.getElementById(suc_tex_id).classList.remove("red_text")
    document.getElementById(suc_tex_id).classList.add("green_text")
    document.getElementById(suc_tex_id).innerHTML="Succesful Request"

  } else {
    
    document.getElementById(suc_tex_id).classList.remove("hidden_div")
    document.getElementById(suc_tex_id).classList.remove("green_text")
    document.getElementById(suc_tex_id).classList.add("red_text")
    document.getElementById(suc_tex_id).innerHTML="Failed Request. You can send and receive 1 email per day. We support the sending of 300 emails per day. Only Companies/Employers can contact Professionals"

  }

}

function post_failed_visible(error,id){

  console.log(error.detail)
  
  let id_text_2 = id.toString();
  fail_tex_id="failed_post_"+id_text_2
  document.getElementById(fail_tex_id).classList.remove("hidden_div")

  
}

async function postLogIn(id) {

  let id_text_3 = id.toString();
  button_tex_id="button_post_log_in_"+id_text_3

  console.log(button_tex_id)

  document.getElementById(button_tex_id).disabled = true;

  btn=document.getElementById(button_tex_id);
  btn.classList.toggle("submission_button_login--loading");

  url="https://apiportalfreelancer.lat/contacts/contacts/post/"+id_text_3


   await fetch(url, {
    headers: {
      Accept: "application/json"
    },
    method: "POST"
  })
  .then((response) => post_succesful_visible_2(response,id=id))
  .catch((error) => post_failed_visible(error,id=id));


  btn.classList.remove("submission_button_login--loading");

  document.getElementById(button_tex_id).disabled = false;

  setTimeout(() => {
    document.getElementById("succesful_post").classList.add("hidden_div");
    document.getElementById("failed_post").classList.add("hidden_div");
  }, "5000");
  
} 