window.addEventListener("DOMContentLoaded", () => {
  document.getElementById("c-header__open-sidebar-button").addEventListener("click", () => {
    const sidebar = document.getElementById("c-sidebar");
    sidebar.classList.toggle("c-sidebar--isHidden");
  });

  document.getElementById("c-sidebar__close-sidebar-button").addEventListener("click", () => {
    const sidebar = document.getElementById("c-sidebar");
    sidebar.classList.toggle("c-sidebar--isHidden");
  });


  document.body.onload = async () => {
    productsContainer = document.getElementById("p-cart__products")

    if (!productsContainer) return;

    const cart = JSON.parse(localStorage.getItem("cart")) ?? { items: [] };

    data = JSON.stringify({
      productIds: cart.items.map(i => i.id)
    })

    let response = await fetch("/get-produtos/", {
      method: 'POST',
      body: data,
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        "X-CSRFToken": csrftoken
      },
    })

    const json = await response.json()

    let index = -1
    for (const item of json.products) {
      index++;
      const amount = cart.items.find(i => i.id == item.id).amount
      const element = document.createElement("div")
      element.className = "c-cart-card"
      element.innerHTML = `
      <div class="c-cart-card__main-info">
        <img src="${item.imageUrl}" class="c-cart-card__img"/>
        <div class="c-cart-card__info">
          <div>
            <span class="c-cart-card__name">${item.name}</span>
            <span class="c-cart-card__value">R$ ${Math.round(item.value * (1 - item.discount) * 100) / 100} x ${amount}</span>
          </div>
        </div>
      </div>
      <div class="c-cart-card__footer">
        <button onclick="removeFromCart(${item.id})" type="button"><i class="fa-solid fa-trash fa-xl"></i></button>
        <span>R$ ${Math.round((item.value * (1 - item.discount)) * amount * 100) / 100}</span>
      </div>
      `
      productsContainer.append(element)
    }

    if (json.products.length == 0) {
      productsContainer.append("Nenhum produto no carrinho.")
    }
  }
});

function addToCart(id, amount) {
  if (!id) return;

  const cart = JSON.parse(localStorage.getItem("cart")) ?? { items: [] };

  if (!cart.items) {
    cart = {
      items: []
    }
  }

  cart.items = cart.items.filter((i) => i.id != id)

  cart.items.push({
    id: id,
    amount: amount ?? 1
  })

  localStorage.setItem("cart", JSON.stringify(cart))

  location.href = "/carrinho"
}

function removeFromCart(id) {
  const cart = JSON.parse(localStorage.getItem("cart")) ?? { items: [] };

  if (!cart.items) {
    cart = {
      items: []
    }
  }

  cart.items = cart.items.filter((i) => i.id != id)

  localStorage.setItem("cart", JSON.stringify(cart))

  location.href = "/carrinho"
}