let bottone = document.getElementById("accedi")
bottone.addEventListener("click", login)
function login (e) {
    e.preventDefault()
    let username = document.getElementById("username")
    console.log(username.value)
    let password = document.getElementById("password")
    console.log(password.value)
}