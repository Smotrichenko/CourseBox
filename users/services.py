import requests
from django.conf import settings


def stripe_create_product(name: str, description: str) -> dict:
    """Запрос в Stripe для создания продукта"""

    url = "https://api.stripe.com/v1/products"
    headers = {"Authorization": f"Bearer {settings.STRIPE_SECRET_KEY}"}
    data = {"name": name, "description": description}

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()


def stripe_create_price(product_id: str, amount: int, currency: str) -> dict:
    """Запрос в Stripe для создания цены"""

    url = "https://api.stripe.com/v1/prices"
    headers = {"Authorization": f"Bearer {settings.STRIPE_SECRET_KEY}"}
    data = {
        "unit_amount": amount,
        "currency": currency,
        "product": product_id,
    }

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()


def stripe_create_checkout_session(price_id: str) -> dict:
    """Запрос в Stripe для создания сессии"""

    url = "https://api.stripe.com/v1/checkout/sessions"
    headers = {"Authorization": f"Bearer {settings.STRIPE_SECRET_KEY}"}

    data = {
        "mode": "payment",
        "success_url": settings.STRIPE_SUCCESS_URL,
        "cancel_url": settings.STRIPE_CANCEL_URL,
        "line_items[0][price]": price_id,
        "line_items[0][quantity]": 1,
    }

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()
