(function(){
  this.init = function(){};
  
  this.domLoaded = function(){
    widget();
    embed();
  };

  function embed(){
    $("#send_player").bind('ajaxcomplete', function(e, response){
      if(response.success){
        console.log("sucesso");
        location.reload();
        return;
      }
    });
  }
  
  function widget(){
    $(document).bind('soundcloud:onPlayerReady', function(event, data) {
        var apiUrl = data.mediaUri + '.json?callback=?';
        $.getJSON(apiUrl, function(data) {
          $('<h3>' + data.title + '</h3>').appendTo(document.body);
          var img = new Image();
          img.src = data.artwork_url;
          $(img).appendTo(document.body);
        });
      });
  }
  
  this.init();
  $(this.domLoaded);
})();