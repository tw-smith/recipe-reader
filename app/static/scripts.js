const input = document.getElementById("file-upload")


//input.onchange = (e) => {
//  const [file] = e.target.files
//  var buttonText = document.getElementById("file-upload-label")
//  buttonText.innerHTML = file.name
//}



input.onchange = () => {
  console.log("in input.onchange function")
  let canvas = document.createElement("canvas");
  let  ctx = canvas.getContext("2d");
  canvas.width = 800;
  canvas.height = 800;

  let anchor = document.createElement("a");
  let surl = URL.createObjectURL(input.files[0]);


  let img = new Image();
  img.onload = () => {
    ctx.drawImage(img,170,20,300,300,0,0,300,300);
  };
};



//var img = new Image();

//img.onload = () => {
//  let canvas = document.getElementById("democanvas");
//  let ctx = canvas.getContext("2d");

//  ctx.drawImage(img,170,20,300,300,0,0,300,300);
//};

//img.src = "5.jpg"
