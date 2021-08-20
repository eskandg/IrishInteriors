var express = require('express');
var router = express.Router();
const fetch = require("node-fetch");


// 
/* GET home page. */ 
router.get('/', function(req, res, next) { 
fetch("http://127.0.0.1:8000/?format=json") // make a request to this endpoint
.then(response => response.json()) // with our response, get the json data returned
.then(categoryData => {
fetch("http://127.0.0.1:8000/products/?format=json")
.then(response => response.json()) 
.then(productsData => {
fetch("http://127.0.0.1:8000/products/bedroom?format=json")
.then(response => response.json()) 
.then(bedroomData => {
fetch("http://127.0.0.1:8000/products/kitchen?format=json")
.then(response => response.json()) 
.then(kitchenData => {
fetch("http://127.0.0.1:8000/products/dining?format=json")
.then(response => response.json()) 
.then(diningData => {
fetch("http://127.0.0.1:8000/products/bathroom?format=json")
.then(response => response.json()) 
.then(bathroomData => {
fetch("http://127.0.0.1:8000/products/workspace?format=json")
.then(response => response.json()) 
.then(workspaceData => {
fetch("http://127.0.0.1:8000/products/living?format=json")
.then(response => response.json()) 
.then(livingData => {
    res.render('index', { title: 'IrishInteriors', categories: categoryData, products: productsData, bedroomProducts: bedroomData, diningProducts: diningData, kitchenProducts: kitchenData, bathroomProducts: bathroomData, workspaceProducts: workspaceData, livingProducts: livingData });
})
}) 
}) 
}) 
}) 
}) 
}) // 
});
// 
}); 
// 
// 

module.exports = router;
