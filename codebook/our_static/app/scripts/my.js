$(document).ready(function () {
    $('.parallax').parallax();
    var insti = [];
    $.getJSON('/api/institute.json',function(data){
      $.each(data,function(i,item){
        $('#institute_list').append('<h3>'+item.name+'</h3>')
        insti.push(item.name);
      });

    console.log(insti);
    $('#institute_search').autocomplete({
    lookup: insti,
    onSelect: function (suggestion) {
        alert('You selected: ' + suggestion.value + ', ' + suggestion.data);
    }
    });
  });

  var user = [];
  $.getJSON('/api/users.json',function(data){
    $.each(data,function(i,item){
      user.push(item.username);
    });
    $('#user_search').autocomplete({
    lookup: user,
    onSelect: function (suggestion) {
        window.location.href = "/profile/"+suggestion.value;
    }
    });
  });


});
