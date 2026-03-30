-- ==========================
-- 1. Workspaces
-- ==========================
INSERT INTO `workspaces` (`id`, `name`, `image`) VALUES
(1, 'Test Workspace', 0x66616B652D696D6167652D6279746573);

-- ==========================
-- 2. Users
-- ==========================
DELETE FROM `user`;
INSERT INTO `user` (`user_id`, `firstname`, `surname`, `username`, `email`, `refresh`, `oid`, `role`) VALUES
(1, 'Alice', 'Smith', 'alice@example.com', 'alice@example.com', 'kasdjfh', 'oid1', 'Employee'),
(2, 'Bob', 'Johnson', 'bob@example.com', 'bob@example.com', 'kasdjfh', 'oid2', 'Employee'),
(3, 'Charlie', 'Brown', 'charlie@example.com', 'charlie@example.com', 'kasdjfh', 'oid3', 'Employee');

-- ==========================
-- 2. User Workspace
-- ==========================

INSERT INTO `user_workspace` (`user_id`, `workspace_id`) VALUES
(1, 1),
(2, 1),
(3, 1);

-- ==========================
-- 4. Sensitivity Categories
-- ==========================
INSERT INTO `sensitivity_category` (`sensitivity_category_id`, `name`) VALUES
(1, 'PII'),
(2, 'Financial'),
(3, 'Legal');

-- ==========================
-- 5. Sensitivity Subcategories
-- ==========================
INSERT INTO `sensitivity_subcategory` (`sensitivity_subcategory_id`, `name`, `sensitivity_category_id`) VALUES
(1, 'Names', 1),
(2, 'Phone numbers', 1),
(3, 'Emails', 1),
(4, 'Passwords', 1),
(5, 'Addresses', 1),
(6, 'Postcodes', 1),
(7, 'Number plates', 1),
(8, 'IP address', 1),
(9, 'MAC address', 1),
(10, 'IBANs', 2),
(11, 'VAT numbers', 2),
(12, 'Payment transactions', 2),
(13, 'Contracts', 3),
(14, 'Court Records', 3),
(15, 'NDAs', 3),
(16, 'Legal Claims', 3),
(17, 'Compliance Documents', 3);

-- ==========================
-- 6. Roles
-- ==========================
INSERT INTO `role` (`role_id`, `name`) VALUES
(1, 'PII Role'),
(2, 'Financial Role'),
(3, 'Legal Role');

-- ==========================
-- 7. Role Permissions (threshold=50)
-- ==========================
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
(11, 2, 11, 50),
(12, 2, 12, 50),
(13, 3, 13, 50),
(14, 3, 14, 50),
(15, 3, 15, 50),
(16, 3, 16, 50),
(17, 3, 17, 50);

-- ==========================
-- 8. User Roles
-- ==========================
INSERT INTO `user_role` (`user_role_id`, `user_id`, `role_id`) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 3);

-- ==========================
-- 9. Files
-- ==========================
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
-- 10. Naming Conventions
-- ==========================
INSERT INTO `naming_convention` (`naming_convention_id`, `name`) VALUES 
(1, 'camel_case'),
(2, 'snake_case'),
(3, 'pascal_case'),
(4, 'kebab_case');