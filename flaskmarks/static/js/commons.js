$(function(){

    $('.clickIncrement').on('click', function(){
        var id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        $.ajax({
          url: url,
          data: {id : id},
          type: 'GET',
          dataType: 'json',
          success: function(data) {
              if (data.status == 'success') {
                  return
              }
          }
        });
    });

    $('.delete').on('click', function(){
        if (confirm('Are you sure you want to delete this?')) {
            return true;
        } else {
            return false;
        }
    });

    if ($(".markform").length && !$("#edit.markform").length) {

        var feedString = 'http://gdata.youtube.com/feeds/api/users/CHANNELNAME/uploads?max-results=30'

        $("label[for='url']").append(
            ' <a href="#" id="jqYoutube" style="font-size:0.7em; padding-left: 5px;">Youtube feed?</a>'
        );

        $("#jqYoutube").on('click', function(){
            $("#url").val(feedString);
            $("input[value='feed']").attr('checked', 'checked');
            if (!$("#url").next(".description").length) {
                $("#url").after(
                    '<span class="description">Remember to replace `CHANNELNAME` with something meaningful. </span>'
                );
            }
        });
    }

    //if ($("#content form").length) {
    //    $("#content form").find("input[type='text']").first().focus();
    //}

});
