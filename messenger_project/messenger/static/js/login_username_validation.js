$(document).ready(function(){
    $("#id_username").blur(function(){
        var username = $(this).val();
        $.ajax({
            url: checkUsernameURL, // Використовуйте змінну з URL
            data: {
                'username': username
            },
            dataType: 'json',
            success: function (data) {
                if (!data.is_taken) {
                    alert("Користувач з таким іменем не зареєстрований.");
                }
            }
        });
    });
});