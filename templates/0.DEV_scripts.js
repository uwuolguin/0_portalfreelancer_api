async function postTalent() {

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


}
  

    // const body = new FormData
    // body.append("username", "hola")
    // body.append("", "\\")
    // body.append("password", "hola")
    // body.append("", "\\")
    // body.append("file", "@Banco_Itaú_logo.svg;type=image/svg+xml")
    
    // fetch("http://127.0.0.1:8000/sign_up/", {
    //   body,
    //   headers: {
    //     Accept: "application/json",
    //     "Content-Type": "multipart/form-data",
    //     "Access-Control-Allow-Origin": "*"
    //   },
    //   method: "POST"
    // })

