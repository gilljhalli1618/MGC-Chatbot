let cartCount = 0;

function abc() {
  cartCount++;

  // update the little number badge next to the cart icon
  let badge = document.getElementById("cart-count");
  if (badge) {
    badge.innerText = cartCount;
  }

  alert("Item added to cart! Total items in cart: " + cartCount);
}