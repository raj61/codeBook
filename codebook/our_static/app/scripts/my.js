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
 console.log("hello");
});
