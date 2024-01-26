document.addEventListener("DOMContentLoaded", function(event) {
   var targetElement = document.getElementById("scroll-target");

   if (targetElement) {
      targetElement.scrollIntoView({ behavior: 'smooth' });
   }
});