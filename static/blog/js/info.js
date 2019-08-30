$(function () {
    $('#forminput').click(function () {
        let captcha = $('.capt').html();
        let user_capt = $('#inputcapt').val();

        if (String(captcha) === String(user_capt)) {
            let id = $('.capt').attr('a_id');
            let name = $('#username').val().trim();
            let command = $('#command').val();
            if (name != "" && name.length<=8){
                $.ajax({
                    type: "GET",
                    url: '/command',
                    async: true,
                    data: {
                        'id': id,
                        'name': name,
                        'command': command,
                    },
                    success: (function (res) {
                        // alert(res)
                        // alert($('.commandlist:last-child').next())
                        $('#commandlist').append(` <div class="fb" ><ul id="commandlist"><p class=\"fbtime\"><span>${res.time}</span>${res.name}</p><p class=\"fbinfo\">${res.commands}</p></ul></div>`)
                        $('#username').val("")
                        $('#inputcapt').val("")
                        $('#command').val("")
                    }),
                    error: (function (res) {
                        console.log(res)
                    })
                })
            }else{
             alert("用户名长度大于8位或为空")
            }
        } else {
            alert("验证码输入不正确")
        }

    });

})

