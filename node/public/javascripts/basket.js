// Hides alert
let addedToBasketAlert = $(".product_added_notification"); 
$(".product_added_notification").hide();

// function to add product to basket
function addtoBasket(productId){
    if (localStorage.token) {
    fetch("http://127.0.0.1:8000/addbasket/" + productId + "?format=json", {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': 'Token ' + localStorage.token 
    }
    }).then(response => response.json()).then(data => {
        console.log(data)
        $(".product_added_notification").css("display", "block");
    })

    }
    else {
        alert("Please log in to continue")
    }
} 

// function generates html for 
function generateBasketItem(product, lastLine) {
    let hr = `<hr style="height: 5px; width: 100%;"/>`
    if (lastLine == true)
        hr = ``

    return $.parseHTML(`
        <div class="product" style="display: contents;">
            <!-- product name -->
            <div class="col-xl-3 col-md-4 mb-auto" style="line-height: 20px;">
                <a id="productName" class="lead font-weight-normal text-md-center text-lg-center text-xl-center text-nowrap text-info" href="#">
                    ${product['name']}
                </a>
            </div>

            <!-- product category -->
            <div class="col-xl-3 col-md-2 mb-auto">
                <p class="mt-0 small text-nowrap text-md-center text-lg-center text-xl-center text-muted font-weight-light">${product['category']}</p>
            </div>
            
            <!-- product quantity -->
            <div class="col-xl-3 col-md-2 mb-auto">
                <p id="productQuantity" class="mt-0 text-nowrap text-md-center text-lg-center text-xl-center small lead">
                    Qty. ${product['quantity']}
                </p>
            </div>
            
            <!-- product price -->
            <div class="col-xl-3 col-md-4 mb-auto">
                <div id="productPrice" class="text-nowrap text-md-center text-lg-center text-xl-center">
                    €${product['price']}
                </div>
            </div>
        ${hr}
        </div>

    `);
}

// event listener to basket button in navbar
let basketButton = document.getElementById("contentID-basket")
basketButton.addEventListener("click", (async event => {
event.preventDefault();
fetch("http://localhost:8000/basket/?format=json",{ // 
    method: 'GET',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Token ' + localStorage.token 
    } 
    
    }).then(response => response.json().then(parsed => {
        let basketSize = parseInt(parsed["size"]);
        let summary = document.getElementById("order-summary");
        let paymentForm = document.getElementById("payment-form");
        let emptyBasket = document.getElementById("empty-basket");
        let orderAlert = document.getElementById("order-alert");

        orderAlert.style.display = "none";
        summary.style.display = "";
        paymentForm.style.display = "";
        emptyBasket.style.display = "none";
        if (basketSize != 0) {
            $(".product").remove(); // remove any existing html for basket items
        
            let lastLine = false;
            let basketItems = $("#basket-items");
            let subtotal = document.getElementById("subtotal");
            let total = document.getElementById("total-price");
            let totalPrice = parseFloat(parsed["total_price"]);

            total.innerHTML = "€" + (totalPrice + 8).toString();
            subtotal.innerHTML = `€${totalPrice}`;

            for (let i = 0; i < parsed["items"].length; i++) {
            
                if (i + 1 == parsed["items"].length)
                    lastLine = true;

                basketItems.append(
                    generateBasketItem(parsed["items"][i], lastLine)
                );
            }
        }
        else {                
            emptyBasket.style.display = "block";
            summary.style.display = "none";
            paymentForm.style.display = "none";
        }
        

    }
    )
)
}))
