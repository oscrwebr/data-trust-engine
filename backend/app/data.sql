-- ==========================
-- 1. Users
-- ==========================
DELETE FROM `user`;
INSERT INTO `user` (`user_id`, `firstname`, `surname`, `username`, `email`, `oid`, `refresh`, `role`) VALUES
(1, 'Tom', 'Clapham', 'tomclapham21@outlook.com',  'tomclapham21@outlook.com', '00000000-0000-0000-3054-4c8d7409054d', 'kasdjfh', 'admin'),
(2, 'Alice', 'Smith', 'alice@example.com', 'alice@example.com', 'oid1', 'kasdjfh', 'employee'),
(3, 'Bob', 'Johnson', 'bob@example.com', 'bob@example.com', 'oid2', 'kasdjfh', 'employee'),
(4, 'Charlie', 'Brown', 'charlie@example.com', 'charlie@example.com', 'oid3', 'kasdjfh', 'employee'),
(5, 'Delia', 'Plain', 'delia@example.com', 'delia@example.com', 'oid4', 'kasdjfh', 'employee'),
(6, 'Margaret', 'Plums', 'margaret@example.com', 'margaret@example.com', 'oid5', 'kasdjfh', 'employee'),
(7, 'Daiyan', 'Khan', 'daiyan@example.com', 'daiyan@example.com', 'oid6', 'kasdjfh', 'employee'),
(8, 'Oscar', 'Webster', 'oscar@example.com', 'oscar@example.com', 'oid7', 'kasdjfh', 'employee'),
(9, 'Sam', 'Carter', 'samtc.1107@gmail.com', 'samtc.1107@gmail.com', '00000000-0000-0000-e24b-a6db04ddcd03', 'kasdjfh', 'admin'),
(10, 'Elizabeth', 'Palmer', 'elizabeth@example.com', 'elizabeth@example.com', 'oid9', 'kasdjfh', 'employee'),
(11, 'Susan', 'Younger', 'susan@example.com', 'susan@example.com', 'oid10', 'kasdjfh', 'employee');


-- ==========================
-- 2. Pending Users
-- ==========================
DELETE FROM `pending_users`;
INSERT INTO `pending_users` (`user_id`, `email`, `type`) VALUES
(1, 'gertrude@email.com', 'invite'),
(2, 'wesley@outlook.com', 'invite'),
(3, 'philip@yahoo.com', 'invite'),
(4, 'daquavious@email.com', 'request'),
(5, 'francesca@outlook.com', 'request'),
(6, 'tomclapham21@gmail.com', 'request');

-- ==========================
-- 3. Workspaces
-- ==========================
DELETE FROM `workspaces`;
INSERT INTO `workspaces` (`id`, `name`, `image`) VALUES
(1, 'John Lewis & Partners', 0x66616B652D696D6167652D6279746573), -- 'fake-image-bytes' as hex
(2, 'Cardiff University Cleaning', 0x66616B652D696D6167652D6279746573),
(3, 'The Garden Center', 0x66616B652D696D6167652D6279746573),
(4, 'Injury Lawyers for You', 0x66616B652D696D6167652D6279746573),
(5, 'FlashPoint Cardiff', 0x66616B652D696D6167652D6279746573);


-- ==========================
-- 4. Invites
-- ==========================
DELETE FROM `invites`;
INSERT INTO `invites` (`invite_id`, `created_at`, `expiry_date`, `token`, `used`, `user_id`, `workspace_id`) VALUES
(1, '2026-01-30 14:00:00', '2026-04-30', 'token_abc123', TRUE, 1, 1),
(2, '2026-12-25 18:05:00', '2026-04-30', 'token_def456', TRUE, 2, 1),
(3, '2026-04-01 09:30:00', '2026-04-30', 'token_ghi789', TRUE, 3, 1);


-- ==========================
-- 5. User Workspaces
-- ==========================
DELETE FROM `user_workspace`;
INSERT INTO `user_workspace` (`user_id`, `workspace_id`) VALUES
(1, 1),
(2, 1),
(3, 1),
(4, 1),
(5, 1),
(6, 1),
(7, 1),
(8, 1),
(9, 1),
(10, 1),
(11, 1);


-- ==========================
-- 6. Pending User Workspaces
-- ==========================
DELETE FROM `pending_user_workspace`;
INSERT INTO `pending_user_workspace` (`user_id`, `workspace_id`) VALUES
(1, 1),
(2, 1),
(3, 1),
(4, 1),
(5, 1),
(6, 1);


-- ==========================
-- 7. Sensitivity Categories
-- ==========================
DELETE FROM `sensitivity_category`;
INSERT INTO `sensitivity_category` (`sensitivity_category_id`, `name`) VALUES
(1, 'Personal'),
(2, 'Financial'),
(3, 'Legal Case');


-- ==========================
-- 8. Sensitivity Subcategories
-- ==========================
DELETE FROM `sensitivity_subcategory`;
INSERT INTO `sensitivity_subcategory` (`sensitivity_subcategory_id`, `name`, `sensitivity_category_id`) VALUES
(1, 'NAME', 1),
(2, 'PHONE', 1),
(3, 'EMAIL', 1),
(4, 'ADDRESS', 1),
(5, 'POSTCODE', 1),
(6, 'IBAN', 2),
(7, 'VAT', 2),
(8, 'CITATION', 3),
(9, 'ACT', 3),
(10, 'REGULATION', 3),
(11, 'CASE_NAME', 3);

-- ==========================
-- 9. Roles
-- ==========================
DELETE FROM `role`;
INSERT INTO `role` (`role_id`, `workspace_id`, `name`) VALUES
(1, 1, 'PII Role'),
(2, 1, 'Financial Role'),
(3, 1, 'Legal Role'),
(4, 1, 'HR Role'),
(5, 1, 'Executive Role');

-- ==========================
-- 10. Role Permissions (threshold=50)
-- ==========================
DELETE FROM `role_permission`;
INSERT INTO `role_permission` (`role_permission_id`, `role_id`, `sensitivity_subcategory_id`, `threshold`) VALUES
(1, 1, 1, 50),
(2, 1, 2, 50),
(3, 1, 3, 50),
(4, 1, 4, 50),
(5, 1, 5, 50),
(6, 1, 6, 50),
(7, 1, 7, 50),
(8, 1, 8, 50),
(9, 1, 9, 50),
(10, 2, 10, 50),
(11, 2, 11, 50);

-- ==========================
-- 11. User Roles
-- ==========================
DELETE FROM `user_role`;
INSERT INTO `user_role` (`user_role_id`, `user_id`, `role_id`) VALUES
(1, 2, 1),
(2, 3, 2),
(3, 4, 3),
(4, 6, 4),
(5, 7, 5);

-- ==========================
-- 12. Files
-- ==========================
DELETE FROM `file`;
INSERT INTO `file` (`file_id`, `graph_file_id`, `file_name`, `hash`) VALUES
(1,'abc123','operational_report_document','e42ad1628a7c4757d92664bda3eeb1ce670f09e490807c2337bc5ebfe39d4edc'),
(2,'def456','realistic_contract_document','5c0a051ff032e9c9a1022f11a9b42f9824a11e1b0b6d533c8fca84ed0b71ec70'),
(3,'ghi789','supplier_agreement_document','3a3b74f5dad564603559be3b101c3706b633cdaad82db9ac6b1c42f9d1c88adf'),
(4,'lc111','legal_case_report_1','fba5e0abc3ded347b579760ad87ae310a1b00a52af989ce4da661059d9a885bb'),
(5,'lc222','legal_case_report_2','15fbe2cd8a4c0beebbde25dbd100ff64e5abe0227495adca7f15dd5525a8afa5');

INSERT INTO `file` (`graph_file_id`, `file_name`, `hash`) VALUES
('graph_014', 'employeeSalaryReport.pdf', 'abc123'),
('graph_015', 'employee_salary_summary.pdf', 'def456'),
('graph_016', 'ClientContractAgreement.docx', 'ghi789'),
('graph_017', 'financial report final.pdf', 'jkl321'),
('graph_018', 'employee-Report_final.docx', 'mno654');

-- ==========================
-- 13. Naming Conventions
-- ==========================
DELETE FROM `naming_convention`;
INSERT INTO `naming_convention` (`naming_convention_id`, `name`) VALUES 
(1, 'camel_case'),
(2, 'snake_case'),
(3, 'pascal_case'),
(4, 'kebab_case');