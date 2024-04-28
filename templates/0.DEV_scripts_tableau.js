// enter equals click in search
document.getElementById("lens_button")
    .addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.key === 'Enter') {
        document.getElementById("lens_button_id_button").click();
    }
});

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
    document.getElementById("succesful_post").innerHTML="Failed Request"

  }

}

function post_failed_visible(error){
  console.log(error.detail)
  document.getElementById("failed_post").classList.remove("hidden_div")

  
}

async function deleteBanFunction(type_input) {

  if (type_input === 'talentDelete') {

    btn= document.getElementById("button_tableau_delete_talent");
    oFormObject = document.forms['form8'];
    word=oFormObject.elements["talent_id"].value;
  }

  document.getElementById("button_tableau_delete_talent").disabled = true;
  document.getElementById("button_tableau_delete_firm").disabled = true;
  document.getElementById("button_tableau_ban_email").disabled = true;
  document.getElementById("button_tableau_ban_word").disabled = true;

  btn.classList.toggle("submission_button_login--loading");


  url='https://apiportalfreelancer.lat/talent/talent_delete_by_admin/id/'+word



  await fetch(url, {
    headers: {
    Accept: "application/json"
    },
    method: "DELETE"
  })
  .then((response) => post_succesful_visible_2(response))
  .catch((error) => post_failed_visible(error));


  btn.classList.remove("submission_button_login--loading");

  document.getElementById("button_tableau_delete_talent").disabled = false;
  document.getElementById("button_tableau_delete_firm").disabled = false;
  document.getElementById("button_tableau_ban_email").disabled = false;
  document.getElementById("button_tableau_ban_word").disabled = false;

  setTimeout(() => {
    document.getElementById("succesful_post").classList.add("hidden_div");
    document.getElementById("failed_post").classList.add("hidden_div");
  }, "5000");
  


} 

function lensButtonRequest(){



  
  let glassValueStateButton= document.getElementById('lens_button').value
  
  if(glassValueStateButton==""){
    
    glassValueStateButton="None"
  
  }

  
  urlFinal=  "https://apiportalfreelancer.lat/contacts/contacts_normal/?skills_string=None&skills_state_string=None&category_string=None&category_state_string=None&pagination_state=1.2.3.4.5.6.7.8.9.10&pagination_value=1&magic_word="+glassValueStateButton
  
  console.log(urlFinal)
  
  
  window.location.href =urlFinal
  return false;
  }



async function logOut() {

      await fetch("https://apiportalfreelancer.lat/auth/logout", {
        headers: {
          Accept: "application/json"
        },
        method: "DELETE"
      }).then((response) => console.log(response)).catch((error) => console.log(error));
    
     }

  

async function reloadPageAfterLogOuT(){

    await logOut()

    location.reload()

  }