-- 创建 comic_authors 表
CREATE TABLE comic_authors
(
    id   INT          NOT NULL AUTO_INCREMENT COMMENT '漫画作者唯一标识',
    name VARCHAR(255) NOT NULL COMMENT '漫画作者名称',
    PRIMARY KEY (id)
);
-- 创建 comics 表
CREATE TABLE comics
(
    id            INT          NOT NULL AUTO_INCREMENT COMMENT '漫画唯一标识',
    name          VARCHAR(255) NOT NULL COMMENT '漫画名称',
    original_name VARCHAR(255)          DEFAULT NULL COMMENT '漫画原名',
    author_id     INT          NOT NULL COMMENT '漫画作者ID',
    date          DATE         NOT NULL COMMENT '漫画发布日期',
    intro         TEXT COMMENT '漫画简介，支持Markdown语法',
    cover         VARCHAR(255) NOT NULL COMMENT '封面图片文件名',
    auto          BOOLEAN      NOT NULL DEFAULT FALSE COMMENT '是否为自动生成',
    volume        INT                   DEFAULT '1' COMMENT '卷数',
    isbn          BIGINT                DEFAULT NULL COMMENT 'ISBN码',
    cid           INT                   DEFAULT NULL COMMENT '官方网站/第三方网站ID(爬虫用)',
    PRIMARY KEY (id),
    FOREIGN KEY (author_id) REFERENCES comic_authors (id) ON DELETE CASCADE
);
-- 创建用户组表
CREATE TABLE user_groups
(
    id               INT          NOT NULL AUTO_INCREMENT COMMENT '用户组唯一标识',
    group_name       VARCHAR(255) NOT NULL COMMENT '用户组名称',
    permission_level BIGINT       NOT NULL COMMENT '用户权限',
    PRIMARY KEY (id)
);
-- 创建 users 表
CREATE TABLE users
(
    id              INT          NOT NULL AUTO_INCREMENT COMMENT '用户唯一标识',
    username        VARCHAR(255) NOT NULL COMMENT '用户名',
    password        VARCHAR(255) NOT NULL COMMENT '密码',
    user_avatar     VARCHAR(255) DEFAULT NULL COMMENT '用户头像',
    user_permission BIGINT       DEFAULT '0' COMMENT '用户权限',
    user_bio        TEXT         DEFAULT NULL COMMENT '用户简介',
    user_position   INT          DEFAULT NULL COMMENT '用户组ID，允许为空',
    PRIMARY KEY (id),
    FOREIGN KEY (user_position) REFERENCES user_groups (id) ON DELETE
        SET NULL
);
-- 创建 articles 表
CREATE TABLE articles
(
    id          INT          NOT NULL AUTO_INCREMENT COMMENT '文章唯一标识',
    title       VARCHAR(255) NOT NULL COMMENT '文章标题',
    date        DATE         NOT NULL COMMENT '文章发布日期',
    content     TEXT COMMENT '文章内容，支持Markdown语法',
    cover       VARCHAR(255) DEFAULT NULL COMMENT '文章封面',
    comic       VARCHAR(255) DEFAULT NULL COMMENT '关联漫画',
    recommended BOOLEAN      DEFAULT FALSE COMMENT '是否为推荐文章',
    author_id   INT          NOT NULL COMMENT '作者ID',
    PRIMARY KEY (id),
    FOREIGN KEY (author_id) REFERENCES users (id) ON DELETE CASCADE
);
-- 创建 magazines 表
CREATE TABLE magazines
(
    id           INT          NOT NULL AUTO_INCREMENT COMMENT '杂志唯一标识',
    name         VARCHAR(255) NOT NULL COMMENT '杂志名称',
    cover        VARCHAR(255) NOT NULL COMMENT '杂志封面',
    publish_date DATE         NOT NULL COMMENT '杂志发布时间',
    intro        TEXT         DEFAULT NULL COMMENT '杂志简介',
    link         VARCHAR(255) DEFAULT NULL COMMENT '杂志链接',
    PRIMARY KEY (id)
);
-- 创建 category_types 表
CREATE TABLE category_types
(
    id   INT          NOT NULL AUTO_INCREMENT COMMENT '分类类型唯一标识',
    name VARCHAR(255) NOT NULL COMMENT '分类类型名称',
    PRIMARY KEY (id)
);
-- 创建 categories 表
CREATE TABLE categories
(
    id            INT          NOT NULL AUTO_INCREMENT COMMENT '分类唯一标识',
    name          VARCHAR(255) NOT NULL COMMENT '分类名称',
    category_type INT          NOT NULL COMMENT '分类类型ID',
    PRIMARY KEY (id),
    FOREIGN KEY (category_type) REFERENCES category_types (id) ON DELETE CASCADE
);
-- 创建 comic_category_map 表，用于关联漫画和分类
CREATE TABLE comic_category_map
(
    comic_id    INT NOT NULL COMMENT '漫画唯一标识',
    category_id INT NOT NULL COMMENT '分类唯一标识',
    PRIMARY KEY (comic_id, category_id),
    FOREIGN KEY (comic_id) REFERENCES comics (id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
);
-- 创建 article_category_map 表，用于关联文章和分类
CREATE TABLE article_category_map
(
    article_id  INT NOT NULL COMMENT '文章唯一标识',
    category_id INT NOT NULL COMMENT '分类唯一标识',
    PRIMARY KEY (article_id, category_id),
    FOREIGN KEY (article_id) REFERENCES articles (id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
);
-- 创建 magazine_category_map 表，用于关联杂志和分类
CREATE TABLE magazine_category_map
(
    magazine_id INT NOT NULL COMMENT '杂志唯一标识',
    category_id INT NOT NULL COMMENT '分类唯一标识',
    PRIMARY KEY (magazine_id, category_id),
    FOREIGN KEY (magazine_id) REFERENCES magazines (id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
);
-- 创建 magazine_comic_map 表，用于存储杂志和多个漫画名称的关联
CREATE TABLE magazine_comic_map
(
    magazine_id INT          NOT NULL COMMENT '杂志唯一标识',
    comic_name  VARCHAR(255) NOT NULL COMMENT '漫画名称',
    FOREIGN KEY (magazine_id) REFERENCES magazines (id) ON DELETE CASCADE
);
-- 创建settings表
CREATE TABLE settings
(
    settings_key   VARCHAR(255) NOT NULL COMMENT '设置项',
    settings_value VARCHAR(255) NOT NULL COMMENT '设置值',
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