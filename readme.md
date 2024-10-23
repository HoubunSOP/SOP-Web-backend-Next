```mysql
-- 创建comic_authors表
CREATE TABLE comic_authors
(
    id       INT          NOT NULL AUTO_INCREMENT COMMENT '漫画作者唯一标识',
    name     VARCHAR(255) NOT NULL COMMENT '漫画作者名称',
    PRIMARY KEY (id)
);

-- 创建comics表
CREATE TABLE comics
(
    id         INT          NOT NULL AUTO_INCREMENT COMMENT '漫画唯一标识',
    name       VARCHAR(255) NOT NULL COMMENT '漫画名称',
    author_id  INT          NOT NULL COMMENT '漫画作者ID',
    date       DATE         NOT NULL COMMENT '漫画发布日期',
    intro      TEXT         COMMENT '漫画简介，支持Markdown语法',
    cover      VARCHAR(255) NOT NULL COMMENT '封面图片文件名',
    auto       BOOLEAN      NOT NULL DEFAULT FALSE COMMENT '是否为自动生成',
    PRIMARY KEY (id),
    FOREIGN KEY (author_id) REFERENCES comic_authors(id) ON DELETE CASCADE
);

-- 创建users表
CREATE TABLE users
(
    id            INT          NOT NULL AUTO_INCREMENT COMMENT '用户唯一标识',
    username      VARCHAR(255) NOT NULL COMMENT '用户名',
    user_avatar   VARCHAR(255) DEFAULT NULL COMMENT '用户头像',
    user_permission VARCHAR(50) NOT NULL COMMENT '用户权限',
    user_bio      TEXT         DEFAULT NULL COMMENT '用户简介',
    user_position VARCHAR(255) DEFAULT NULL COMMENT '用户职位',
    PRIMARY KEY (id)
);

-- 创建articles表
CREATE TABLE articles
(
    id            INT          NOT NULL AUTO_INCREMENT COMMENT '文章唯一标识',
    title         VARCHAR(255) NOT NULL COMMENT '文章标题',
    date          DATE         NOT NULL COMMENT '文章发布日期',
    content       TEXT         COMMENT '文章内容，支持Markdown语法',
    cover         VARCHAR(255) DEFAULT NULL COMMENT '文章封面',
    comic         VARCHAR(255) DEFAULT NULL COMMENT '关联漫画',
    recommended   BOOLEAN      DEFAULT FALSE COMMENT '是否为推荐文章',
    author_id     INT          NOT NULL COMMENT '作者ID',
    PRIMARY KEY (id),
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 创建magazines表
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

-- 创建分类类型表
CREATE TABLE category_types
(
    id   INT          NOT NULL AUTO_INCREMENT COMMENT '分类类型唯一标识',
    name VARCHAR(255) NOT NULL COMMENT '分类类型名称', -- 漫画、文章、杂志等
    PRIMARY KEY (id)
);

-- 创建分类表
CREATE TABLE categories
(
    id             INT          NOT NULL AUTO_INCREMENT COMMENT '分类唯一标识',
    name           VARCHAR(255) NOT NULL COMMENT '分类名称',
    category_type  INT          NOT NULL COMMENT '分类类型ID',
    PRIMARY KEY (id),
    FOREIGN KEY (category_type) REFERENCES category_types(id) ON DELETE CASCADE
);

-- 创建comic_category_map表，用于关联漫画和分类
CREATE TABLE comic_category_map
(
    comic_id    INT NOT NULL COMMENT '漫画唯一标识',
    category_id INT NOT NULL COMMENT '分类唯一标识',
    PRIMARY KEY (comic_id, category_id),
    FOREIGN KEY (comic_id) REFERENCES comics(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- 创建article_category_map表，用于关联文章和分类
CREATE TABLE article_category_map
(
    article_id  INT NOT NULL COMMENT '文章唯一标识',
    category_id INT NOT NULL COMMENT '分类唯一标识',
    PRIMARY KEY (article_id, category_id),
    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- 创建magazine_category_map表，用于关联杂志和分类
CREATE TABLE magazine_category_map
(
    magazine_id INT NOT NULL COMMENT '杂志唯一标识',
    category_id INT NOT NULL COMMENT '分类唯一标识',
    PRIMARY KEY (magazine_id, category_id),
    FOREIGN KEY (magazine_id) REFERENCES magazines(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- 创建magazine_comic_map表，用于关联杂志和漫画
CREATE TABLE magazine_comic_map
(
    magazine_id INT NOT NULL COMMENT '杂志唯一标识',
    comic_id    INT NOT NULL COMMENT '漫画唯一标识',
    PRIMARY KEY (magazine_id, comic_id),
    FOREIGN KEY (magazine_id) REFERENCES magazines(id) ON DELETE CASCADE,
    FOREIGN KEY (comic_id) REFERENCES comics(id) ON DELETE CASCADE
);

-- 创建settings表
CREATE TABLE settings
(
    id        INT          NOT NULL COMMENT '唯一标识',
    topswiper VARCHAR(255) NOT NULL COMMENT 'topswiper的文章id'
);

-- 插入分类类型数据
INSERT INTO category_types (name)
VALUES ('漫画'), ('文章'), ('杂志');

-- 添加漫画分类示例
INSERT INTO categories (name, category_type)
VALUES ('Kirara', 1),
       ('MAX', 1),
       ('Carat', 1),
       ('Forward', 1);

-- 添加文章分类示例
INSERT INTO categories (name, category_type)
VALUES ('未分类', 2);

-- 添加杂志分类示例
INSERT INTO categories (name, category_type)
VALUES ('Kirara', 3),
       ('MAX', 3),
       ('Carat', 3),
       ('Forward', 3);

-- 插入settings表的初始数据
INSERT INTO settings (id, topswiper)
VALUES ('0', '');

```
接下来我会告诉你根据上方数据库会怎么操作

但是在此之前我想修改一下文章表中的comic是与漫画id进行关联，并且可以关联多个，请你根据情况来进行修改


增删改comics
增时我会提供name，作者ID，date,intro,cover,auto以及漫画的分类（其中如果没有提供分类的话就放到漫画的未分类中）

增删改articles
增时我会提供title,date,content,cover,comic,author_id以及文章分类（其中如果没有提供分类的话就放到文章的未分类中）

增删改magazine
增时我会提供name,publish_date,intro,cover,link,author_id以及comic id数组（其中如果没有提供分类的话就放到文章的未分类中）

增删改categories 
增时我会提供name与type

在获取指定ID的comic时我希望获取到comics中的name，作者ID，作者名称，date,intro,cover,auto以及漫画的分类，还有链接到mangazine的ID以及名称和cover
在获取指定ID的articles时我希望获取到title,date,content,cover,comic,author_id，作者名称，以及文章分类，还有链接到所有comic的ID以及名称和cover
在获取指定ID的magazine时我希望获取到title,date,content,cover,comic,author_id以及文章分类