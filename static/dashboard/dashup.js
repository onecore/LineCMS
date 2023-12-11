$(function() {
    $('#upload-file-btn').click(function() {
        var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: '/upload',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                if (data['status'] === 0){
                  console.log("False")
                  return false;
                }
                $("#logoview").attr('src','/media/'+data['status']);
                swal("", 'Website Logo updated', "success");

            },
        });
    });

    $('#upload-fav-btn').click(function() {
        var form_data = new FormData($('#upload-fav')[0]);
        $.ajax({
            type: 'POST',
            url: '/upload_fav',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
              if (data['status'] === 0) {
                console.log("False")
                return false;
              }
                $("#favview").attr('src','/media/'+data['status']);
                swal("", 'Website Favicon updated', "success");

            },
        });
    });

    $('#upload-th-btn').click(function() {
        var form_data = new FormData($('#upload-file-th')[0]);
        $.ajax({
            type: 'POST',
            url: '/upload_th',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
              console.log(data)
                if (data.hasOwnProperty('theme')) {
                    swal("", `${data['theme']} Theme uploaded`, "success");
                    update_sel(data['list'])
                }else{
                  swal("", `Cannot process theme files`, "error");
                }
                
            },
        });
    });
});