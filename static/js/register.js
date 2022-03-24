// console.log("register working")
const usernameField = document.querySelector("#usernameField");
const usernameFeedBackArea = document.querySelector(".usernameFeedBackArea");
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const emailField = document.querySelector("#emailField");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
const emailSuccessOutput = document.querySelector(".emailSuccessOutput");
const passwordField = document.querySelector("#passwordField");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const submitBtn = document.querySelector(".submitBtn");

const handleToggleInput = (e) => {
  if (showPasswordToggle.textContent === "SHOW") {
    showPasswordToggle.textContent = "HIDE";
    passwordField.setAttribute("type", "text");
  } else {
    showPasswordToggle.textContent = "SHOW";
    passwordField.setAttribute("type", "password");
  }
};


showPasswordToggle.addEventListener("click", handleToggleInput);

emailField.addEventListener("keyup", (e) => {
  const emailVal = e.target.value;
  console.log("emalField", emailVal);
  if (emailVal === "") {
    emailSuccessOutput.style.display = "none";
  } else {
    emailSuccessOutput.style.display = "block";

    emailSuccessOutput.textContent = `Checking ${emailVal}`;
    // console.log("emailVal", emailVal)
    emailField.classList.remove("is-invalid");
    emailFeedBackArea.style.display = "none";

    if (emailVal.length > 0) {
      fetch("/authentication/validate-email", {
        body: JSON.stringify({ email: emailVal }),
        method: "POST",
      })
        .then((res) => res.json())
        .then((data) => {
          console.log("data", data);
          emailSuccessOutput.style.display = "none";
          if (data.email_error || emailVal==="") {
            // submitBtn.setAttribute('disabled', "disabled")
            submitBtn.disabled = true;
            emailField.classList.add("is-invalid");
            emailFeedBackArea.style.display = "block";
            emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
          } else{
            submitBtn.removeAttribute("disabled")
          }
        });
    }
  }
});

usernameField.addEventListener("keyup", (e) => { 
  const usernameVal = e.target.value;
  if (usernameVal === "") {
    usernameSuccessOutput.style.display = "none";
  } else {
    usernameSuccessOutput.style.display = "block";

    usernameSuccessOutput.textContent = `Checking ${usernameVal}`;

    // console.log("usernameVal", usernameVal)
    usernameField.classList.remove("is-invalid");
    usernameFeedBackArea.style.display = "none";

    if (usernameVal.length > 0) {
      fetch("/authentication/validate-username", {
        body: JSON.stringify({ username: usernameVal }),
        method: "POST",
      })
        .then((res) => res.json())
        .then((data) => {
          console.log("data", data);
          usernameSuccessOutput.style.display = "none";
          if (data.username_error) {
            console.log("dis")
            usernameField.classList.add("is-invalid");
            usernameFeedBackArea.style.display = "block";
            usernameFeedBackArea.innerHTML = `<p>${data.username_error}</p>`;
            submitBtn.disabled = true;
          } else {
            submitBtn.removeAttribute("disabled");
          }
        });
    }
  }
});
