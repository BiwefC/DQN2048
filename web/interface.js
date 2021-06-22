$(document).ready(function(e){
    newgame();
});

function newgame() {
  init();
  $.ajax({
    url: "newgame",
    type: "POST",
    success: function (result) {
      updtBoard(result.board)
      updtScore(result.score)
    }
  });
}

function init() {
  $("#gameover").css('display','none');
  for(var i = 0;i<4;i++){
    for(var j = 0;j<4;j++){
      var gridCell = $("#grid-cell-"+i+"-"+j);
      gridCell.css("top",getPosTop(i,j));
      gridCell.css("left",getPosLeft(i,j));
    }
  }
}

function updtScore(score) {
  document.getElementById("score").innerHTML=score;
}

function updtBoard(board) {
  $(".number-cell").remove();
  for (var i = 0; i < 4; i++){
    for (var j = 0; j < 4; j++) {
      $("#grid-container").append('<div class="number-cell" id="number-cell-'+i+'-'+j+'"></div>');
      var theNumberCell = $('#number-cell-'+i+'-'+j);
      if (board[i][j] == 1){
        theNumberCell.css('width','0px');
        theNumberCell.css('height','0px');
        theNumberCell.css('top',getPosTop(i,j));
        theNumberCell.css('left',getPosLeft(i,j));
      }
      else{
        theNumberCell.css('width','100px');
        theNumberCell.css('hegiht','100px');
        theNumberCell.css('top',getPosTop(i,j));
        theNumberCell.css('left',getPosLeft(i,j));
                //NumberCell覆盖
        theNumberCell.css('background-color',getNumberBackgroundColor(board[i][j]));//返回背景色
        theNumberCell.css('color',getNumberColor(board[i][j]));//返回前景色
        theNumberCell.text(board[i][j]);
      }
    }
  }
}


$(document).keydown(function(event){
  var direct;
  var find = false;
  switch (event.keyCode) {
    case 37://left
      direct = "left";
      find = true;
      break;
    case 38://up
      direct = "up";
      find = true;
      break;
    case 39://right
      direct = "right";
      find = true;
      break;
    case 40://down
      direct = "down";
      find = true;
      break;
  }
  if (find) {
    $.ajax({
      url: "step",
      type: "POST",
      data: {"direct": direct},
      success: function (result) {
        updtBoard(result.board);
        updtScore(result.score);
        if (result.end) {
          gameover();
        }
      }
    });
  }
});

function gameover(){
    $("#gameover").css('display','block');
}

function getPosTop(i, j) {
  return 20 + i * 120;
}
 
function getPosLeft(i, j) {
  return 20 + j * 120;
}

function getNumberBackgroundColor(number) {
  switch (number) {
    case 2:
      return "#eee4da";
      break;
    case 4:
      return "#eee4da";
      break;
    case 8:
      return "#f26179";
      break;
    case 16:
      return "#f59563";
      break;
    case 32:
      return "#f67c5f";
      break;
    case 64:
      return "#f65e36";
      break;
    case 128:
      return "#edcf72";
      break;
    case 256:
      return "#edcc61";
      break;
    case 512:
      return "#9c0";
      break;
    case 1024:
      return "#3365a5";
      break;
    case 2048:
      return "#09c";
      break;
    case 4096:
      return "#a6bc";
      break;
    case 8192:
      return "#93c";
      break;
    }
  return "black";
}
 
function getNumberColor(number) {
  if (number <= 4){
    return "#776e65";
  }
  return "white";
}

