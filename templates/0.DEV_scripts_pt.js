
function post_succesful_visible(response){


  const status = ((response.status).toString()).substring(0, 1);

  if (status ==="2") {
    document.getElementById("succesful_post").classList.remove("hidden_div")
    document.getElementById("succesful_post").classList.remove("red_text")
    document.getElementById("succesful_post").classList.add("green_text")
    document.getElementById("succesful_post").innerHTML="Your user was Created"
    document.location.href = "https://apiportalfreelancer.lat/";
  } else {
    
    document.getElementById("succesful_post").classList.remove("hidden_div")
    document.getElementById("succesful_post").classList.remove("green_text")
    document.getElementById("succesful_post").classList.add("red_text")
    document.getElementById("succesful_post").innerHTML="User was not Created"

  }


  


}

function post_failed_visible(error){
  console.log(error.detail)
  document.getElementById("failed_post").classList.remove("hidden_div")
  
}

async function postTalent() {

  document.getElementById("button_post").disabled = true;

  btn=document.querySelector(".custom-file-upload-2");
  btn.classList.toggle("custom-file-upload-2--loading");

  const responseCategories = await fetch("https://apiportalfreelancer.lat/categories/categories_get_all", {
    headers: {
      Accept: "application/json"
    }
  });
  const categories = await responseCategories.json();
  
  const responseSkills = await   fetch("https://apiportalfreelancer.lat/skills/skills_get_all", {
    headers: {
      Accept: "application/json"
    }
  });
  const skills = await responseSkills.json();

  oFormObject = document.forms['form7'];

  email=oFormObject.elements["email"].value
  password=oFormObject.elements["password"].value

  myFile=document.getElementById("file")
  file = myFile.files[0];  

  full_name=oFormObject.elements["full_name"].value
  profession=oFormObject.elements["profession"].value
  rate=oFormObject.elements["rate"].value
  description=oFormObject.elements["description"].value

  github=oFormObject.elements["github"].value
  linkedin=oFormObject.elements["linkedin"].value
  instagram=oFormObject.elements["instagram"].value
  facebook=oFormObject.elements["facebook"].value


  let categories_string = ""
  for (var category of categories) {

  id=(category.category.replace(/\s/g,'')).concat("-category")
  checkbox_value=oFormObject.elements[id].checked

  if (checkbox_value ===true){

    categories_string=categories_string.concat(category.category.concat('.'))

  }

  }

  oFormObject.elements["categories"].value=categories_string

  let skills_string = ""
  for (var skill of skills) {

  id=(skill.skill.replace(/\s/g,'')).concat("-skill")
  checkbox_value=oFormObject.elements[id].checked

  if (checkbox_value ===true){

    skills_string=skills_string.concat(skill.skill.concat('.'))

  }

  }

  oFormObject.elements["skills"].value=skills_string
  
const body = new FormData
body.append("rate", parseInt(rate))
body.append("", "\\")
body.append("skills", oFormObject.elements["skills"].value)
body.append("", "\\")
body.append("github", github)
body.append("", "\\")
body.append("facebook", facebook)
body.append("", "\\")
body.append("instagram", instagram)
body.append("", "\\")
body.append("full_name", full_name)
body.append("", "\\")
body.append("password", password)
body.append("", "\\")
body.append("profession", profession)
body.append("", "\\")
body.append("file", file);
body.append("", "\\")
body.append("categories", oFormObject.elements["categories"].value)
body.append("", "\\")
body.append("email", email)
body.append("", "\\")
body.append("description", description)
body.append("", "\\")
body.append("linkedin", linkedin)


await fetch("https://apiportalfreelancer.lat/talent/talent_post/", {
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