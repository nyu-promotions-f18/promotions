$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#promo_id").val(res.id);
        $("#promo_name").val(res.promo_name);
        $("#promo_goods_name").val(res.goods_name);
        $("#promo_price").val(res.price);
        $("#promo_discount").val(res.discount);
        $("#promo_category").val(res.category);
        if (res.available == true) {
            $("#promo_available").val("True");
        } else {
            $("#promo_available").val("False");
        }
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#promo_name").val("");
        $("#promo_goods_name").val("");
        $("#promo_price").val("");
        $("#promo_discount").val("");
        $("#promo_category").val("");
        $("#promo_available").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Promotion
    // ****************************************

    $("#create-btn").click(function () {

        var promo_name = $("#promo_name").val();
        var goods_name = $("#promo_goods_name").val();
        var orig_price = $("#promo_price").val();
        var discount = $("#promo_discount").val();
        var category = $("#promo_category").val();
        var available = $("#promo_available").val() == "true";

        var data = {
            "promo_name": promo_name,
            "goods_name": goods_name,
            "price": orig_price,
            "discount": discount,
            "category": category,
            "available": available
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/promotions",
            contentType:"application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update a Promotion
    // ****************************************

    $("#update-btn").click(function () {

        var promo_id = $("#promo_id").val();
        var promo_name = $("#promo_name").val();
        var goods_name = $("#promo_goods_name").val();
        var orig_price = $("#promo_price").val();
        var discount = $("#promo_discount").val();
        var category = $("#promo_category").val();
        var available = $("#promo_available").val() == "true";

        var data = {
            "promo_name": promo_name,
            "goods_name": goods_name,
            "price": orig_price,
            "discount": discount,
            "category": category,
            "available": available
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/promotions/" + promo_id,
                contentType:"application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve a Promotion
    // ****************************************

    $("#retrieve-btn").click(function () {

        var promo_id = $("#promo_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/promotions/" + promo_id,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete a Promotion
    // ****************************************

    $("#delete-btn").click(function () {

        var promo_id = $("#promo_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/promotions/" + promo_id,
            contentType:"application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Promotion with ID [" + promo_id + "] has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#promo_id").val("");
        clear_form_data()
    });

    // ****************************************
    // Search for a Promotion
    // ****************************************

    $("#search-btn").click(function () {

        var name = $("#promo_name").val();
        var category = $("#promo_category").val();
        var available = $("#promo_available").val() == "True";

        var queryString = ""

        if (name) {
            queryString += 'name=' + name
        }
        if (category) {
            if (queryString.length > 0) {
                queryString += '&category=' + category
            } else {
                queryString += 'category=' + category
            }
        }
        if (available) {
            if (queryString.length > 0) {
                queryString += '&availability=' + available
            } else {
                queryString += 'availability=' + available
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/promotions?" + queryString,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th style="width:10%">ID</th>'
            header += '<th style="width:40%">Name</th>'
            header += '<th style="width:40%">Category</th>'
            header += '<th style="width:10%">Available</th></tr>'
            $("#search_results").append(header);
            for(var i = 0; i < res.length; i++) {
                promotion = res[i];
                var row = "<tr><td>"+promotion.id+"</td><td>"+promotion.promo_name+"</td><td>"+promotion.category+"</td><td>"+promotion.available+"</td></tr>";
                $("#search_results").append(row);
            }

            $("#search_results").append('</table>');

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
