var canvas  = $("#canvas"),
    context = canvas.get(0).getContext("2d")
    $result = $('#result');

var img_list = [];

$('#photoBtn').on('change', function(){
    if (this.files && this.files[0]) {
      if (this.files[0].type.match(/^image\//) ) {
        var reader = new FileReader();
        reader.onload = function(evt) {
           var img = new Image();
           img.onload = function() {
             context.canvas.height = img.height;
             context.canvas.width  = img.width;
             context.drawImage(img, 0, 0);
             var cropper = canvas.cropper({
               aspectRatio: 1 / 1
             });
             $('#complete').click(function() {
                if(img_list.length > 12) {
                  alert("이미지가 너무 많아요")
                }
                var croppedImageDataURL = canvas.cropper('getCroppedCanvas').toDataURL("image/png"); 
                var img = $('<img>').attr('class', 'result_img').attr('src', croppedImageDataURL);
                img_list.push(croppedImageDataURL);
                $result.append(img);
                if(img_list.length < 12){
                  $('#complete').html(`${img_list.length}/12개 업로드`)
                } else {
                  $('#complete').html(`이미지 업로드 완료`)
                  // TODO: deploy code
                }
             });
             $('#resetPhoto').click(function() {
               canvas.cropper('reset');
               canvas.empty();
             });
           };
           img.src = evt.target.result;
				};
        reader.readAsDataURL(this.files[0]);
      }
      else {
        alert("Invalid file type! Please select an image file.");
      }
    }
    else {
      alert('No file(s) selected.');
    }
});