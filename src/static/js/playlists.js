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