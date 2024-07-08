/* for ADD movie */
var isFirst1 = true;
var isFirst2 = true;
const browseFileHandler = (btn) => {
    console.log(btn)
    const btnParent = btn.closest('.dragger');
    var file = btn.files[0];
    uploadFileHandler(file, btnParent, btn);
}

const dragover = (e, area) => {
    e.preventDefault();
    const dragger_text = area.querySelector('.dragger-text');
    dragger_text.textContent = "Release to upload image";
}

const dragleave = (area) => {
    const dragger_text = area.querySelector('.dragger-text');
    if (dragger_text.id == "ver") dragger_text.textContent = "Drag Image Ratio [3:4]";
    else if (dragger_text.id == "hor") dragger_text.textContent = "Drag Image Ratio [2:1]";
}

const drop = (e, area) => {
    e.preventDefault();
    file = e.dataTransfer.files[0];
    var btn = area.querySelector('#fileSelectorInput');
    uploadFileHandler(file, area, btn);
}

const uploadFileHandler = (file, btnParent, btn) =>{
    if(btnParent.id == "1"){
        if (isFirst1 == true){
            var icon = btnParent.querySelector('.icon');
            var h2 = btnParent.querySelector('h2');
            var h3 = btnParent.querySelector('h3');
            icon.style.display = 'none';
            h2.style.display = 'none';
            h3.style.display = 'none';
            isFirst1 = false;
        }
        else{
            btnParent.removeChild(btnParent.firstElementChild);
        }
        btn.file = file
        console.log(btn.file, btn) 
    }
    else if(btnParent.id == "2"){
        if (isFirst2 == true){
            var icon = btnParent.querySelector('.icon');
            var h2 = btnParent.querySelector('h2');
            var h3 = btnParent.querySelector('h3');
            icon.style.display = 'none';
            h2.style.display = 'none';
            h3.style.display = 'none';
            isFirst2 = false;
        }
        else{
            btnParent.removeChild(btnParent.firstElementChild);
        }
        btn.file = file
        console.log(btn.file, btn)
    }
    const fileReader = new FileReader();

    fileReader.onload = () => {
        
        const fileURL = fileReader.result;
        var imageTag = document.createElement("img");
        imageTag.setAttribute("src", fileURL);

        if(btnParent.id == "1") imageTag.style.width = "50%";
        else if(btnParent.id == "2") imageTag.style.width = "90%";

        btnParent.prepend(imageTag);
    }
    fileReader.readAsDataURL(file);
}

/* for mode button*/
const toggleFunc = (btn) => {
    const addbutton = document.querySelector("#addbutton");
    const deletebutton = document.querySelector("#deletebutton");
    
    const addMovie = document.querySelector(".input-box");
    const deleteMovie = document.querySelector(".delete-box");

    if (btn.id == "addbutton"){
        addMovie.style.display = "flex";
        deleteMovie.style.display = "none";
        deletebutton.style.backgroundColor = "#c5c5c5";
    }
    else if(btn.id == "deletebutton"){
        addMovie.style.display = "none";
        deleteMovie.style.display = "block";
        addbutton.style.backgroundColor = "#c5c5c5";
    }
    btn.style.backgroundColor = "#ffc632";
}

/* for pop up window  */
const confirm = () => {
    pop_up = document.querySelector(".pop-up");
    console.log('clicked');
    pop_up.style.display = "flex";
}

const cancel = () => {
    pop_up = document.querySelector(".pop-up");
    pop_up.style.display = "none";
}