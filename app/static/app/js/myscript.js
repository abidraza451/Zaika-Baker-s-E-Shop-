

$('.plus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml =this.parentNode.children[2]
    console.log("pid =",id)
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data: {
            prod_id:id
        },
        success:function(data){
            console.log("data =",data);
            eml.innerText = data.quantity
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
        }
    })
})

$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this.parentNode.children[2];
    console.log("pid =", id);
    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id
        },
        success: function(data){
            console.log("data=", data);
            eml.innerText = data.quantity;
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;

            // Check if reload_page flag is set, then reload the page
            if (data.reload_page) {
                window.location.reload();
            }
        }
    });
});


$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this;
    $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
            prod_id: id
        },
        success: function(data) {
            document.getElementById("amount").innerText = data.amount;
            document.getElementById("totalamount").innerText = data.totalamount;
            eml.parentNode.parentNode.parentNode.parentNode.remove();
            location.reload(); // Reload the page
        }
    });
});


$('.plus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/pluswishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            window.location.href=`http://localhost:8000/category-detail/${id}`
        }
    })
})

$('.minus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/minuswishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            window.location.href=`http://localhost:8000/category-detail/${id}`
        }
    })
})


$('.remove-wish').click(function(){
    var id = $(this).attr("pid").toString();
    var eml = this;
    $.ajax({
        type: "GET",
        url: "/removewish",
        data: {
            prod_id: id
        },
        success: function(data) {
            eml.parentNode.parentNode.parentNode.parentNode.remove();
            location.reload(); // Reload the page
        }
    });
});



