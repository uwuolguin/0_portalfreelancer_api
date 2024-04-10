
function lensButtonRequest(){



  
  let glassValueStateButton= document.getElementById('lens_button').value
  
  if(glassValueStateButton==""){
    
    glassValueStateButton="None"
  
  }

  
  urlFinal=  "https://apiportalfreelancer.lat/contacts/contacts_normal/?skills_string=None&skills_state_string=None&category_string=None&category_state_string=None&pagination_state=1.2.3.4.5.6.7.8.9.10&pagination_value=1&magic_word="+glassValueStateButton
  
  console.log(urlFinal)
  
  
  location.href =urlFinal
  
  }