function fillDescriptions(){

    descriptions = document.getElementsByClassName("description")

    missing_text = "This user hasn't provided a description for this playlist"

    for (let description of descriptions) {
        if(description.textContent.length <= 0){
            description.textContent = missing_text
        }
 
    }
}

function alreadyInList(element,list,removal=""){

    for (let i = 0; i < list.length; i++) {
        tempVar = list[i]

        if(removal.length >=1){
            tempVar = tempVar.replace(removal,"")
        }
        
        if(tempVar === element){
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

function constrainString(string,limit=5){

    splitAt = (index, xs) => [xs.slice(0, index), xs.slice(index)] // very cool and useful thank you https://stackoverflow.com/questions/16441770/insert-character-into-string-at-index

    if(string.length >= limit){
        return splitAt(limit,string)[0] + "..."
    }
    return string
}

function addToCart(name,id){

    const CHAR_CONSTRAINT = 10
    prevName = name
    name = constrainString(name,CHAR_CONSTRAINT)

    if(!alreadyInList(name,grabListItems("menu","li"),"\nX")){
        
        toast(`Added ${prevName}`,3)

        const newListItem    = document.createElement("li")

        const playListItem   = document.createElement("div")
        const removalItem    = document.createElement("div")

        const newPlayList    = document.createElement("label")
        const newRemovalText = document.createElement("label")

        newRemovalText.classList = "remove"
        playListItem.classList   = "listItem"
        removalItem.classList    = "listItem"

        cart = document.getElementById("menu")

        newRemovalText.innerText = "X"
        newPlayList.innerText    = constrainString(name,CHAR_CONSTRAINT)

        playListItem.appendChild(newPlayList)
        removalItem.appendChild(newRemovalText)

        newListItem.appendChild(playListItem)
        newListItem.appendChild(removalItem)

        newListItem.setAttribute("id",id)
        newListItem.setAttribute("name",prevName) // hacky way to allow actual names through

        cart.appendChild(newListItem)

    }else{
        toast(`${name} is already in the list`,3)
    }

}

function scanPlaylists(){

    // Redirect to route that scans playlists and package list in some data structure to route

    list = document.getElementById("menu")
    list = list.getElementsByTagName("li")

    for (let item of list) {
        console.log(item.getAttribute("name"))
    }
}

fillDescriptions()