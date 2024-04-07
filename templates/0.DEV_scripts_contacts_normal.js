
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

async function postLogIn(id_var) {

  let id_text_3 = id_var.toString();
  button_tex_id="button_post_log_in_"+id_text_3
  suc_tex_id="succesful_post_"+id_text_3
  fail_tex_id="failed_post_"+id_text_3

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
  .then((response) => post_succesful_visible_2(response,id=id_var))
  .catch((error) => post_failed_visible(error,id=id_var));


  btn.classList.remove("submission_button_login--loading");
  btn.classList.add("hidden_div");

  document.getElementById(button_tex_id).disabled = false;

  setTimeout(() => {
    document.getElementById(suc_tex_id).classList.add("hidden_div");
    document.getElementById(fail_tex_id).classList.add("hidden_div");
    btn.classList.remove("hidden_div");
  }, "5000");
  
} 
// PAGINATION LOGIC ********************************************************************************************************************************************************

function paginationMinusClick(){
  let pag_value_1 = document.getElementById("pagination_one").innerHTML;

  if (pag_value_1 > 10) {

    document.querySelectorAll('.w3-button-m').forEach(elem => {
      elem.innerHTML = elem.innerHTML-10;
    });

    document.querySelectorAll('.w3-button-m').forEach(elem => {
      elem.classList.remove("w3-button-active");
    });

  }

}

function paginationPlusClick(){


    document.querySelectorAll('.w3-button-m').forEach(elem => {
      elem.innerHTML = parseInt(elem.innerHTML)+10;
    });

    document.querySelectorAll('.w3-button-m').forEach(elem => {
      elem.classList.remove("w3-button-active");
    });
}
//SENDING REQUEST FOR HTML BY USING THE PAGINATION BUTTONS

function paginationBackground(clicked_object){

// DISABLE ALL BUTTONS UNTIL PAGE IS CHARGED

document.querySelectorAll('.w3-button-m').forEach(elem => {
  elem.disabled=true;
  });
document.querySelectorAll('.submission_button_login').forEach(elem => {
    elem.disabled=true;
  });
document.querySelectorAll('.submission_button').forEach(elem => {
    elem.disabled=true;
  });
document.querySelectorAll('input[type="checkbox"]').forEach(elem => {
    elem.disabled=true;
  });


  
//CHANGE STATE PAGINATION
  let current_id = clicked_object.getAttribute("id")

    document.querySelectorAll('.w3-button-m').forEach(elem => {
    elem.classList.remove("w3-button-active");
    });
  document.getElementById(current_id).classList.add("w3-button-active")


  paginationState1=document.getElementById("pagination_one").innerHTML
  paginationState2=document.getElementById("pagination_two").innerHTML
  paginationState3=document.getElementById("pagination_three").innerHTML
  paginationState4=document.getElementById("pagination_four").innerHTML
  paginationState5=document.getElementById("pagination_five").innerHTML
  paginationState6=document.getElementById("pagination_six").innerHTML
  paginationState7=document.getElementById("pagination_seven").innerHTML
  paginationState8=document.getElementById("pagination_eight").innerHTML
  paginationState9=document.getElementById("pagination_nine").innerHTML
  paginationState10=document.getElementById("pagination_ten").innerHTML

// Pagiantion State General
 let paginationState= paginationState1+'.'+paginationState2+'.'+paginationState3+'.'+paginationState4+'.'+paginationState5+'.'+paginationState6+'.'+paginationState7+'.'+paginationState8+'.'+paginationState9+'.'+paginationState10

let paginationStateSelected= document.getElementById(current_id).innerHTML





let skillStringValues=''
let skillStringState=''

let checkboxArraySkills=document.getElementById('checkbox_container_skills').getElementsByTagName('input')

for (let i = 0; i < checkboxArraySkills.length; i++) {

  		if (checkboxArraySkills[i].checked){
			skillStringValues=skillStringValues+checkboxArraySkills[i].value+'.'
			skillStringState=skillStringState+checkboxArraySkills[i].id+'.'

			}

}

if(skillStringValues==""){
  
  skillStringValues="None"

} else {
  skillStringValues = skillStringValues.slice(0, -1); 
}

if(skillStringState==""){
  
  skillStringState="None"

} else {

  skillStringState = skillStringState.slice(0, -1); 

}

let categoryStringValues=''
let categoryStringState=''

let checkboxArrayCategories=document.getElementById('checkbox_container_categories').getElementsByTagName('input')

for (let i = 0; i < checkboxArrayCategories.length; i++) {

  		if (checkboxArrayCategories[i].checked){
			categoryStringValues=categoryStringValues+checkboxArrayCategories[i].value+'.'
			categoryStringState=categoryStringState+checkboxArrayCategories[i].id+'.'

			}

}

if(categoryStringValues==""){
  
  categoryStringValues="None"

} else {
  categoryStringValues = categoryStringValues.slice(0, -1); 
}

if(categoryStringState==""){
  
  categoryStringState="None"

} else {


  categoryStringState = categoryStringState.slice(0, -1); 
}

let glassValueStateButton= document.getElementById('lens_button').value

if(glassValueStateButton==""){
  
  glassValueStateButton="None"

}
console.log(paginationState)
console.log(paginationStateSelected)
console.log(skillStringValues)
console.log(skillStringState)
console.log(categoryStringValues)
console.log(categoryStringState)
console.log(glassValueStateButton)

url_part1="https://apiportalfreelancer.lat/contacts/contacts_normal/?"
url_part2="skills_string="+skillStringValues+"&"
url_part3="skills_state_string="+skillStringState+"&"
url_part4="category_string="+categoryStringValues+"&"
url_part5="category_state_string="+categoryStringState+"&"
url_part6="pagination_state="+paginationState+"&"
url_part7="pagination_value="+paginationStateSelected+"&"
url_part8="magic_word="+glassValueStateButton

urlFinal=url_part1+url_part2+url_part3+url_part4+url_part5+url_part6+url_part7+url_part8

console.log(urlFinal)


location.href =urlFinal

}


