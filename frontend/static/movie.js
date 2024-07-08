// javascript for comment's area
var field = document.querySelector('textarea');
var backUp = field.getAttribute('placeholder');
var clearBtn = document.getElementById('clear-button');

field.onfocus = function(){
  this.setAttribute('placeholder', '');
}

field.onblur = function(){
  this.setAttribute('placeholder', backUp);
}
function myFunc(){
  field.value = '';
}

let submit = document.querySelector('input[name="submit"]');
submit.addEventListener("click", Submit);
let loadMoreBtn = document.querySelector('#see-more');
loadMoreBtn.addEventListener("click", LoadMore);
let currentItem = 3;
let boxes = [...document.querySelectorAll('.comments-container .comment')];

const article = document.querySelector("#movie_id");
var movie_id = article.dataset.movieid;

var bar_percentage = document.querySelectorAll('.bar-percentage');
for(i = 0; i < bar_percentage.length; i++){
  var percentage = bar_percentage[i].getAttribute('value');
  var num = percentage.toString() + '%';
  bar_percentage[i].style.width = num;
}

function Submit(){
  var comment = document.getElementById("comment-box").value;
  var rating = document.querySelector('input[name="rate"]:checked').value;
  fetch('/comment/' + movie_id, {
    headers : {
      'Content-Type' : 'application/json'
    },
    method : 'POST',
    body : JSON.stringify( {
      'rating' : rating,
      'comment' : comment
    })
  });
};

function LoadMore(){
  var isFull = false;
  var i = currentItem;

  for (i = currentItem; i < currentItem + 3 && i < boxes.length; i++){
    boxes[i].style.display = 'block';
  }
  
  if (currentItem + 3 < boxes.length) {currentItem += 3;}
  else {currentItem = boxes.length}

  if(i >= boxes.length){
    loadMoreBtn.innerHTML = 'Nothing else~';
    loadMoreBtn.style.cursor = 'context-menu';
    loadMoreBtn.addEventListener("mouseover", mouseOver);
    function mouseOver(){
      loadMoreBtn.style.color = '#fff';
    }
  }
}

//javascript for like and dislike button
let upvote = document.querySelectorAll("#upvote");
let downvote = document.querySelectorAll("#downvote");
for(var i = 0; i < upvote.length; i++){
  if(upvote[i].getAttribute('state') == 1) upvote[i].style.backgroundColor = "#ffc632";
  if(downvote[i].getAttribute('state') == 1) downvote[i].style.backgroundColor = "#ffc632";
}


function Vote(btn){
  var like_dislike = btn.closest(".like-button");
  var quant = like_dislike.querySelector("p");
  var upvote = like_dislike.querySelector("#upvote");
  var downvote = like_dislike.querySelector("#downvote");
  var state = btn.getAttribute('state');
  var value = btn.value;
  var id = btn.id;
  let x = parseInt(quant.innerHTML, 10);

  if(state == 0){
    let others;
    if(id == "upvote") {
      x++;
      value = 1;
      others = downvote;
    }
    else if (id == "downvote") {
      x--;
      value = -1;
      others = upvote;
    }
    if(others.getAttribute('state') == 1){
      if(others.id == "upvote"){
        x--;
        value = -2;
      } 
      else if(others.id == "downvote"){
        x++;
        value = 2;
      } 
      others.setAttribute('state', 0);
      others.value= 0;
      others.style.backgroundColor = "#fff";
    }
    quant.innerHTML = x.toString();
    btn.setAttribute('state', 1);
    btn.style.backgroundColor = "#ffc632";
  }
  
  else if(state == 1){
    if(id == "upvote") {
      x--;
    }
    else if (id == "downvote"){
      x++;
    } 
    value = 0;
    quant.innerHTML = x.toString();
    btn.setAttribute('state', 0);
    btn.style.backgroundColor = "#fff";
  }
  fetch('/vote', {
    headers : {
      'Content-Type' : 'application/json'
    },
    method : 'POST',
    body : JSON.stringify( {
      'review_id' : btn.getAttribute('data-review_id'),
      'vote' : value,
      'movie_id' : movie_id
    })
  });
}