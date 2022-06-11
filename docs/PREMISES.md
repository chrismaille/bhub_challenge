## Challenge Premisses

#### O que estamos tentando resolver?

Criar uma API que controle cadastro de clientes, conforme indicado aqui - https://drive.google.com/file/d/1e1RZtvOKKwqzPgj_0V_9XOfMjRm6mvZg/view

#### Premissas adicionais

A partir das premissas apresentadas, está adicionado:

* O cadastro pode ser acessado tanto via API quando via Admin Panel.
* **Dados Bancários** serão considerados como um de vários _Métodos de Pagamento_.
* O cadastro pode ter mais de um endereço, classificado como _Entrega_ ou _Cobrança_.
* O cadastro pode ser bloqueado, com o desbloqueio feito via Admin.
* Toda a criação, alteração e exclusão no cadastro deve ser realizada por um usuário autenticado. No caso da API,
  será gravado pelo super-usuário do sistema.

#### Tópicos para Apresentação

1. **Stack**. Porque Postgres e Django Rest-Framework? Porque Python assíncrono e a suas limitações no Django.
2. **Modelagem**. Explicar a modelagem de dados.
3. **Fluxo da API**. Explicar o fluxo proposta da API.
4. **Views**. Explicar rotas aninhadas x PATCH, Autenticação e Serializadores.
5. **DAOs**. Explicar como funciona o DAO.
6. **Testes Unitários**. Explicar Factories, Fixtures e Teste de Cliente assíncrono.
7. **DEV Container**. Explicar como funciona o desenvolvimento local via Docker.
8. **CI/CD**. Explicar como funciona o CI focando no Github Actions.
