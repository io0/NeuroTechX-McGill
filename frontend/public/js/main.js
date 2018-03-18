$(document).ready(function(){
  $("div.emoji").toggle();
  $( "div.emojibtn" ).on( "click", function() {
    $("div.letters").toggle();
    $("div.emoji").toggle();
    });
  var hits = [];

  var NF_int = 100; // Non-flash interval
  var F_int = 200; // Flash interval
  var RC_int = 1000; // Row/Col interval
  var num_trials = 3; // number of trials
  var T_int = 3000; // Inter-trial interval

  var orderRow1 = [1, 4, 2, 5, 0, 3];
  var orderCol1 = [5, 3, 2, 0, 4, 1];
  var orderRow2 = [3, 2, 5, 0, 1, 4];
  var orderCol2 = [3, 2, 0, 1, 5, 4];
  var orderRow3 = [4, 0, 2, 3, 1, 5];
  var orderCol3 = [3, 4, 0, 5, 2, 1];


  // Trial 1
      function rowOn1(row) {
        $(".row-"+orderRow1[row]).toggleClass("litup");
        window.setTimeout(function() {
          rowOff1(row);
        }, F_int);}
      
      function rowOff1(row) {
        $(".row-"+orderRow1[row]).toggleClass("litup");
        window.setTimeout(function() {
          if(row >= 6){
            colOn1(0);
          } else {
            rowOn1(row+1);
          }
        }, NF_int);}


      function colOn1(col) {
        $(".col-"+orderCol1[col]).toggleClass("litup");
        window.setTimeout(function() {
          colOff1(col);
        }, F_int);}
      
      function colOff1(col) {
        $(".col-"+orderCol1[col]).toggleClass("litup");
        window.setTimeout(function() {
          if(col >= 6){
            window.setTimeout(function() {
              rowOn2(0);}, RC_int);
          } else {
            colOn1(col+1);
          }
          }, NF_int);}

// Trial 2

function rowOn2(row) {
  $(".row-"+orderRow2[row]).toggleClass("litup");
  window.setTimeout(function() {
    rowOff2(row);
  }, F_int);}

function rowOff2(row) {
  $(".row-"+orderRow2[row]).toggleClass("litup");
  window.setTimeout(function() {
    if(row >= 6){
      colOn2(0);
    } else {
      rowOn2(row+1);
    }
  }, NF_int);}


function colOn2(col) {
  $(".col-"+orderCol2[col]).toggleClass("litup");
  window.setTimeout(function() {
    colOff2(col);
  }, F_int);}

function colOff2(col) {
  $(".col-"+orderCol2[col]).toggleClass("litup");
  window.setTimeout(function() {
    if(col >= 6){
      window.setTimeout(function() {
        rowOn3(0);}, RC_int);
    } else {
      colOn2(col+1);
    }
    }, NF_int);}


//Trial 3


function rowOn3(row) {
  $(".row-"+orderRow3[row]).toggleClass("litup");
  window.setTimeout(function() {
    rowOff3(row);
  }, F_int);}

function rowOff3(row) {
  $(".row-"+orderRow3[row]).toggleClass("litup");
  window.setTimeout(function() {
    if(row >= 6){
      colOn3(0);
    } else {
      rowOn3(row+1);
    }
  }, NF_int);}


function colOn3(col) {
  $(".col-"+orderCol3[col]).toggleClass("litup");
  window.setTimeout(function() {
    colOff3(col);
  }, F_int);}

function colOff3(col) {
  $(".col-"+orderCol3[col]).toggleClass("litup");
  window.setTimeout(function() {
    if(col >= 6){
      window.setTimeout(function() {
        rowOn1(0);}, T_int);
    } else {
      colOn3(col+1);
    }
    }, NF_int);}
  
  rowOn1(0);

});

