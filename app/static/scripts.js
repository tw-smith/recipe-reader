function previewImg() {
  const canvas = document.getElementById("democanvas");
  const ctx = canvas.getContext("2d");
  const file = document.querySelector("#file-upload").files[0];
  const reader = new FileReader();
  var image = new Image();
  var ratio, hRatio, vRatio
  let offsetX, offsetY, startX, startY, deltaX, deltaY, endX, endY, isDrawing = false, cropRatio;


  reader.readAsDataURL(file);
  reader.onload = () => {
    image.src = reader.result;
    hRatio = canvas.width / image.width;
    vRatio = canvas.height / image.height;
  //  ratio = Math.min(hRatio,vRatio);
    ratio = 0.25; // FIXME Hard coding in 0.25 because hRatio and vRatio appear to go to Infinity for some reason. Variable scope maybe?

    image.onload = () => { // This image.onload function is required to make the image preview appear. Without it the image preview only appears when stepping through the JS in debug mode.
      ctx.drawImage(image,0,0,image.width,image.height,0,0,image.width*ratio,image.height*ratio);
      canvas.removeAttribute("hidden");
      offsetX = canvas.offsetLeft
      offsetY = canvas.offsetTop
    };
    
    canvas.onmousedown = (e) => {
      canvas.style.cursor = "crosshair"
      isDrawing = true;
      startX = parseInt(e.pageX - offsetX);
      startY = parseInt(e.pageY - offsetY);
    }
    
    canvas.onmouseup = (e) => {
      canvas.style.cursor = "default"
      isDrawing = false;
    }
  
    canvas.onmousemove = (e) => {
      if (isDrawing) {
        let mouseX = parseInt(e.pageX - offsetX);
        let mouseY = parseInt(e.pageY - offsetY);
        ctx.clearRect(0,0,canvas.width,canvas.height);
        ctx.drawImage(image,0,0,image.width,image.height,0,0,image.width*ratio,image.height*ratio);
        ctx.strokeStyle = "red";
        ctx.beginPath();
        endX = mouseX;
        endY = mouseY;
        deltaX = mouseX - startX;
        deltaY = mouseY - startY;
        console.log(startX)
        console.log(deltaX)
        ctx.rect(startX, startY, deltaX, deltaY);
        ctx.stroke();
        ctx.strokeText(mouseX,100,0)
        ctx.strokeText(mouseY,200,0)
      }
    }
  }


  document.getElementById("crop-image-button").onclick = () => {
    console.log("crop function")
    cropWidth = (endX - startX)/hRatio;
    cropHeight = (endY - startY)/vRatio;
    var hCropRatio = canvas.width / cropWidth;
    var vCropRatio = canvas.height / cropHeight;
    cropRatio = Math.min(hCropRatio,vCropRatio);
  //  console.log(hCropRatio)
  //  console.log(vCropRatio)
  //  console.log(cropRatio)
    console.log(startX/hRatio)
    console.log(startY/vRatio)
    console.log(cropWidth)
    console.log(cropHeight)
    console.log(offsetX)

    // FIXME draws a blank canvas
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.drawImage(image,startX/vRatio,startY/vRatio,cropWidth,cropHeight,0,0,cropWidth*hRatio,cropHeight*vRatio);
  }
};