const toast = document.querySelector(".toast");
const closeIcon = document.querySelector(".close");
const progress = document.querySelector(".progress");

let timer1, timer2;

// Display toast message on page load
toast.classList.add("active");
progress.classList.add("active");

timer1 = setTimeout(() => {
    toast.classList.remove("active");
}, 3000);

timer2 = setTimeout(() => {
    progress.classList.remove("active");
}, 3300);

closeIcon.addEventListener("click", () => {
    toast.classList.remove("active");

    setTimeout(() => {
        progress.classList.remove("active");
    }, 300);

    clearTimeout(timer1);
    clearTimeout(timer2);
});
