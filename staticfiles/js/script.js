// updateQuantity (productId,operation) + and - for the product quantity
//the quantity should not no negative

function updateQuantity(productId,operation){
 const inputBox = document.getElementById('quantity'+productId)
 inputBox.value =parseInt(inputBox.value)+operation;
 if(inputBox.value<1){
    inputBox.value=1;
  }
  
}

