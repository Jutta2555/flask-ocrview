// // When the user scrolls the page, execute myFunction
// window.onscroll = function() {myFunction()};

// // Get the header
// var header = document.getElementById("myHeader");

// // Get the offset position of the navbar
// var sticky = header.offsetLeft;

// Add the sticky class to the header when you reach its scroll position. Remove "sticky" when you leave the scroll position
// function myFunction() {
//   if (window.pageYOffset > sticky) {
//     header.classList.add("sticky");
//   } else {
//     header.classList.remove("sticky");
//   }
// }

function mycheck(id) {
    dataform = $("#form"+id).serialize() ;// JSON.stringify($("#form"+id).serializeArray());
    $.ajax({
      url: '/toggleUpdate',
      data: dataform , //$('form').serialize(),
      type: 'POST',
      success: function(response){
        if (response == '"Cancle"') {
          document.getElementById("checked").value=0;
          console.log("cancle");
        } else {
          document.getElementById("checked").value=1;
          console.log("Good ");
        }        
      },
      error: function(error){
        console.log(error);
      }
    });

  }
    
function addmissword() {
dataform = $("#fmisform").serialize() ;// JSON.stringify($("#form"+id).serializeArray());
$.ajax({
    url: '/addmissword',
    data: dataform , //$('form').serialize(),
    type: 'POST',
    success: function(response){
    if (response == '"add"') {
        document.getElementById("misword").value="";
        document.getElementById("rghword").value="";
        console.log("addmissword");
    }        
    },
    error: function(error){
    console.log(error);
    }
});

}

function openForm() {
document.getElementById("misform").style.display = "block";
}

function closeForm() {
document.getElementById("misform").style.display = "none";
}


