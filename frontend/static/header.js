function dropButton(btn){
    var caret = btn.querySelector(".caret");
    var dropdowncontent = document.querySelector(".dropdown-content");
    if(btn.value == "hide"){
        dropdowncontent.style.display = "inline-block";
        btn.value = "active";
        caret.style.transform = 'rotate(180deg)';
        caret.style.transition = '0.3s';
    }
    else if(btn.value == "active"){
        dropdowncontent.style.display = "none";
        btn.value = "hide";
        caret.style.transform = 'rotate(0deg)';
        caret.style.transition = '0.3s';
    }
}

function selectOption(btn){
    var value = btn.innerHTML;
    var defaultbutton = document.querySelector(".dropbtn");
    var dropdowncontent = document.querySelector(".dropdown-content");
    var text = defaultbutton.querySelector('p');
    var caret = defaultbutton.querySelector(".caret");
    text.innerHTML = value;
    defaultbutton.value = "hide";
    dropdowncontent.style.display = "none";
    caret.style.transform = 'rotate(0deg)';
    caret.style.transition = '0.3s';
    $('ul.dropdown-content').on('click', 'li.All', function(event) {
        $.ajax({
            url : '/filter',
            type : "post",
            contentType: 'application/json;charset=UTF-8',
            dataType: "json",
            data : JSON.stringify({
                "filter" : "All"
            })
        });
        event.preventDefault();
    });
    $('ul.dropdown-content').on('click', 'li.Title', function(event) {
        $.ajax({
            url : '/filter',
            type : "post",
            contentType: 'application/json;charset=UTF-8',
            dataType: "json",
            data : JSON.stringify({
                "filter" : "Title"
            })
        });
        event.preventDefault();
    });
    $('ul.dropdown-content').on('click', 'li.Actors', function(event) {
        $.ajax({
            url : '/filter',
            type : "post",
            contentType: 'application/json;charset=UTF-8',
            dataType: "json",
            data : JSON.stringify({
                "filter" : "Actors"
            })
        });
        event.preventDefault();
    });
    $('ul.dropdown-content').on('click', 'li.Year',function(event) {
        $.ajax({
            url : '/filter',
            type : "post",
            contentType: 'application/json;charset=UTF-8',
            dataType: "json",
            data : JSON.stringify({
                "filter" : "Year"
            })
        });
        event.preventDefault();
    });
    $('ul.dropdown-content').on('click', 'li.Genre', function(event) {
        $.ajax({
            url : '/filter',
            type : "post",
            contentType: 'application/json;charset=UTF-8',
            dataType: "json",
            data : JSON.stringify({
                "filter" : "Genre"
            })
        });
        event.preventDefault();
    });
}

function submitSearch(){
    document.getElementById("searchbar").submit();
}