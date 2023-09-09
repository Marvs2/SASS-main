//--------------------LOG-IN FORM--------------------------------------
const inputs = document.querySelectorAll(".input-field");
const toggle_btn = document.querySelectorAll(".toggle");
const main = document.querySelector("main");
const bullets = document.querySelectorAll(".bullets span");
const images = document.querySelectorAll(".image");

inputs.forEach((inp) => {
  inp.addEventListener("focus", () => {
    inp.classList.add("active");
  });
  inp.addEventListener("blur", () => {
    if (inp.value != "") return;
    inp.classList.remove("active");
  });
});

toggle_btn.forEach((btn) => {
  btn.addEventListener("click", () => {
    main.classList.toggle("sign-up-mode");
  });
});

function moveSlider() {
  let index = this.dataset.value;

  let currentImage = document.querySelector(`.img-${index}`);
  images.forEach((img) => img.classList.remove("show"));
  currentImage.classList.add("show");

  const textSlider = document.querySelector(".text-group");
  textSlider.style.transform = `translateY(${-(index - 1) * 2.2}rem)`;

  bullets.forEach((bull) => bull.classList.remove("active"));
  this.classList.add("active");
}

bullets.forEach((bullet) => {
  bullet.addEventListener("click", moveSlider);
});



//--------------------NAVBAR NAVIGATION--------------------------------------
$(document).ready(function(){
//sub-menu
$(".sub-btn").click(function(){
$(this).next(".sub-menu").slideToggle();
});

// more-menu
$(".more-btn").click(function(){
$(this).next(".more-menu").slideToggle();
});
});

var menu = document.querySelector(".menu");
var menuBtn = document.querySelector(".menu-btn");
var closeBtn = document.querySelector(".close-btn");

menuBtn.addEventListener("click", () => {
menu.classList.add("active");
});

closeBtn.addEventListener("click", () => {
menu.classList.remove("active");
});


window.addEventListener("scroll", function(){
var header = document.querySelector("header");
header.classList.toggle("sticky", window.scrollY > 0);
});


//--------------------SCROLL TO THE TOP--------------------------------------
document.addEventListener("DOMContentLoaded", function () {
const scrollToTopButton = document.getElementById("scrollToTop");

// Show or hide the button based on the scroll position
window.addEventListener("scroll", () => {
if (window.scrollY > 300) {
    scrollToTopButton.style.display = "block";
} else {
    scrollToTopButton.style.display = "none";
}
});

// Smooth scroll to the top when the button is clicked
scrollToTopButton.addEventListener("click", () => {
window.scrollTo({
    top: 0,
    behavior: "smooth",
});
});
});

