# 社区志愿服务系统

基于Vue.js + Python Flask的社区志愿服务管理平台

## 项目结构

```
py-vue/
├── frontend/          # Vue.js前端项目
│   ├── src/
│   │   ├── components/    # 组件
│   │   ├── views/        # 页面
│   │   ├── router/       # 路由
│   │   ├── store/        # 状态管理
│   │   └── api/          # API接口
│   ├── public/
│   └── package.json
├── backend/           # Python Flask后端
│   ├── app/
│   │   ├── models/       # 数据模型
│   │   ├── routes/       # 路由处理
│   │   └── utils/        # 工具函数
│   ├── requirements.txt
│   └── run.py
└── README.md
```

## 功能特性

- 用户注册登录
- 志愿活动发布与管理
- 志愿者报名参与
- 活动签到打卡
- 志愿时长统计
- 个人中心管理

## 快速开始

### 后端启动
```bash
cd backend
pip install -r requirements.txt
python run.py
```

### 前端启动
```bash
cd frontend
npm install
npm run serve
```

## 技术栈

- 前端：Vue.js 3, Vue Router, Vuex, Element Plus
- 后端：Python Flask, SQLAlchemy, JWT
- 数据库：SQLite (开发环境)