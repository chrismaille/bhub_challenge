Main Story: [FTINSU-33](https://facily-jira.atlassian.net/browse/FTINSU-33)

### Authentication
You need to pass a valid `access_token` in the `Authorization` header, which you can obtain:

---

### Mobile Endpoints

<details>
<summary><b>Click to see instructions for Mobile endpoints.</b></summary>

From [Facily Core Commerce User Identity API](https://core-commerce-user-identity.staging.faci.ly/docs#/Users%20V2/sign_in_v2_users_signin_post),
passing the `email` and `password` of the user you want to authenticate:

Get access token in Facily Core Commerce User Identity API, passing the Bearer token
which you can find here: [https://facily-jira.atlassian.net/browse/FTINSU-124](https://facily-jira.atlassian.net/browse/FTINSU-124)

```bash
$ curl -X 'POST' \
  'https://core-commerce-user-identity.staging.faci.ly/v2/users/signin' \
  -H 'accept: application/json' \
  -H 'access_token: Bearer <<GET BEARER IN JIRA TASK FTINSU-124>>' \
  -H 'Content-Type: application/json' \
  -d '{
  "key": "segurosteste@email.com",
  "password": "super_senha_secreta"
}'
```
Then use the `access_token` received to access any Acquisition Mobile Endpoints:

```bash
$ curl -H "Authorization: Bearer <access_token> https://fintech-insurance-acquisition.development.faci.ly/api/quotes/me
```
</details>

---

### Backoffice Endpoints

<details>
<summary><b>Click to see instructions for Backoffice endpoints.</b></summary>

From [Backoffice Admin API](https://finance-admin-api.development.faci.ly/docs/static/index.html#/),
passing the `CF_Authorization` value inside the cookie saved on your Browser, after you open Swagger:

```bash
$ curl -X 'POST' \
  'https://finance-admin-api.development.faci.ly/login' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "cfAccessToken": "<<ADD HERE THE CF_Authorization FROM SWAGGER COOKIE>>"
}'
```

Then use the `access_token` received to access any Acquisition Mobile Endpoints:

```bash
$ curl -H "Authorization: Bearer <access_token> https://fintech-insurance-acquisition.development.faci.ly/api/quotes/me
```
</details>

---

### Using the "Try it Out" button
If you already have a JWT Token generated in the authentication systems you can use the
`Try It Out` button, clicking on `Authorize` button and pass your access token:
`Bearer <access_token>`:

<details>
<summary>Click to see button in action.</summary>

<img src="static/docs/8e979d56.gif"/>

</details>

_**In local environment only**_, you can use the form below to generate a JWT Token:
on **username** pass your WordPress Id and put any value on **password**:

<details>
<summary>Click to see form in action.</summary>

<img src="static/docs/08612100.gif"/>

</details>

---

### Current Use:

1. **GET** `/partners/active-products/me` to get the list of active products for the
   current user.
2. **GET** `/quotes/me` endpoint to get the current Quote for a logged user (or
   Lead). If Lead was just created (automatically by Backend) this endpoint will
   return 404.
3. **POST** `/quotes/me/new` for create Lead's new Quote.
4. **POST** occupation and personal data required in  `/quotes/me/analysis` to
   approve or deny Quote.
5. **POST** complete personal data at `/leads/me/personal-data`.
6. **POST** complete address at `/quotes/me/address`.
7. **POST** Lead accept terms and conditions to `/quotes/me/accept`.
8. **GET** Payment External Link at `/quotes/me/payment` or `/quotes/me` or wait
   for OneSignal notification with this data.
9. **GET** Lead history for Quotes at `/quotes/me/history`.

Each **POST** endpoint has his own **GET** method to retrieve the same data.

---

### Changelog
<details>
<summary><b>Click to open changelog</b></summary>

#### 2022.04.12 - v1.1

* On local environment add the option to generate a JWT Token.
* Fix error when user uses the JWT token from `meryto` authentication system.
* Swagger is now in `/docs` endpoint. Example: `https://fintech-insurance-acquisition.development.faci.ly/docs`.
  The older endpoints will redirect to here.

#### 2022.04.08 - v1.0

From this point API is now versioned: the latest version will be always
`/api/latest/<endpoint>` - for example `/api/latest/quotes/me`.

##### Other changes

* Rename endpoint `partners/me/active-products/schemas` to
  `/partners/active-products/me/schema/`.
* Removed `/quotes/me/product` endpoint.
* Removed `/quotes/me/occupation` endpoint.
* Rollback `/quotes/me/payment` GET endpoint.
* Add fields `status`, `external_payment_link` and `external_payment_link_valid_through`
  to `/quotes/me/payment` GET endpoint.
* Remove `pep` field in Lead Response
* Add `facily_wordpress_id` field in Lead Response
* Add `partner_quote_id` field in Product Response

----

#### 2022.04.01 - New additions per mobile team requests:

* Revert `product` changes in `/quotes/me` endpoint.
* All datetime fields are now returned as `ISO 8601` format: `2020-01-01T00:00:00.000Z`.
* Add the `product_payment_method` field to `/quotes/me` endpoint. This field means the
  payment method "chosen" by user. (In fact, it is selected in backend automaticaly, like
  product, because currently, we have just only one partner/product/payment_method combo).
* Add missing fields in `/quotes/me` endpoint:

| Field                            | Type     | Description                                                   |
|----------------------------------|----------|---------------------------------------------------------------|
| `branch_number`                  | str      | Bank Branch Number (for BANK TRANSFER method). Not used now.  |
| `account_number`                 | str      | Bank Account Number (for BANK TRANSFER method). Not used now. |
| `external_payment_link`          | str      | URL External Payment for CREDIT CARD method.                  |
| `external_payment_valid_through` | datetime | URL External Payment expiration datetime                      |

----

#### 2022.03.30 - Refactoring:

* Removed `/api/occupations/` endpoint.
* Removed `/api/quotes/me/payment` endpoint.
* Removed `partner_product_ids` in `Product` resource.
* On `/api/quotes/me` endpoint, `product` now contains `partner_id`, `title`,
  `description`, `product_price`, `product_price_currency`, `product_price_recurrence`
  and `product_locale`. For full product details, please refer to the
  `/api/quotes/me/product` endpoint.
* Added `terms_accepted_ip_address`, `terms_accepted_datetime` and `terms_accepted_email` in
  `Quote` resource.
* Removed `pep` and `lead_occupation` in `Quote` resource.

----

#### 2022.03.24 - New additions per mobile team requests:

* Add `/api/partners/active-products/schemas` endpoint
* Add `/api/quotes/me/payment/schemas` endpoint

----

#### 2022.03.23 - New additions per mobile team requests:

* Add all `/api/quotes/me/analysis` endpoints
* Make POST and GET schemas equal in `/api/quotes/me/address` endpoint
* Add new fields in `/api/quotes/me/`:

| Field                 | Type      | Description                               |
|-----------------------|-----------|-------------------------------------------|
| `is_final_state`      | bool      | Return if Quote is in a final status      |
| `is_persistent_state` | bool      | Return if Quote is in a persistent status |
| `denied_reason`       | list[str] | Show denied reasons for a denied Quote    |

* Add Product Titles, Description and FAQ in `/api/partners/active-products/me` endpoint

---

#### 2022.02.15 - Initial version
</details>

---
