-- Dados de exemplo para a Mini Loja.

INSERT INTO clientes (nome, email, cidade) VALUES
    ('Ana Souza', 'ana.souza@example.com', 'São Paulo'),
    ('Bruno Lima', 'bruno.lima@example.com', 'Rio de Janeiro'),
    ('Carla Mendes', 'carla.mendes@example.com', 'Belo Horizonte'),
    ('Diego Alves', 'diego.alves@example.com', 'Curitiba'),
    ('Elisa Rocha', 'elisa.rocha@example.com', 'São Paulo');

INSERT INTO produtos (nome, categoria, preco) VALUES
    ('Teclado Mecânico', 'Informática', 350.00),
    ('Mouse Sem Fio', 'Informática', 120.00),
    ('Monitor 27"', 'Informática', 1200.00),
    ('Cadeira Gamer', 'Móveis', 950.00),
    ('Mesa de Escritório', 'Móveis', 700.00),
    ('Fone Bluetooth', 'Áudio', 180.00),
    ('Caixa de Som', 'Áudio', 250.00),
    ('Webcam HD', 'Informática', 220.00);

INSERT INTO pedidos (cliente_id, data_pedido) VALUES
    (1, '2026-01-10'),
    (1, '2026-02-05'),
    (2, '2026-01-15'),
    (3, '2026-01-20'),
    (4, '2026-02-01'),
    (5, '2026-02-10'),
    (2, '2026-02-15');

INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES
    (1, 1, 1, 350.00),
    (1, 2, 2, 120.00),
    (2, 3, 1, 1200.00),
    (3, 4, 1, 950.00),
    (3, 6, 1, 180.00),
    (4, 5, 1, 700.00),
    (4, 7, 2, 250.00),
    (5, 2, 1, 120.00),
    (5, 8, 1, 220.00),
    (6, 1, 2, 350.00),
    (6, 6, 1, 180.00),
    (7, 3, 1, 1200.00),
    (7, 4, 1, 950.00);
