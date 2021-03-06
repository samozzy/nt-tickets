// AJAX for posting
function sell_tickets() {
  // console.log("create post is working!") // sanity check before AJAX
  $.ajax({
    url : "sale/", // the endpoint
    type : "POST", // http method
    data : {
      number_member : $('#member').val(),
      number_concession : $('#concession').val(),
      number_public : $('#public').val(),
      number_fringe : $('#fringe').val(),
      number_matinee_freshers : $('#matinee_freshers').val(),
      number_matinee_freshers_nnt : $('#matinee_freshers_nnt').val(),
      number_season : $('#season').val(),
      number_season_sales : $('#season_sales').val(),
      number_season_sales_nnt : $('#season_sales_nnt').val(),
      number_fellow : $('#fellow').val(),
      number_stuff: $('#stuff').val(),
      number_day: $('#day').val(),
      number_day_sales: $('#day_sales').val(),
      number_festival: $('#festival').val(),
      number_festival_sales: $('#festival_sales').val(),
      unique_ticket : $('#unique_ticket').val(),
      reservation: $('#reservation').val(),
      reservation_number: $('#reservation_number').val(),
    }, // data sent with the post request

    // handle a successful response
    success : function(data) {
      // Reset sale form
      $("#sale-form")[0].reset();
      // Update sale overview
      $('#sale-update').html($('#div-1', data).html());
      $('.sale-final').html($('#div-2', data).html());
      $('#reservation_modal_container').html($('#div-3', data).html());
      checkSell(0, parseFloat( ($('#div-4', data).html()) ) );
      // console.log(data);
      // console.log("Sell success"); // sanity check after AJAX
    },

    // handle a non-successful response
    error : function(xhr,errmsg,err) {
      $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
        " <a href='#' class='close'>&times;</a></div>"); // add the error to the DOM
      console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
  });
};

function collect_tickets(id) {
  // console.log('Collect tickets is working')  // Sanity check
  $.ajax({
    url : "reserve/",
    type : "post",
    data : {
      unique_code : $('#code_' + id).val(),
      number : $('#number_' + id).val(),
    },

    // Handle a successful response
    success : function(data) {
      // console.log(data)
      $("#sale-form")[0].reset();
      resetButton();
      
      $('#reservation').val(data.reservation);
      $('#reservation_number').val(data.number);
      $('#unique_ticket').val(data.unique_code);
      // $('#sell_button').prop("disabled", false)
      // console.log('Collect success');  // Sanity check after AJAX
    },

    // Handle and error
    error : function(xhr,errmsg,err) {
      $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
        " <a href='#' class='close'>&times;</a></div>"); // add the error to the DOM
      console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    },
  });
};

function gen_report() {
  // console.log('Collect tickets is working')  // Sanity check
  $.ajax({
    url : "bug/",
    type : "post",
    data : {
      subject : $('#subject').val(),
      message : $('#message').val(),
      name : $('#name').val(),
      label : $(".bug-radio:checked").val(),
      path : $('#path').val(),
    },

    // Handle a successful response
    success : function(data) {
      // console.log(data);
      // console.log('Buggy success');  // Sanity check after AJAX
      if (data.err == false) {
        $('#bug-modal-loader').hide();
        $('#bug-modal-success').show();
        $('#success-path').attr('href', data.content.html_url);
      }
      else {
        $('#bug-modal-loader').hide();
        $('#bug-modal-error').show();
        $('#error-log').html(data.content.message);
      }
    },

    // Handle and error
    error : function(xhr,errmsg,err) {
      $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
        " <a href='#' class='close'>&times;</a></div>"); // add the error to the DOM
      console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    },
  });
};
