function revealInformation(element){

    contents   = document.getElementById("contents")
    classList  = Array.from(contents.classList) // stupid JS types...
    downArrow  = '\u{25BC}'
    rightArrow = '\u{25B6}'

    if(classList.includes("hidden")){
        contents.classList = ""
        element.innerText = `Error information ${downArrow}`
    }else{
        contents.classList = "hidden"
        element.innerText =`Error information ${rightArrow}`
    }
}