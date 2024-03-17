function postTalent() {
    myFile=document.getElementById("file")
    file = myFile.files[0];  
    filename = file.name;
    fileextension=file.type
    oFormObject = document.forms['form7'];
    email=oFormObject.elements["email"].value
    password=oFormObject.elements["password"].value

    full_name=oFormObject.elements["full_name"].value
    profession=oFormObject.elements["profession"].value
    rate=oFormObject.elements["rate"].value
    password=oFormObject.elements["password"].value
    password=oFormObject.elements["password"].value
    password=oFormObject.elements["password"].value


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

  }