function escapeHtml(unsafe)
{
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
 }

function myFunction() {
    // myFile=document.getElementById("lfile")
    // file = myFile.files[0];  
    // filename = file.name;
    // fileextension=file.type
    // text=filename
    // text2=fileextension
    // oFormObject = document.forms['form1'];
    // oFormObject.elements["username"].value = text;
    // oFormObject.elements["password"].value = text2;
    // document.getElementById("demo").innerHTML = "Paragraph changed.";

    const body = new FormData
    body.append("username", "hola")
    body.append("", "\\")
    body.append("password", "hola")
    body.append("", "\\")
    body.append("file", "@Banco_Itaú_logo.svg;type=image/svg+xml")
    
    fetch("http://127.0.0.1:8000/sign_up/", {
      body,
      headers: {
        Accept: "application/json",
        "Content-Type": "multipart/form-data",
        "Access-Control-Allow-Origin": "*"
      },
      method: "POST"
    })

  }