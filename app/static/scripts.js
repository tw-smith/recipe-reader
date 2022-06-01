





function previewImg() {
  const canvas2 = document.getElementById("democanvas");
  console.log(canvas2)
  const ctx2 = canvas2.getContext("2d");
  const file = document.querySelector("#file-upload").files[0];
  const reader = new FileReader();
  var image = new Image();
  var ratio
  var hRatio
  var vRatio

    reader.readAsDataURL(file);
    reader.onload = function () {
      image.src = reader.result;
      console.log(image.src)
      hRatio = canvas2.width / image.width;
      vRatio = canvas2.height / image.height;
      ratio = Math.min(hRatio,vRatio);
      ctx2.drawImage(image,0,0,image.width,image.height,0,0,image.width*ratio,image.height*ratio);
    }




};

//
// function cropImg(){
//   console.log("in cropImg")
//   const canvas = document.getElementById("democanvas");
//   const ctx = canvas.getContext("2d");
//   var isDrawing = false;
//   var startX;
//   var startY;
//   var deltaX;
//   var deltaY;
//   var endX;
//   var endY;
//   var offsetX = canvas.offsetLeft;
//   var offsetY = canvas.offsetTop;
//   var ratio
//   var hRatio
//   var vRatio
//
//   const file = document.querySelector("#file-upload").files[0];
//   const reader = new FileReader();
//   var image = new Image();
//
//   //if (file) {
//     reader.readAsDataURL(file);
//     image.src = reader.result;
//   //}
//
//   //reader.addEventListener("load", function () {
//   //  image.src = reader.result;
//   //}, false);
//
//
//
//
//   //image.onload = function(){
//     hRatio = canvas.width / image.width;
//     vRatio = canvas.height / image.height;
//     ratio = Math.min(hRatio,vRatio);
//     ctx.drawImage(image,0,0,image.width,image.height,0,0,image.width*ratio,image.height*ratio);
// //  };
//   canvas.onmousedown = (e) => {
//     canvas.style.cursor = "crosshair"
//     isDrawing = true;
//     startX = parseInt(e.pageX - offsetX);
//     startY = parseInt(e.pageY - offsetY);
//   }
//
//   canvas.onmouseup = (e) => {
//     canvas.style.cursor = "default"
//     isDrawing = false;
//
//   }
//
//   canvas.onmousemove = (e) => {
//     if (isDrawing) {
//       var mouseX = parseInt(e.pageX - offsetX);
//       var mouseY = parseInt(e.pageY - offsetY);
//
//       ctx.clearRect(0,0,canvas.width,canvas.height);
//       ctx.drawImage(image,0,0,image.width,image.height,0,0,image.width*ratio,image.height*ratio);
//       ctx.strokeStyle = "red";
//       ctx.beginPath();
//       endX = mouseX;
//       endY = mouseY;
//       deltaX = mouseX - startX;
//       deltaY = mouseY - startY;
//       ctx.rect(startX, startY, deltaX, deltaY);
//       ctx.stroke();
//       ctx.strokeText(mouseX,100,0)
//       ctx.strokeText(mouseY,200,0)
//     }
//   }
//
//   document.getElementById("submit-image-button").onclick = () => {
//     console.log("crop function")
//     cropWidth = (endX - startX)/hRatio;
//     cropHeight = (endY - startY)/vRatio;
//     var hCropRatio = canvas.width / cropWidth;
//     var vCropRatio = canvas.height / cropHeight;
//     cropRatio = Math.min(hCropRatio,vCropRatio);
//   //  console.log(hCropRatio)
//   //  console.log(vCropRatio)
//   //  console.log(cropRatio)
//     console.log(startX/hRatio)
//     console.log(startY/vRatio)
//     console.log(cropWidth)
//     console.log(cropHeight)
//     console.log(offsetX)
//
//     ctx.clearRect(0,0,canvas.width,canvas.height);
//     ctx.drawImage(image,startX/vRatio,startY/vRatio,cropWidth,cropHeight,0,0,cropWidth*hRatio,cropHeight*vRatio);
//   }
// };
