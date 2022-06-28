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


// function mytransfer(id) {
//   dataform = $("#form" + id).serialize();// JSON.stringify($("#form"+id).serializeArray());
//   $.ajax({
//     url: '/mongo2sql',
//     data: dataform, //$('form').serialize(),
//     type: 'POST',
//     success: function (response) {
//       if (response == '"Cancle"') {
//         // document.getElementById("checked").value = 0;
//         console.log("cancle");
//       } else {
//         // document.getElementById("checked").value = 1;
//         console.log("Good ");
//       }
//     },
//     error: function (error) {
//       console.log(error);
//     }
//   });

// }

function sendmysms(ph, row_number) {
  console.log(ph + "  Status" + row_number + " Row  " + document.getElementById("s" + row_number).value);
  dataform = $("#form" + row_number).serialize();// JSON.stringify($("#form"+id).serializeArray());
  document.getElementById("c" + row_number).style.display = "none";
  document.getElementById("elb" + row_number).style.display = "none";
  document.getElementById("lb" + row_number).style.display = "block";
  document.getElementById("plb" + row_number).style.display = "block";
  phonesms = { "number": document.getElementById("s" + row_number).value };
  $.ajax({
    url: '/sendsms',
    data: phonesms, //$('form').serialize(),
    type: 'POST',
    success: function (response) {
      console.log(response);
      x = JSON.parse(response);
      if (x.status == "DELIVERED") {
        document.getElementById("lb" + row_number).style.display = "none";
        document.getElementById("plb" + row_number).innerHTML = x.text;
        document.getElementById("ulb" + row_number).innerHTML = x.user;
        document.getElementById("tlb" + row_number).innerHTML = x.time;
        console.log("success");
      } else {
        document.getElementById("elb" + row_number).style.display = "block";  // error
        document.getElementById("plb" + row_number).innerHTML = 'เบอร์มือถือไม่สามารถติดต่อได้';
        document.getElementById("ulb" + row_number).innerHTML = x.user;
        document.getElementById("tlb" + row_number).innerHTML = x.time;
        console.log("error");
      }
    },
    error: function (error) {
      console.log(error);
    }
  });

}

function mycheck(id) {
  var el_up = document.getElementById("checked" + id).value;
  dataform = $("#form" + id).serialize();// JSON.stringify($("#form"+id).serializeArray());
  console.log(id + "  Status" + el_up + " ee  " + document.getElementById("checked" + id).value);
  console.log(document.getElementById("checked" + id));
  $.ajax({
    url: '/toggleUpdate',
    data: dataform, //$('form').serialize(),
    type: 'POST',
    success: function (response) {
      if (response == '"Cancle"') {
        dataform
        document.getElementById("checked" + id).value = 0;
        console.log(id + "  cancle" + "   " + response + document.getElementById("checked" + id).value);
      } else {
        document.getElementById("checked" + id).value = 1;
        console.log(id + "  Good " + "   " + response) + document.getElementById("checked" + id).value;
      }
    },
    error: function (error) {
      console.log(error);
    }
  });

}



// function addmissword() {
//   dataform = $("#fmisform").serialize();// JSON.stringify($("#form"+id).serializeArray());
//   $.ajax({
//     url: '/addmissword',
//     data: dataform, //$('form').serialize(),
//     type: 'POST',
//     success: function (response) {
//       if (response == '"add"') {
//         document.getElementById("misword").value = "";
//         document.getElementById("rghword").value = "";
//         console.log("addmissword");
//       }
//     },
//     error: function (error) {
//       console.log(error);
//     }
//   });

// }

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
// findmoblie
function findmoblie() {
  tel_nof = { "tel_no": document.getElementById("tel_nof").value };
  console.log(tel_nof);
  $.ajax({
    url: "/findtel_no",
    data: tel_nof, //$('form').serialize(),
    type: 'POST',
    success: function (response) {
      if (response == '"notfound"') {
        alert("ไม่เบอร์โทรศัพท์นี้ในข้อมูลบริษัท!");
        console.log(response);
      } else if (response == '"wrongID"') {
        alert("หมายเลขเบอร์โทรศัพท์ผิดผลาด!");
        console.log(response);
      } else {
        console.log(response);
        window.location.href = "/mobileinfo";
      }
    },
    error: function (error) {
      console.log(error);
    }
  });

}



// 
// function sendmysmscheck(phoneid) {
//   var phonesms = phoneid
//   // document.getElementById("checked" + id).value;
//   dataform = $("#form" + id).serialize();// JSON.stringify($("#form"+id).serializeArray());
//   console.log(id + "  Status" + phonesms + " ee  " + document.getElementById("checked" + id).value);
//   document.getElementById('smsprocess' + phoneid).style.display = 'block'
//   $.ajax({
//     url: '/sendsms',
//     data: dataform, //$('form').serialize(),
//     type: 'POST',
//     success: function (response) {
//       if (response == '"Cancle"') {
//         dataform
//         document.getElementById("checked" + id).value = 0;
//         console.log(id + "  cancle" + "   " + response + document.getElementById("checked" + id).value);
//       } else {
//         document.getElementById("checked" + id).value = 1;
//         console.log(id + "  Good " + "   " + response) + document.getElementById("checked" + id).value;
//       }
//     },
//     error: function (error) {
//       console.log(error);
//     }
//   });

// }
// 