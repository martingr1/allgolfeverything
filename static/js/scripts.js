const name = document.getElementById('name')
const email = document.getElementById('email')
const password = document.getElementById('password')
const reg_form = document.getElementById('registration-form')

addEventListener('reg-submit', (e) => {
    if (password.length < 8) {
        flash("Password must be a minimum of 8 characters")
    }


})