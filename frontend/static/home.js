var bigTitle = document.querySelectorAll('#big-title');
for(var i = 0; i < bigTitle.length; i++){
    var bigTitleWidth = bigTitle[i].clientWidth;
    var bigTitleWidth2 = bigTitle[i].scrollWidth;
    if(bigTitleWidth2 > bigTitleWidth){
        bigTitle[i].style.fontSize = bigTitleWidth / bigTitleWidth2 * 2.8 + 'rem';
    }
}