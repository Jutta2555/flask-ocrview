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


// var interval = setInterval(update_progress, 1000);
// function update_progress() {
//   $.get('/progress').done(function (n) {
//     n = n / 5;  // percent value
//     if (n == 100) {
//       clearInterval(interval);
//       callback(); // user defined
//     }
//     $('.progress-bar').animate({ 'width': n + '%' }).attr('aria-valuenow', n);
//   }).fail(function () {
//     clearInterval(interval);
//     displayerror(); // user defined
//   });
// }


function mytransfer(id) {
  dataform = $("#form" + id).serialize();// JSON.stringify($("#form"+id).serializeArray());
  $.ajax({
    url: '/mongo2sql',
    data: dataform, //$('form').serialize(),
    type: 'POST',
    success: function (response) {
      if (response == '"Cancle"') {
        // document.getElementById("checked").value = 0;
        console.log("cancle");
      } else {
        // document.getElementById("checked").value = 1;
        console.log("Good ");
      }
    },
    error: function (error) {
      console.log(error);
    }
  });

}

function mycheck(id) {
  dataform = $("#form" + id).serialize();// JSON.stringify($("#form"+id).serializeArray());
  $.ajax({
    url: '/toggleUpdate',
    data: dataform, //$('form').serialize(),
    type: 'POST',
    success: function (response) {
      if (response == '"Cancle"') {
        document.getElementById("checked").value = 0;
        console.log("cancle");
      } else {
        document.getElementById("checked").value = 1;
        console.log("Good ");
      }
    },
    error: function (error) {
      console.log(error);
    }
  });

}

function addmissword() {
  dataform = $("#fmisform").serialize();// JSON.stringify($("#form"+id).serializeArray());
  $.ajax({
    url: '/addmissword',
    data: dataform, //$('form').serialize(),
    type: 'POST',
    success: function (response) {
      if (response == '"add"') {
        document.getElementById("misword").value = "";
        document.getElementById("rghword").value = "";
        console.log("addmissword");
      }
    },
    error: function (error) {
      console.log(error);
    }
  });

}

function findidcard() {
  idcardf = { "idcard": document.getElementById("findid").value };
  $.ajax({
    url: "/findidcard",
    data: idcardf, //$('form').serialize(),
    type: 'POST',
    success: function (response) {
      if (response == '"notfound"') {
        alert("ไม่พบบัตรปปช!");
        console.log(response);
      } else if (response == '"wrongID"') {
        alert("หมายเลขไอดีผิดผลาด!");
        console.log(response);
      } else {
        console.log(response);
        window.location.href = "/idcard/" + response;
      }
    },
    error: function (error) {
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


