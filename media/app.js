window.onload = function() {
    var ws_url = '/ws/foobar?subscribe-broadcast&publish-broadcast&echo';
	var ws = new WebSocket('ws://'+location.hostname+(location.port ? ':' + location.port : '') + ws_url);
    var $message = $('#message');
    var $table = $('#loaded-images');

    ws.onopen = function(){
      $message.attr("class", 'label label-success');
      $message.text('open');
    };

    var create_row = function (data) {
      var id = $("<td></td>").text(data.id);
      var created = $("<td></td>").text(new Date(data.created * 1000));
      var converted_date = data.converted_datetime ? new Date(data.converted_datetime * 1000) : "";
      var converted = $("<td></td>").text(converted_date);
      var element = $("<tr></tr>").append(id, created, converted);
      element.attr("id", "row_" + data.id);
      return element;
    };

    ws.onmessage = function(ev){
      $message.attr("class", 'label label-info');
      $message.hide();
      $message.fadeIn("slow");
      $message.text('recieved message');
      var json = JSON.parse(ev.data);
      var $rowid = $('#row_' + json.id);
      if ($rowid)
          $rowid.remove();
      $table.append(create_row(json))
    };

    ws.onclose = function(ev){
      $message.attr("class", 'label label-important');
      $message.text('closed');
    };

    ws.onerror = function(ev){
      $message.attr("class", 'label label-warning');
      $message.text('error occurred');
    };
};
