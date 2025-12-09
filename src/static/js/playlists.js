function fillDescriptions(){

    descriptions = document.getElementsByClassName("description")

    missing_text = "This user hasn't provided a description for this playlist"

    for (let description of descriptions) {
        if(description.textContent.length <= 0){
            description.textContent = missing_text
        }
 
    }
}


function alreadyInList(element,list){

    for (let i = 0; i < list.length; i++) {
        if(list[i] === element){
            return true
        }
    }
    
    return false;
}

function toast(message,seconds) {
  // Get the snackbar DIV
  var x = document.getElementById("snackbar");

  x.innerText = message

  // Add the "show" class to DIV
  x.className = "show";

  // After 3 seconds, remove the show class from DIV
  setTimeout(function(){ x.className = x.className.replace("show", ""); }, seconds * 1000);
}

function grabListItems(id,tag){

    array = []
    list = document.getElementById(id)
    list = list.getElementsByTagName(tag)

    for (let i = 0; i < list.length; i++) {
        array.push(list[i].innerText)
    }

    return array

}

function addToCart(name){

    if(!alreadyInList(name,grabListItems("menu","li"))){
        
        toast(`Added ${name}`,3)

        const newListItem = document.createElement("li");
        const newLink = document.createElement("a");
        const newLabel = document.createElement("label");

        cart = document.getElementById("menu")

        newLabel.innerText = name

        newLink.appendChild(newLabel)
        newListItem.appendChild(newLink)
        cart.appendChild(newListItem)

    }else{
        toast(`${name} is already in the list`,3)
    }

}

function scanPlaylists(){

    // Redirect to route that scans playlists and package list in some data structure to route

}

fillDescriptions()