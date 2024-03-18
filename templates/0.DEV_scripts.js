async function postTalent() {

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
  filename = file.name;
  fileextension=file.type

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

  console.log(categories);
  console.log(skills);
  console.log(email)
  console.log(password)
  console.log(filename)
  console.log(fileextension)
  console.log(full_name)
  console.log(profession)
  console.log(rate)
  console.log(description)
  console.log(github)
  console.log(linkedin)
  console.log(instagram)
  console.log(facebook)
  console.log(oFormObject.elements["categories"].value)
  console.log(oFormObject.elements["skills"].value)

  

const body = new FormData
body.append("rate", parseInt(rate))
body.append("", "\\")
body.append("skills", skills)
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
body.append("file", "@"+filename+";type="+fileextension)
body.append("", "\\")
body.append("categories", categories)
body.append("", "\\")
body.append("email", email)
body.append("", "\\")
body.append("description", description)
body.append("", "\\")
body.append("linkedin", linkedin)

fetch("https://apiportalfreelancer.lat/talent/talent_post/", {
  body,
  headers: {
    Accept: "application/json",
    "Content-Type": "multipart/form-data"
  },
  method: "POST"
})
.then(response => response.json())
.then(json => console.log(json))
.catch(err => console.log('Failed Request', err));

}