// function generates html for each item in order
function generateOrderItems(orderItems) {
    return $.parseHTML(`
        <div class="order-item d-flex justify-content-between">
            <span class="font-weight-bold">${orderItems["name"] }  (Qty:${orderItems["quantity"]})</span>
            <span style="padding-right: 50px" class="text-muted">€${orderItems["price"]}</span>
        </div>
    `)
}

// event listener for checkout button
let checkoutbutton = document.getElementById("checkout-button");
checkoutbutton.addEventListener("click", (event)=>{
    event.preventDefault();

    let card_name = document.getElementById("id_cardholder_name").value;
    let card_num = document.getElementById("id_card_number").value;
    let cvv_num = document.getElementById("id_cvv_number").value;
    let ship_addr = document.getElementById("id_shipping_address").value;

    if (localStorage.token) {
    
        fetch("http://127.0.0.1:8000/orderform/?format=json", { 
            method:'POST', // 
            headers:{// 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + localStorage.token 
        },
        body: JSON.stringify( { cardholder_name:card_name, card_number:card_num, cvv_number:cvv_num, shipping_address:ship_addr })
        }).then(response => response.json()).then(orderData => {
            console.log(orderData)
            let basket = document.getElementById("basket");
            let orderComplete = document.getElementById("order-complete");
            let orderItems = $("#order-items");
            
            if (!("Error" in orderData)) {
                basket.style.display = "none";
                
                $(".order-item").remove(); // remove any old order items before creating new ones
                orderData["order_items"].forEach(orderItem => {
                    orderItems.append(
                    generateOrderItems(orderItem) 
                    );
                });
                
                let totalPrice = document.getElementById("total_order_price")
                totalPrice.innerHTML = `€${orderData["total_price"]}`;

                let orderID = document.getElementById("order-id");
                orderID.innerHTML = `Order No. ${orderData["order_credentials"]["id"]}`;
                
                let cardName = document.getElementById("order-cardholder-name");
                cardName.innerHTML = `Recipient Name: ${orderData["order_credentials"]["cardholder_name"]}`;
                
                let shippingAddress = document.getElementById("order-shipping-address");
                shippingAddress.innerHTML = `Shipping Address: ${orderData["order_credentials"]["shipping_address"]}`;
                
                let dateOrdered = document.getElementById("date-ordered");
                dateOrdered.innerHTML = `Date Ordered: ${orderData["order_credentials"]["date_created"]}`;

                orderComplete.style.display = "block";

            }
            else {
                let orderAlert = document.getElementById("order-alert");
                orderAlert.style.display = "block";
            }
        })
    } 
    else {
        alert("Please log in to continue.");
    }

}, true)
