### Welcome to Bhub Customer API Challenge

Please check the following links to understand *OpenAPI* specifications:
* [OpenAPI Specification](https://swagger.io/specification/)
* [DRF Spectacular](https://github.com/tfranzel/drf-spectacular)

---

### Authentication
On this page, you're already authenticated. For API access you need to authenticate passing the development Authorization header:

```
Authorization: Api-Key 1234-ABCDE
```

---

### API Workflow

1. Make a POST to `/api/customers`. You will get the CustomerId (`id`).
2. With CustomerId, make a POST to `/api/customers/<id>/address`.
3. With CustomerId, make a POST to `/api/customers/<id>/account`.

<details>
<summary>>> Click to see some example payloads</summary>

#### Create Customer
```json
{
  "tax_id": "834.485.901-85",
  "first_name": "Seu",
  "last_name": "Madruga",
  "gender": "MALE",
  "personal_pronoums": [
    "Ele", "Seu"
  ],
  "declared_income": 2000.00,
  "declared_income_currency": "BRL",
  "email": "ramon@hotmail.com",
  "cell_phone": "+5511 99999-9999"
}
```

#### Create Customer Account
```json
{
  "bank": {
    "code": "341",
    "name": "ITAÚ"
  },
  "payment_type": "BANK_TRANSFER",
  "bank_branch": "1234",
  "bank_account": "12345-6"
}
```


#### Create Customer Address
```json
{
  "address": {
    "street": "Avenida Riomar Tapajós Virgulino Lages",
    "district": "Do Bom Remédio",
    "city": "Itaituba",
    "state": "PA",
    "country": "BR",
    "zip_code": "68180-650"
  },
  "address_type": "BILLING",
  "address_number": "465",
  "address_complement": "atrás da padaria"
}
```

</details>

[![](https://mermaid.ink/img/pako:eNqtkcFqAjEQhl8lzLG4BDzmIBQrvQiKemtKGZKpBt2NJBNBln1308aF3bYHD53TMHz_9x-mBeMtgYLIyPTicB-wri5T3Yg8b0_voqpmYukiz1NkX1OISrwudkLi2UnT3wo-wr6D80BZ29-UWK-2j0Y3xMHRZRD-XStbZ7siGDcNyp-tDRTjn92y7dePLJJY0CL82f8PylF66DPGp4Yf8hUUJpAvNTqbX9d-2TXwgWrSoPJqMRw16KbLXDrbXLGwjn0A9YmnSBPAxH57bQwoDol66P7-O9XdAE9tvNQ)](https://mermaid.live/edit#pako:eNqtkcFqAjEQhl8lzLG4BDzmIBQrvQiKemtKGZKpBt2NJBNBln1308aF3bYHD53TMHz_9x-mBeMtgYLIyPTicB-wri5T3Yg8b0_voqpmYukiz1NkX1OISrwudkLi2UnT3wo-wr6D80BZ29-UWK-2j0Y3xMHRZRD-XStbZ7siGDcNyp-tDRTjn92y7dePLJJY0CL82f8PylF66DPGp4Yf8hUUJpAvNTqbX9d-2TXwgWrSoPJqMRw16KbLXDrbXLGwjn0A9YmnSBPAxH57bQwoDol66P7-O9XdAE9tvNQ)

### Changelog
<details>
<summary><b>Click to open changelog</b></summary>

#### 2022.06.10 - Initial version
</details>

---
