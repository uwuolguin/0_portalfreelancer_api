

document.getElementById("lens_button")
    .addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.key === 'Enter') {
        document.getElementById("lens_button_id_button").click();
    }
});

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