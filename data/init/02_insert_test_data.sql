-- Insertion de catégories
INSERT INTO category (id, intitule, created_at) VALUES
(1, 'Roman', CURRENT_TIMESTAMP),
(2, 'Science-Fiction', CURRENT_TIMESTAMP),
(3, 'Policier', CURRENT_TIMESTAMP),
(4, 'Biographie', CURRENT_TIMESTAMP),
(5, 'Informatique', CURRENT_TIMESTAMP);

-- Insertion de livres
INSERT INTO books (id, category_id, code, intitule, isbn_10, isbn_13, created_at) VALUES
(1, 1, 'ROM001', 'Les Misérables', '1234567890', '9781234567890', CURRENT_TIMESTAMP),
(2, 2, 'SF001', 'Dune', '2345678901', '9782345678901', CURRENT_TIMESTAMP),
(3, 3, 'POL001', 'Sherlock Holmes', '3456789012', '9783456789012', CURRENT_TIMESTAMP),
(4, 4, 'BIO001', 'Steve Jobs', '4567890123', '9784567890123', CURRENT_TIMESTAMP),
(5, 5, 'INFO001', 'Python pour les nuls', '5678901234', '9785678901234', CURRENT_TIMESTAMP),
(6, 1, 'ROM002', 'Le Comte de Monte-Cristo', '6789012345', '9786789012345', CURRENT_TIMESTAMP),
(7, 2, 'SF002', 'Fondation', '7890123456', '9787890123456', CURRENT_TIMESTAMP),
(8, 5, 'INFO002', 'Big Data pour tous', '8901234567', '9788901234567', CURRENT_TIMESTAMP);

-- Insertion de clients
INSERT INTO customers (id, code, first_name, last_name, created_at) VALUES
(1, 'CUST001', 'Jean', 'Dupont', CURRENT_TIMESTAMP),
(2, 'CUST002', 'Marie', 'Martin', CURRENT_TIMESTAMP),
(3, 'CUST003', 'Pierre', 'Bernard', CURRENT_TIMESTAMP),
(4, 'CUST004', 'Sophie', 'Petit', CURRENT_TIMESTAMP),
(5, 'CUST005', 'Lucas', 'Dubois', CURRENT_TIMESTAMP);

-- Insertion de factures et ventes historiques (2022-2025)
-- 2022:
INSERT INTO factures (id, code, date_edit, customers_id, qte_totale, total_amount, total_paid, created_at) VALUES
(100, 'FAC100', '20220110', 1, 2, 45.90, 45.90, CURRENT_TIMESTAMP),
(101, 'FAC101', '20220215', 2, 1, 29.99, 29.99, CURRENT_TIMESTAMP),
(102, 'FAC102', '20220320', 3, 1, 29.99, 29.99, CURRENT_TIMESTAMP),
(103, 'FAC103', '20220405', 4, 2, 49.80, 49.80, CURRENT_TIMESTAMP),
(104, 'FAC104', '20220512', 5, 2, 54.80, 54.80, CURRENT_TIMESTAMP),
(105, 'FAC105', '20220618', 1, 1, 24.90, 24.90, CURRENT_TIMESTAMP),
(106, 'FAC106', '20220722', 2, 2, 45.90, 45.90, CURRENT_TIMESTAMP),
(107, 'FAC107', '20220830', 3, 1, 29.99, 29.99, CURRENT_TIMESTAMP),
(108, 'FAC108', '20220915', 4, 2, 54.80, 54.80, CURRENT_TIMESTAMP),
(109, 'FAC109', '20221020', 5, 1, 24.90, 24.90, CURRENT_TIMESTAMP),
(110, 'FAC110', '20221125', 1, 2, 45.90, 45.90, CURRENT_TIMESTAMP),
(111, 'FAC111', '20221210', 2, 1, 29.99, 29.99, CURRENT_TIMESTAMP);

-- 2023:
INSERT INTO factures (id, code, date_edit, customers_id, qte_totale, total_amount, total_paid, created_at) VALUES
(200, 'FAC200', '20230115', 1, 3, 75.80, 75.80, CURRENT_TIMESTAMP),
(201, 'FAC201', '20230220', 2, 2, 54.90, 54.90, CURRENT_TIMESTAMP),
(202, 'FAC202', '20230310', 3, 2, 49.80, 49.80, CURRENT_TIMESTAMP),
(203, 'FAC203', '20230405', 4, 3, 82.50, 82.50, CURRENT_TIMESTAMP),
(204, 'FAC204', '20230512', 5, 2, 54.80, 54.80, CURRENT_TIMESTAMP),
(205, 'FAC205', '20230618', 1, 2, 45.90, 45.90, CURRENT_TIMESTAMP),
(206, 'FAC206', '20230722', 2, 3, 67.50, 67.50, CURRENT_TIMESTAMP),
(207, 'FAC207', '20230830', 3, 2, 54.80, 54.80, CURRENT_TIMESTAMP),
(208, 'FAC208', '20230915', 4, 2, 45.90, 45.90, CURRENT_TIMESTAMP),
(209, 'FAC209', '20231020', 5, 3, 67.50, 67.50, CURRENT_TIMESTAMP),
(210, 'FAC210', '20231125', 1, 2, 54.80, 54.80, CURRENT_TIMESTAMP),
(211, 'FAC211', '20231210', 2, 2, 45.90, 45.90, CURRENT_TIMESTAMP);

-- 2024:
INSERT INTO factures (id, code, date_edit, customers_id, qte_totale, total_amount, total_paid, created_at) VALUES
(300, 'FAC300', '20240105', 3, 3, 82.50, 82.50, CURRENT_TIMESTAMP),
(301, 'FAC301', '20240120', 4, 2, 54.80, 54.80, CURRENT_TIMESTAMP),
(302, 'FAC302', '20240215', 5, 3, 67.50, 67.50, CURRENT_TIMESTAMP),
(303, 'FAC303', '20240310', 1, 2, 45.90, 45.90, CURRENT_TIMESTAMP),
(304, 'FAC304', '20240405', 2, 3, 75.80, 75.80, CURRENT_TIMESTAMP),
(305, 'FAC305', '20240512', 3, 2, 54.80, 54.80, CURRENT_TIMESTAMP),
(306, 'FAC306', '20240618', 4, 3, 67.50, 67.50, CURRENT_TIMESTAMP),
(307, 'FAC307', '20240722', 5, 2, 45.90, 45.90, CURRENT_TIMESTAMP),
(308, 'FAC308', '20240830', 1, 3, 82.50, 82.50, CURRENT_TIMESTAMP),
(309, 'FAC309', '20240915', 2, 2, 54.80, 54.80, CURRENT_TIMESTAMP),
(310, 'FAC310', '20241020', 3, 3, 67.50, 67.50, CURRENT_TIMESTAMP),
(311, 'FAC311', '20241125', 4, 2, 45.90, 45.90, CURRENT_TIMESTAMP),
(312, 'FAC312', '20241210', 5, 3, 75.80, 75.80, CURRENT_TIMESTAMP);

-- 2025:
INSERT INTO factures (id, code, date_edit, customers_id, qte_totale, total_amount, total_paid, created_at) VALUES
(400, 'FAC400', '20250101', 1, 3, 82.50, 82.50, CURRENT_TIMESTAMP),
(401, 'FAC401', '20250115', 2, 3, 67.50, 67.50, CURRENT_TIMESTAMP),
(402, 'FAC402', '20250202', 3, 4, 99.80, 99.80, CURRENT_TIMESTAMP),
(403, 'FAC403', '20250220', 4, 3, 75.80, 75.80, CURRENT_TIMESTAMP),
(404, 'FAC404', '20250305', 5, 3, 67.50, 67.50, CURRENT_TIMESTAMP),
(405, 'FAC405', '20250315', 1, 4, 99.80, 99.80, CURRENT_TIMESTAMP),
(406, 'FAC406', '20250325', 2, 3, 75.80, 75.80, CURRENT_TIMESTAMP),
(407, 'FAC407', '20250405', 3, 3, 67.50, 67.50, CURRENT_TIMESTAMP),
(408, 'FAC408', '20250415', 4, 4, 99.80, 99.80, CURRENT_TIMESTAMP),
(409, 'FAC409', '20250425', 5, 3, 75.80, 75.80, CURRENT_TIMESTAMP),
(410, 'FAC410', '20250505', 1, 3, 67.50, 67.50, CURRENT_TIMESTAMP),
(411, 'FAC411', '20250515', 2, 4, 99.80, 99.80, CURRENT_TIMESTAMP),
(412, 'FAC412', '20250525', 3, 3, 75.80, 75.80, CURRENT_TIMESTAMP);

-- Insertion des ventes correspondantes
-- 2022:
INSERT INTO ventes (id, code, date_edit, factures_id, books_id, pu, qte, created_at) VALUES
(100, 'VNT100', '20220110', 100, 1, 22.95, 1, CURRENT_TIMESTAMP),
(101, 'VNT101', '20220110', 100, 3, 22.95, 1, CURRENT_TIMESTAMP),
(102, 'VNT102', '20220215', 101, 2, 29.99, 1, CURRENT_TIMESTAMP),
(103, 'VNT103', '20220320', 102, 4, 29.99, 1, CURRENT_TIMESTAMP),
(104, 'VNT104', '20220405', 103, 5, 24.90, 1, CURRENT_TIMESTAMP),
(105, 'VNT105', '20220405', 103, 6, 24.90, 1, CURRENT_TIMESTAMP),
(106, 'VNT106', '20220512', 104, 7, 27.40, 1, CURRENT_TIMESTAMP),
(107, 'VNT107', '20220512', 104, 8, 27.40, 1, CURRENT_TIMESTAMP),
(108, 'VNT108', '20220618', 105, 1, 24.90, 1, CURRENT_TIMESTAMP),
(109, 'VNT109', '20220722', 106, 2, 22.95, 1, CURRENT_TIMESTAMP),
(110, 'VNT110', '20220722', 106, 3, 22.95, 1, CURRENT_TIMESTAMP),
(111, 'VNT111', '20220830', 107, 4, 29.99, 1, CURRENT_TIMESTAMP),
(112, 'VNT112', '20220915', 108, 5, 27.40, 1, CURRENT_TIMESTAMP),
(113, 'VNT113', '20220915', 108, 6, 27.40, 1, CURRENT_TIMESTAMP),
(114, 'VNT114', '20221020', 109, 7, 24.90, 1, CURRENT_TIMESTAMP),
(115, 'VNT115', '20221125', 110, 8, 22.95, 1, CURRENT_TIMESTAMP),
(116, 'VNT116', '20221125', 110, 1, 22.95, 1, CURRENT_TIMESTAMP),
(117, 'VNT117', '20221210', 111, 2, 29.99, 1, CURRENT_TIMESTAMP);

-- 2023:
INSERT INTO ventes (id, code, date_edit, factures_id, books_id, pu, qte, created_at) VALUES
(200, 'VNT200', '20230115', 200, 1, 22.95, 1, CURRENT_TIMESTAMP),
(201, 'VNT201', '20230115', 200, 3, 22.95, 1, CURRENT_TIMESTAMP),
(202, 'VNT202', '20230115', 200, 5, 29.90, 1, CURRENT_TIMESTAMP),
(203, 'VNT203', '20230220', 201, 2, 29.99, 1, CURRENT_TIMESTAMP),
(204, 'VNT204', '20230220', 201, 4, 24.91, 1, CURRENT_TIMESTAMP),
(205, 'VNT205', '20230310', 202, 6, 24.90, 1, CURRENT_TIMESTAMP),
(206, 'VNT206', '20230310', 202, 7, 24.90, 1, CURRENT_TIMESTAMP),
(207, 'VNT207', '20230405', 203, 8, 27.40, 1, CURRENT_TIMESTAMP),
(208, 'VNT208', '20230405', 203, 1, 27.40, 1, CURRENT_TIMESTAMP),
(209, 'VNT209', '20230405', 203, 2, 27.40, 1, CURRENT_TIMESTAMP),
(210, 'VNT210', '20230512', 204, 3, 27.40, 1, CURRENT_TIMESTAMP),
(211, 'VNT211', '20230512', 204, 4, 27.40, 1, CURRENT_TIMESTAMP),
(212, 'VNT212', '20230618', 205, 5, 22.95, 1, CURRENT_TIMESTAMP),
(213, 'VNT213', '20230618', 205, 6, 22.95, 1, CURRENT_TIMESTAMP),
(214, 'VNT214', '20230722', 206, 7, 22.95, 1, CURRENT_TIMESTAMP),
(215, 'VNT215', '20230722', 206, 8, 22.95, 1, CURRENT_TIMESTAMP),
(216, 'VNT216', '20230722', 206, 1, 21.60, 1, CURRENT_TIMESTAMP),
(217, 'VNT217', '20230830', 207, 2, 27.40, 1, CURRENT_TIMESTAMP),
(218, 'VNT218', '20230830', 207, 3, 27.40, 1, CURRENT_TIMESTAMP),
(219, 'VNT219', '20230915', 208, 4, 22.95, 1, CURRENT_TIMESTAMP),
(220, 'VNT220', '20230915', 208, 5, 22.95, 1, CURRENT_TIMESTAMP),
(221, 'VNT221', '20231020', 209, 6, 22.95, 1, CURRENT_TIMESTAMP),
(222, 'VNT222', '20231020', 209, 7, 22.95, 1, CURRENT_TIMESTAMP),
(223, 'VNT223', '20231020', 209, 8, 21.60, 1, CURRENT_TIMESTAMP),
(224, 'VNT224', '20231125', 210, 1, 27.40, 1, CURRENT_TIMESTAMP),
(225, 'VNT225', '20231125', 210, 2, 27.40, 1, CURRENT_TIMESTAMP),
(226, 'VNT226', '20231210', 211, 3, 22.95, 1, CURRENT_TIMESTAMP),
(227, 'VNT227', '20231210', 211, 4, 22.95, 1, CURRENT_TIMESTAMP);

-- 2024:
INSERT INTO ventes (id, code, date_edit, factures_id, books_id, pu, qte, created_at) VALUES
(300, 'VNT300', '20240105', 300, 1, 22.95, 1, CURRENT_TIMESTAMP),
(301, 'VNT301', '20240105', 300, 3, 22.95, 1, CURRENT_TIMESTAMP),
(302, 'VNT302', '20240105', 300, 5, 29.90, 1, CURRENT_TIMESTAMP),
(303, 'VNT303', '20240120', 301, 2, 27.40, 1, CURRENT_TIMESTAMP),
(304, 'VNT304', '20240120', 301, 4, 27.40, 1, CURRENT_TIMESTAMP),
(305, 'VNT305', '20240215', 302, 6, 22.95, 1, CURRENT_TIMESTAMP),
(306, 'VNT306', '20240215', 302, 7, 22.95, 1, CURRENT_TIMESTAMP),
(307, 'VNT307', '20240215', 302, 8, 21.60, 1, CURRENT_TIMESTAMP),
(308, 'VNT308', '20240310', 303, 1, 27.40, 1, CURRENT_TIMESTAMP),
(309, 'VNT309', '20240310', 303, 2, 27.40, 1, CURRENT_TIMESTAMP),
(310, 'VNT310', '20240405', 304, 3, 22.95, 1, CURRENT_TIMESTAMP),
(311, 'VNT311', '20240405', 304, 4, 22.95, 1, CURRENT_TIMESTAMP),
(312, 'VNT312', '20240405', 304, 5, 29.90, 1, CURRENT_TIMESTAMP),
(313, 'VNT313', '20240512', 305, 6, 27.40, 1, CURRENT_TIMESTAMP),
(314, 'VNT314', '20240512', 305, 7, 27.40, 1, CURRENT_TIMESTAMP),
(315, 'VNT315', '20240618', 306, 8, 22.95, 1, CURRENT_TIMESTAMP),
(316, 'VNT316', '20240618', 306, 1, 22.95, 1, CURRENT_TIMESTAMP),
(317, 'VNT317', '20240618', 306, 2, 21.60, 1, CURRENT_TIMESTAMP),
(318, 'VNT318', '20240722', 307, 3, 27.40, 1, CURRENT_TIMESTAMP),
(319, 'VNT319', '20240722', 307, 4, 27.40, 1, CURRENT_TIMESTAMP),
(320, 'VNT320', '20240830', 308, 5, 22.95, 1, CURRENT_TIMESTAMP),
(321, 'VNT321', '20240830', 308, 6, 22.95, 1, CURRENT_TIMESTAMP),
(322, 'VNT322', '20240830', 308, 7, 29.90, 1, CURRENT_TIMESTAMP),
(323, 'VNT323', '20240915', 309, 8, 27.40, 1, CURRENT_TIMESTAMP),
(324, 'VNT324', '20240915', 309, 1, 27.40, 1, CURRENT_TIMESTAMP),
(325, 'VNT325', '20241020', 310, 2, 22.95, 1, CURRENT_TIMESTAMP),
(326, 'VNT326', '20241020', 310, 3, 22.95, 1, CURRENT_TIMESTAMP),
(327, 'VNT327', '20241020', 310, 4, 21.60, 1, CURRENT_TIMESTAMP),
(328, 'VNT328', '20241125', 311, 5, 27.40, 1, CURRENT_TIMESTAMP),
(329, 'VNT329', '20241125', 311, 6, 27.40, 1, CURRENT_TIMESTAMP),
(330, 'VNT330', '20241210', 312, 7, 22.95, 1, CURRENT_TIMESTAMP),
(331, 'VNT331', '20241210', 312, 8, 22.95, 1, CURRENT_TIMESTAMP),
(332, 'VNT332', '20241210', 312, 1, 29.90, 1, CURRENT_TIMESTAMP);

-- 2025:
INSERT INTO ventes (id, code, date_edit, factures_id, books_id, pu, qte, created_at) VALUES
(400, 'VNT400', '20250101', 400, 1, 22.95, 1, CURRENT_TIMESTAMP),
(401, 'VNT401', '20250101', 400, 3, 22.95, 1, CURRENT_TIMESTAMP),
(402, 'VNT402', '20250101', 400, 5, 29.90, 1, CURRENT_TIMESTAMP),
(403, 'VNT403', '20250115', 401, 2, 22.95, 1, CURRENT_TIMESTAMP),
(404, 'VNT404', '20250115', 401, 4, 22.95, 1, CURRENT_TIMESTAMP),
(405, 'VNT405', '20250115', 401, 6, 21.60, 1, CURRENT_TIMESTAMP),
(406, 'VNT406', '20250202', 402, 7, 27.40, 1, CURRENT_TIMESTAMP),
(407, 'VNT407', '20250202', 402, 8, 27.40, 1, CURRENT_TIMESTAMP),
(408, 'VNT408', '20250202', 402, 1, 27.40, 1, CURRENT_TIMESTAMP),
(409, 'VNT409', '20250202', 402, 2, 27.40, 1, CURRENT_TIMESTAMP),
(410, 'VNT410', '20250220', 403, 3, 22.95, 1, CURRENT_TIMESTAMP),
(411, 'VNT411', '20250220', 403, 4, 22.95, 1, CURRENT_TIMESTAMP),
(412, 'VNT412', '20250220', 403, 5, 29.90, 1, CURRENT_TIMESTAMP),
(413, 'VNT413', '20250305', 404, 6, 27.40, 1, CURRENT_TIMESTAMP),
(414, 'VNT414', '20250305', 404, 7, 27.40, 1, CURRENT_TIMESTAMP),
(415, 'VNT415', '20250305', 404, 8, 21.60, 1, CURRENT_TIMESTAMP),
(416, 'VNT416', '20250315', 405, 1, 22.95, 1, CURRENT_TIMESTAMP),
(417, 'VNT417', '20250315', 405, 2, 22.95, 1, CURRENT_TIMESTAMP),
(418, 'VNT418', '20250315', 405, 3, 29.90, 1, CURRENT_TIMESTAMP),
(419, 'VNT419', '20250315', 405, 4, 27.40, 1, CURRENT_TIMESTAMP),
(420, 'VNT420', '20250325', 406, 5, 27.40, 1, CURRENT_TIMESTAMP),
(421, 'VNT421', '20250325', 406, 6, 27.40, 1, CURRENT_TIMESTAMP),
(422, 'VNT422', '20250325', 406, 7, 21.60, 1, CURRENT_TIMESTAMP),
(423, 'VNT423', '20250405', 407, 8, 22.95, 1, CURRENT_TIMESTAMP),
(424, 'VNT424', '20250405', 407, 1, 22.95, 1, CURRENT_TIMESTAMP),
(425, 'VNT425', '20250405', 407, 2, 29.90, 1, CURRENT_TIMESTAMP),
(426, 'VNT426', '20250415', 408, 3, 27.40, 1, CURRENT_TIMESTAMP),
(427, 'VNT427', '20250415', 408, 4, 27.40, 1, CURRENT_TIMESTAMP),
(428, 'VNT428', '20250415', 408, 5, 27.40, 1, CURRENT_TIMESTAMP),
(429, 'VNT429', '20250415', 408, 6, 21.60, 1, CURRENT_TIMESTAMP),
(430, 'VNT430', '20250425', 409, 7, 22.95, 1, CURRENT_TIMESTAMP),
(431, 'VNT431', '20250425', 409, 8, 22.95, 1, CURRENT_TIMESTAMP),
(432, 'VNT432', '20250425', 409, 1, 29.90, 1, CURRENT_TIMESTAMP),
(433, 'VNT433', '20250505', 410, 2, 27.40, 1, CURRENT_TIMESTAMP),
(434, 'VNT434', '20250505', 410, 3, 27.40, 1, CURRENT_TIMESTAMP),
(435, 'VNT435', '20250505', 410, 4, 21.60, 1, CURRENT_TIMESTAMP),
(436, 'VNT436', '20250515', 411, 5, 22.95, 1, CURRENT_TIMESTAMP),
(437, 'VNT437', '20250515', 411, 6, 22.95, 1, CURRENT_TIMESTAMP),
(438, 'VNT438', '20250515', 411, 7, 29.90, 1, CURRENT_TIMESTAMP),
(439, 'VNT439', '20250515', 411, 8, 27.40, 1, CURRENT_TIMESTAMP),
(440, 'VNT440', '20250525', 412, 1, 27.40, 1, CURRENT_TIMESTAMP),
(441, 'VNT441', '20250525', 412, 2, 27.40, 1, CURRENT_TIMESTAMP),
(442, 'VNT442', '20250525', 412, 3, 21.60, 1, CURRENT_TIMESTAMP); 