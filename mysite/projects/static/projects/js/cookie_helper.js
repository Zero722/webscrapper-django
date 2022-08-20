console.log("apple")
// function toggle(){
//     if($("#json_div").css('display') == 'none'){
//         $("#url_div").css("display", "none");
//         $("#json_div").css("display", "block");
//         $("#toggle_btn").html("View CSV Upload");
//     }else{
//         $("#json_div").css("display", "none");
//         $("#url_div").css("display", "block");
//         $("#toggle_btn").html("View JSON Upload");
//     }
// }

// console.log("apple")
// function getCookie(user) {
//     var cookieArr = document.cookie.split(";");
//     for (var i = 0; i < cookieArr.length; i++) {
//         var cookiePair = cookieArr[i].split("=");
//         if (user == cookiePair[0].trim()) {
//             return decodeURIComponent(cookiePair[1]);
//         }
//     }
//     return null;
// }

// function checkCookie() {
//     $(".latest_download").hide();
//     var latest_url = getCookie("latest_url");
//     if (latest_url != null) {
//         $(".latest_download").show();
//         url_href = "{% get_media_prefix %}path_to_upload/" + latest_url + ".csv";
//         document.getElementById("latest_file").href = url_href;
//     }
// }
checkCookie();


// $(".csv_upload").click(function (e) {
//     e.preventDefault();
//     $("#url_upload_msg").text("The csv file is being prepared. Please wait for a while ");
//     $("#download_latest").attr('disabled', true);
//     var data = new FormData();
//     data.append("file", $("input[id^='csvfile']")[0].files[0]);
//     data.append("csrfmiddlewaretoken", "{{ csrf_token }}");
//     data.append("scheme_name", $('#scheme_name option:selected').val());
//     console.log("sdfgsdg")

//     $.ajax({

//         url: "{% url 'uploadcsv' %}",
//         method: "POST",
//         data: data,
//         processData: false,
//         contentType: false,
//         mimeType: "multipart/form-data",
//         success: function (response) {
//             console.log("Success")
//             console.log(response);
//             response = JSON.parse(response)
//             $("#url_upload_msg").text(response.message);
//             url_href = "{% get_media_prefix %}path_to_upload/" + getCookie("latest_url") + ".csv";
            
//             if (response.message != 'Error: Invalid URL') {
//                 url_href = "{% get_media_prefix %}path_to_upload/" + response.urls + ".csv";
//                 document.getElementById("download_scraped_data").href = url_href;
//                 $(".download_btn").show();
//             }
//             document.getElementById("latest_file").href = url_href;
            
//             if (getCookie("latest_url") != null) {
//                 $(".latest_download").show();
//                 $("#download_latest").attr('disabled', false);
//             }

//         },
//         error: function (error) {
//             console.log(error);
//             console.log("Error")
//             $("#download_latest").attr('disabled', false);
//             $("#url_upload_msg").text("Some error occured. Please try again");

//         }
//     })
// });


// $(".both_upload").click(function (e) {
//     e.preventDefault();
//     $("#both_upload_msg").text("The files are being processed. Please wait for a while ");
//     $("#download_latest").attr('disabled', true);
//     var data = new FormData();
//     data.append("csv_file", $("input[id^='csvfile']")[0].files[0]);
//     data.append("json_file", $("input[id^='jsonfile']")[0].files[0]);

//     data.append("csrfmiddlewaretoken", "{{ csrf_token }}");
//     console.log("hreth")

//     $.ajax({

//         url: "{% url 'upload_csv_json' %}",
//         method: "POST",
//         data: data,
//         processData: false,
//         contentType: false,
//         mimeType: "multipart/form-data",
//         success: function (response) {
//             console.log("Success")
//             console.log(response);
//             response = JSON.parse(response)
//             $("#both_upload_msg").text(response.message);
//             url_href = "{% get_media_prefix %}path_to_upload/" + getCookie("latest_url") + ".csv";
            
            
//             if (response.message != 'Error: Invalid URL') {
//                 url_href = "{% get_media_prefix %}path_to_upload/" + response.urls + ".csv";
//                 document.getElementById("download_scraped_data").href = url_href;
//                 $(".download_btn").show();
//             }
//             document.getElementById("latest_file").href = url_href;
            
//             if (getCookie("latest_url") != null) {
//                 $("#download_latest").attr('disabled', false);
//                 $(".latest_download").show();
//             }


//         },
//         error: function (error) {
//             console.log(error);
//             console.log("Error")
//             $("#download_latest").attr('disabled', false);
//             $("#both_upload_msg").text("Some error occured. Please try again");
//         }
//     })
// });
