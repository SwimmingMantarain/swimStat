// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function () {
    modal.style.display = "block";
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, "0");
    var mm = String(today.getMonth() + 1).padStart(2, "0"); //January is 0!
    var yyyy = today.getFullYear();
    var hours = String(today.getHours()).padStart(2, "0");
    var minutes = String(today.getMinutes()).padStart(2, "0");

    today = yyyy + "-" + mm + "-" + dd;
    var time = hours + ":" + minutes;
    document.getElementById("dateInput").value = today;
    document.getElementById("timeInput").value = time;

    block = btn.parentElement;
    session = block.children[5];
    document.getElementById("sessionInput").value = session.id;
}

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}