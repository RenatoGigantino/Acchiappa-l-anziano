let bottone = document.getElementById("registrati")
bottone.addEventListener("click", register)
function register (e) {
    e.preventDefault()
    let username = document.getElementById("username")
    console.log(username.value)
}