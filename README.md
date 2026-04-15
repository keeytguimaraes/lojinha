# Projeto Lojinha
Este projeto consiste no desenvolvimento de um sistema web para controle de estoque de um pequeno comércio (“Lojinhainha”), criado como trabalho escolar. A aplicação foi desenvolvida utilizando Python com o framework Flask e banco de dados MySQL.

O sistema permite o gerenciamento completo de informações essenciais, incluindo cadastro e listagem de clientes, fornecedores, vendedores, produtos em estoque e registro de vendas. Além disso, conta com funcionalidades de exclusão de registros e organização dos dados por meio de relacionamentos entre as tabelas do banco de dados, garantindo maior integridade e consistência das informações.

A aplicação também possui integração direta com o banco de dados utilizando MySQL Connector/Python, permitindo a execução de operações como inserção, consulta e manipulação de dados de forma eficiente.

A interface foi construída com HTML, CSS e Bootstrap, buscando oferecer uma navegação simples e intuitiva. O sistema conta com menu lateral para acesso às funcionalidades, além de uma barra superior (topbar) com o título da aplicação e um botão de navegação “Voltar”, melhorando a experiência do usuário.

Como recurso adicional, foi implementada uma funcionalidade de busca dinâmica nas tabelas, desenvolvida em JavaScript, que permite localizar registros em tempo real. As sugestões são exibidas automaticamente conforme o usuário digita, e ao selecionar um resultado, o sistema destaca o item correspondente na tabela, facilitando a navegação.

## Autenticação e Controle de Acesso
O sistema possui um módulo de autenticação de usuários, permitindo login seguro através de validação no banco de dados. As senhas são armazenadas de forma protegida utilizando hash (Werkzeug Security), garantindo maior segurança contra acessos não autorizados.

Além disso, o sistema implementa um controle de acesso baseado em níveis (RBAC), diferenciando usuários administradores e vendedores:

Administrador (tipo_login = 1): acesso completo ao sistema
Vendedor (tipo_login = 2): acesso restrito a determinadas funcionalidades

O controle de acesso é realizado por meio de sessões do Flask e decorators, garantindo que apenas usuários autenticados e autorizados possam acessar determinadas rotas do sistema.

O principal objetivo do projeto é facilitar o controle e a organização de um estoque de forma prática, centralizando informações importantes e auxiliando na gestão do negócio de maneira simples e eficiente.

## Acesso ao sistema

### Administrador
Usuário: admin  
Senha: admin123  

### Vendedor
Usuário: vendedor 
Senha: vend123  

# Lojinha project

This project consists of the development of a web system for inventory control of a small business (“Lojinhainha”), created as a school project. The application was developed using Python with the Flask framework and a MySQL database.

The system allows full management of essential information, including registration and listing of customers, suppliers, sellers, products in stock, and sales records. In addition, it includes record deletion features and data organization through relationships between database tables, ensuring greater integrity and consistency of information.

The application also integrates directly with the database using MySQL Connector/Python, enabling efficient data insertion, querying, and manipulation.

The interface was built using HTML, CSS, and Bootstrap, aiming to provide a simple and intuitive user experience. The system includes a sidebar menu for accessing functionalities, as well as a topbar with the application title and a “Back” button to improve navigation.

As an additional feature, a dynamic search functionality was implemented using JavaScript, allowing users to find records in real time. Suggestions are automatically displayed as the user types, and selecting a result highlights the corresponding item in the table, making navigation easier.

##  Authentication and Access Control
The system includes a user authentication module, allowing secure login through database validation. Passwords are securely stored using hashing (Werkzeug Security), ensuring protection against unauthorized access.

Additionally, the system implements role-based access control (RBAC), distinguishing between administrators and sellers:

Administrator (tipo_login = 1): full system access
Seller (tipo_login = 2): restricted access to certain features

Access control is handled through Flask sessions and decorators, ensuring that only authenticated and authorized users can access protected routes.

The main objective of this project is to facilitate inventory management in a practical way, centralizing important information and helping manage the business efficiently.

## System Access

### Administrator
Username: admin  
Password: admin123  

### Seller
Username: vendedor
Password: vend123  