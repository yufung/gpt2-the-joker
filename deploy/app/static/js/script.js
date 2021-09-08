$(document).ready(function() {
  $('form').on('submit', function(event) {
    $('#textprompt').prop('disabled', true);
    $('#button-addon').addClass('disabled');
    event.preventDefault();
    $.ajax({
      url: '/generate',
      type: 'POST',
      contentType: 'application/json; charset=UTF-8',
      dataType: 'json',
      data: JSON.stringify({textprompt: $('#textprompt').val()}),
      success: function(data) {
        var jsonObj = JSON.parse(data)
        get_task_info(jsonObj.task_id);
        
        function get_task_info(tid) {
          event.preventDefault();
          $.ajax({
            url: '/generate/' + tid,
            type: 'GET',
            contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
            dataType: 'json',
            success: function(data) {
              var jsonObj = JSON.parse(data)
              if (jsonObj.state == 'PENDING') {
                $('.output-content').html('Please wait...');
              }
              else if (jsonObj.state == 'PROGRESS') {
                $('.output-content').html('Please wait...');
              }
              else if (jsonObj.state == 'SUCCESS') {
                $('.output-content').html(jsonObj.result.replace("\n", "</p><p>"));
                $('#textprompt').removeAttr('disabled');
                $('#button-addon').removeClass('disabled');
              }
              if (jsonObj.state != 'SUCCESS') {
                setTimeout(function () {
                  get_task_info(tid)
                }, 500);
              }
            },
            error: function (data) {
              $('.output-content').html('Error!');
              $('#textprompt').removeAttr('disabled');
              $('#button-addon').removeClass('disabled');
            }
          });
        }
      },
      error: function(jqXHR, textStatus, errorThrown){}
    });
  });
});

