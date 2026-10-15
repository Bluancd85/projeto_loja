-- Esquema da Mini Loja: 4 tabelas relacionadas + 1 view de relatório.

PRAGMA foreign_keys = ON;

DROP VIEW IF EXISTS vw_itens_detalhados;
DROP TABLE IF EXISTS itens_pedido;
DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS produtos;
DROP TABLE IF EXISTS clientes;

CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    cidade TEXT NOT NULL
);

CREATE TABLE produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    preco REAL NOT NULL CHECK (preco >= 0)
);

CREATE TABLE pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    data_pedido TEXT NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes (id)
);

CREATE TABLE itens_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unitario REAL NOT NULL CHECK (preco_unitario >= 0),
    FOREIGN KEY (pedido_id) REFERENCES pedidos (id),
    FOREIGN KEY (produto_id) REFERENCES produtos (id)
);

CREATE INDEX idx_pedidos_cliente_id ON pedidos (cliente_id);
CREATE INDEX idx_itens_pedido_pedido_id ON itens_pedido (pedido_id);
CREATE INDEX idx_itens_pedido_produto_id ON itens_pedido (produto_id);

-- View de relatório: cada item de pedido já "achatado" com dados de
-- cliente, pedido e produto, pronta para ser reaproveitada por várias
-- consultas (pedidos detalhados, faturamento, ranking).
CREATE VIEW vw_itens_detalhados AS
SELECT
    i.id AS item_id,
    p.id AS pedido_id,
    p.data_pedido AS data_pedido,
    c.id AS cliente_id,
    c.nome AS cliente_nome,
    pr.id AS produto_id,
    pr.nome AS produto_nome,
    pr.categoria AS produto_categoria,
    i.quantidade AS quantidade,
    i.preco_unitario AS preco_unitario,
    i.quantidade * i.preco_unitario AS subtotal
FROM itens_pedido AS i
JOIN pedidos AS p ON p.id = i.pedido_id
JOIN clientes AS c ON c.id = p.cliente_id
JOIN produtos AS pr ON pr.id = i.produto_id;
