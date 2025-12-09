function fillDescriptions(){

    descriptions = document.getElementsByClassName("description")

    missing_text = "This user hasn't provided a description for this playlist"

    for (let description of descriptions) {
        if(description.textContent.length <= 0){
            description.textContent = missing_text
        }
 
    }
}

fillDescriptions()


function addToCart(name){

    const newListItem = document.createElement("li");
    const newLink = document.createElement("a");
    const newLabel = document.createElement("label");

    cart = document.getElementById("menu")

    newLabel.innerText = name

    newLink.appendChild(newLabel)
    newListItem.appendChild(newLink)
    cart.appendChild(newListItem)

}