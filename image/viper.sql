




-- 班级表
CREATE TABLE classes (
    class_id INTEGER PRIMARY KEY,  -- 自动自增
    class_name TEXT NOT NULL
);


-- 学生表
CREATE TABLE student (
    student_id INTEGER PRIMARY KEY,  -- 自动自增
    student_name TEXT NOT NULL,
    student_number TEXT NOT NULL UNIQUE,
    gender INTEGER NOT NULL,         -- 1=男, 2=女
    class_id INTEGER NOT NULL,
    chinese_score REAL,
    math_score REAL,
    english_score REAL
);


-- 用户表
CREATE TABLE user (
    user_id INTEGER PRIMARY KEY,     -- 自动自增
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,          -- 存储加密后的密码
    nickname TEXT,
    user_role INTEGER,               -- 1=管理员, 2=老师
    class_id TEXT                    -- 逗号分隔班级ID，如 '1,2,3'
);



1. classes 表
用途: 存储班级的基本信息
主键: class_id
外键: 无
字段说明:
class_id: 班级的唯一标识符，自增主键
class_name: 班级的名称，不能为空

2. student 表
用途: 存储学生的基本信息及成绩
主键: student_id
外键: class_id 关联到 classes 表的 class_id
字段说明:
student_id: 学生的唯一标识符，自增主键
student_name: 学生姓名，不能为空
student_number: 学号，不能为空且唯一
gender: 性别，1表示"男"，2表示"女"
class_id: 学生所属班级ID，不能为空，关联 classes 表的 class_id 字段
chinese_score: 语文成绩，可以为空
math_score: 数学成绩，可以为空
english_score: 英语成绩，可以为空

3. user 表
用途: 存储系统用户的基本信息及权限
主键: user_id
外键: 无（但 class_id 可以作为逻辑外键，关联 classes 表的 class_id 字段）
字段说明:
user_id: 用户的唯一标识符，自增主键
username: 用户名，不能为空且唯一
password: 密码，不能为空
nickname: 用户昵称，可以为空
user_role: 用户角色，1表示管理员，2表示老师
class_id: 管理班级的ID列表，使用逗号分隔的字符串形式保存，如"1,2,3"

