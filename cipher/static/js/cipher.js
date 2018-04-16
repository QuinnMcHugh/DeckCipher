
$('#btn-generate').click(function (){
  $.ajax({
    type: "POST",
    url: "generate_key",
    success: function (data){
      $('#generated-key').val(data['key']);
    },
    failure: function (data){
      $('#generated-key').val('failed to generate a key');
    },
  });
});

$('#btn-encipher').click(function (){
  // Check that input box only has lower case characters and whitespace
  var plaintext = $('#inputarea').val();
  var legalPattern = /([a-z]|\s)+/;
  var result = plaintext.match(legalPattern);

  if (!result || result[0] !== plaintext){
    alert('Your message should only include lower case characters');
    return;
  }

  $.ajax({
    type: "POST",
    url: "cipher_message",
    data: {
      action: $('#action option:selected').text(),
      key: $('#encipherment-key').val(),
      input: $('#inputarea').val().split(' ').join(''),
    },
    success: function (data){
      if (data.hasOwnProperty('error')){
        $('#outputarea').val(data['output']);
      }
      else {
        var reformatted = reformatOutput($('#inputarea').val(), data['output']);
        $('#outputarea').val(reformatted);
      }
    },
    failure: function (data){
      $('#outputarea').val('failed to process request');
    },
  });
});

function getWhitespaceIndices(text){
  var indices = [];
  for (var i = 0; i < text.length; i++){
    if (text.substring(i, i+1).match(/\s/)){
      indices.push(i);
    }
  }
  return indices;
}

// Make output match input's whitespace grouping
function reformatOutput(input, output){
  var indices = getWhitespaceIndices(input);
  indices.push(input.length);
  var outputChunks = [];
  for (var i = 0; i < indices.length; i++){
    var start = (i > 0) ? indices[i - 1] - (i - 1) : 0;
    var len = indices[i] - ((i > 0) ? indices[i - 1] : -1) - 1;
    outputChunks.push(output.substr(start, len));
  }
  return outputChunks.join(' ');
}


