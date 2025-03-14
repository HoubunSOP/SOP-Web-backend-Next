-- 创建 comic_authors 表
CREATE TABLE comic_authors
(
    id   INT          NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);
-- 创建 comics 表
CREATE TABLE comics
(
    id            INT          NOT NULL AUTO_INCREMENT,
    name          VARCHAR(255) NOT NULL,
    original_name VARCHAR(255)          DEFAULT NULL,
    author_id     INT          NOT NULL,
    date          DATE         NOT NULL,
    intro         TEXT,
    cover         VARCHAR(255) NOT NULL,
    auto          BOOLEAN      NOT NULL DEFAULT FALSE,
    volume        INT                   DEFAULT '1',
    isbn          BIGINT                DEFAULT NULL,
    cid           INT                   DEFAULT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (author_id) REFERENCES comic_authors (id) ON DELETE CASCADE
);
-- 创建用户组表
CREATE TABLE user_groups
(
    id               INT          NOT NULL AUTO_INCREMENT,
    group_name       VARCHAR(255) NOT NULL,
    permission_level BIGINT       NOT NULL,
    PRIMARY KEY (id)
);
-- 创建 users 表
CREATE TABLE users
(
    id              INT          NOT NULL AUTO_INCREMENT,
    username        VARCHAR(255) NOT NULL,
    password        VARCHAR(255) NOT NULL,
    user_avatar     VARCHAR(255) DEFAULT NULL,
    user_permission BIGINT       DEFAULT '0',
    user_bio        TEXT         DEFAULT NULL,
    user_position   INT          DEFAULT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_position) REFERENCES user_groups (id) ON DELETE
        SET NULL
);
-- 创建 articles 表
CREATE TABLE articles
(
    id          INT          NOT NULL AUTO_INCREMENT,
    title       VARCHAR(255) NOT NULL,
    date        DATE         NOT NULL,
    content     TEXT,
    cover       VARCHAR(255) DEFAULT NULL,
    comic       VARCHAR(255) DEFAULT NULL,
    recommended BOOLEAN      DEFAULT FALSE,
    author_id   INT          NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (author_id) REFERENCES users (id) ON DELETE CASCADE
);
-- 创建 magazines 表
CREATE TABLE magazines
(
    id           INT          NOT NULL AUTO_INCREMENT,
    name         VARCHAR(255) NOT NULL,
    cover        VARCHAR(255) NOT NULL,
    publish_date DATE         NOT NULL,
    intro        TEXT         DEFAULT NULL,
    link         VARCHAR(255) DEFAULT NULL,
    PRIMARY KEY (id)
);
-- 创建 category_types 表
CREATE TABLE category_types
(
    id   INT          NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);
-- 创建 categories 表
CREATE TABLE categories
(
    id            INT          NOT NULL AUTO_INCREMENT,
    name          VARCHAR(255) NOT NULL,
    category_type INT          NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (category_type) REFERENCES category_types (id) ON DELETE CASCADE
);
-- 创建 comic_category_map 表，用于关联漫画和分类
CREATE TABLE comic_category_map
(
    comic_id    INT NOT NULL,
    category_id INT NOT NULL,
    PRIMARY KEY (comic_id, category_id),
    FOREIGN KEY (comic_id) REFERENCES comics (id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
);
-- 创建 article_category_map 表，用于关联文章和分类
CREATE TABLE article_category_map
(
    article_id  INT NOT NULL,
    category_id INT NOT NULL,
    PRIMARY KEY (article_id, category_id),
    FOREIGN KEY (article_id) REFERENCES articles (id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
);
-- 创建 magazine_category_map 表，用于关联杂志和分类
CREATE TABLE magazine_category_map
(
    magazine_id INT NOT NULL,
    category_id INT NOT NULL,
    PRIMARY KEY (magazine_id, category_id),
    FOREIGN KEY (magazine_id) REFERENCES magazines (id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
);
-- 创建 magazine_comic_map 表，用于存储杂志和多个漫画名称的关联
CREATE TABLE magazine_comic_map
(
    magazine_id INT          NOT NULL,
    comic_name  VARCHAR(255) NOT NULL,
    FOREIGN KEY (magazine_id) REFERENCES magazines (id) ON DELETE CASCADE
);
-- 创建settings表
CREATE TABLE settings
(
    settings_key   VARCHAR(255) NOT NULL,
    settings_value VARCHAR(255) NOT NULL,
    PRIMARY KEY (settings_key)
);
-- 插入分类类型数据
INSERT INTO category_types (name)
VALUES ('漫画'),
       ('文章'),
       ('杂志');
-- 添加漫画分类示例
INSERT INTO categories (name, category_type)
VALUES ('Kirara', 1),
       ('MAX', 1),
       ('Carat', 1),
       ('Forward', 1),
       ('其他', 1);
-- 添加文章分类示例
INSERT INTO categories (name, category_type)
VALUES ('未分类', 2);
-- 添加杂志分类示例
INSERT INTO categories (name, category_type)
VALUES ('Kirara', 3),
       ('MAX', 3),
       ('Carat', 3),
       ('Forward', 3),
       ('其他', 3);
-- 插入settings表的初始数据
INSERT INTO settings (settings_key, settings_value)
VALUES ('topswiper', '');
-- 插入示例用户组
INSERT INTO user_groups (group_name, permission_level)
VALUES ('管理员', 33554431),
       ('编辑', 3131310000);
-- 插入示例用户
INSERT INTO users (username,
                   password,
                   user_avatar,
                   user_permission,
                   user_bio,
                   user_position)
VALUES ('misaka10843',
        '$2b$12$fkpli5MgRINae5XS/.t7bOPLthjJQ08.XSDsd6aVlEK7PfMTx3CYi',
        'alice.jpg',
        '33554431',
        'qwq',
        1);