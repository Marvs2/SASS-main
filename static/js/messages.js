
const toast = document.querySelector(".toast");
const closeIcon = document.querySelector(".close");
const toastprogress = document.querySelector(".progress"); // Fix variable name

let timer1, timer2;

// Display toast message on page load
toast.classList.add("active");
toastprogress.classList.add("active"); // Fix variable name

timer1 = setTimeout(() => {
    toast.classList.remove("active");
}, 3000);

timer2 = setTimeout(() => {
    toastprogress.classList.remove("active"); // Fix variable name
}, 3300);

closeIcon.addEventListener("click", () => {
    toast.classList.remove("active");

    setTimeout(() => {
        toastprogress.classList.remove("active"); // Fix variable name
    }, 300);

    clearTimeout(timer1);
    clearTimeout(timer2);
});
