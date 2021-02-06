var canvas  = $("#canvas"),
    context = canvas.get(0).getContext("2d")
    $result = $('#result');
var lists = [];
var names = ["ad", "0c", "d0", "74", "13", "03", "66", "84", "5f", "56", "50"];
var formData = new FormData();

function dataURItoBlob(dataURI) {
  var byteString = atob(dataURI.split(',')[1]);

  var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];

  var ab = new ArrayBuffer(byteString.length);
  var ia = new Uint8Array(ab);
  for (var i = 0; i < byteString.length; i++) {
    ia[i] = byteString.charCodeAt(i);
  }

  return new Blob([ab], {type: mimeString});
}

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
              if(lists.length < 11){
                var croppedImageDataURL = canvas.cropper('getCroppedCanvas').toDataURL("image/png"); 
                var img = $('<img>').attr('class', 'result_img').attr('src', croppedImageDataURL);
                var blob = dataURItoBlob(croppedImageDataURL);
                formData.append(names[lists.length], blob);
                lists.push(blob);
                $result.append(img);
                $('#complete').html(`${lists.length}/11개 업로드`);
              } else {
                $('#complete').html(`이미지 업로드 완료`)
                $.ajax({
                  url: "/upload",
                  processData: false,
                  contentType: false,
                  data: formData,
                  type: 'POST',
                  success: function(data) {
                    console.log(data)
                  }
                });
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
    } else {
      alert("Invalid file type! Please select an image file.");
    }
  } else {
    alert('No file(s) selected.');
  }
});