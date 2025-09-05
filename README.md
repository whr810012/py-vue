# 社区志愿服务系统

[![Vue.js](https://img.shields.io/badge/Vue.js-3.3.4-4FC08D?style=flat-square&logo=vue.js)](https://vuejs.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-000000?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![Element Plus](https://img.shields.io/badge/Element%20Plus-2.3.9-409EFF?style=flat-square&logo=element)](https://element-plus.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

一个现代化的社区志愿服务管理系统，基于 Vue.js 3 + Flask 构建，提供完整的志愿活动管理解决方案。

## ✨ 功能特性

### 🎯 核心功能
- **用户管理** - 注册、登录、个人资料管理
- **活动管理** - 创建、编辑、删除志愿活动
- **报名系统** - 在线报名、签到、完成确认
- **数据统计** - 参与统计、时长统计、图表展示
- **个人中心** - 我的活动、参与记录、个人设置

### 🚀 技术亮点
- **响应式设计** - 支持桌面端和移动端
- **实时更新** - 基于 WebSocket 的实时通知
- **权限控制** - JWT 身份验证和角色管理
- **数据可视化** - 丰富的图表和统计展示
- **文件上传** - 支持头像和活动图片上传

## 🛠 技术栈

### 前端技术
- **框架**: Vue 3 (Composition API)
- **路由**: Vue Router 4
- **状态管理**: Vuex 4
- **UI组件**: Element Plus
- **HTTP客户端**: Axios
- **样式**: SCSS + CSS Variables
- **构建工具**: Vue CLI 5

### 后端技术
- **框架**: Flask 2.3.3
- **ORM**: SQLAlchemy
- **身份验证**: Flask-JWT-Extended
- **跨域处理**: Flask-CORS
- **数据库**: SQLite (开发) / PostgreSQL (生产)

## 🚀 快速开始

### 方式一：一键启动（推荐）

```bash
# 克隆项目
git clone <repository-url>
cd py-vue

# 安装所有依赖
npm run install:all

# 一键启动前后端
npm run start:dev
```

### 方式二：使用启动脚本

**Windows:**
```bash
# 双击运行或命令行执行
start.bat
```

**macOS/Linux:**
```bash
# 给脚本执行权限并运行
chmod +x start.sh
./start.sh
```

**跨平台Node.js脚本:**
```bash
npm install
npm start
```

### 方式三：分别启动

**后端服务:**
```bash
cd backend
pip install -r requirements.txt
python run.py
```

**前端服务:**
```bash
cd frontend
npm install
npm run serve
```

## 📁 项目结构

```
py-vue/
├── 📁 backend/                 # Flask 后端服务
│   ├── 📁 app/
│   │   ├── 📁 models/          # 数据模型
│   │   │   ├── user.py         # 用户模型
│   │   │   └── activity.py     # 活动模型
│   │   ├── 📁 routes/          # API 路由
│   │   │   ├── auth.py         # 认证路由
│   │   │   ├── users.py        # 用户路由
│   │   │   └── activities.py   # 活动路由
│   │   └── __init__.py         # 应用初始化
│   ├── 📁 instance/            # 实例配置
│   ├── requirements.txt        # Python 依赖
│   └── run.py                  # 启动文件
├── 📁 frontend/                # Vue 前端应用
│   ├── 📁 public/              # 静态资源
│   ├── 📁 src/
│   │   ├── 📁 api/             # API 接口
│   │   ├── 📁 assets/          # 资源文件
│   │   ├── 📁 router/          # 路由配置
│   │   ├── 📁 store/           # Vuex 状态管理
│   │   ├── 📁 views/           # 页面组件
│   │   │   ├── Activities.vue  # 活动列表
│   │   │   ├── CreateActivity.vue # 创建活动
│   │   │   ├── MyActivities.vue   # 我的活动
│   │   │   ├── Profile.vue     # 个人中心
│   │   │   └── Statistics.vue  # 数据统计
│   │   ├── App.vue             # 根组件
│   │   └── main.js             # 入口文件
│   ├── package.json            # 前端依赖
│   └── vue.config.js           # Vue 配置
├── 📄 package.json             # 项目脚本
├── 📄 start.bat                # Windows 启动脚本
├── 📄 start.sh                 # Unix 启动脚本
├── 📄 start.js                 # Node.js 启动脚本
├── 📄 启动指南.md               # 详细启动指南
└── 📄 README.md                # 项目说明
```

## 🌐 访问地址

启动成功后，可以通过以下地址访问：

- **前端应用**: http://localhost:8081
- **后端API**: http://localhost:5000
- **API文档**: http://localhost:5000/api/docs (开发中)

## 📋 可用脚本

在项目根目录下提供了以下npm脚本：

```bash
# 开发相关
npm start                 # 启动Node.js脚本
npm run start:dev         # 使用concurrently同时启动前后端
npm run start:backend     # 只启动后端服务
npm run start:frontend    # 只启动前端服务

# 构建和部署
npm run build            # 构建前端生产版本

# 依赖管理
npm run install:all      # 安装前后端所有依赖
npm run clean           # 清理缓存和构建文件
```

## 🔧 开发指南

### 环境要求

- **Node.js**: >= 14.0.0
- **Python**: >= 3.7
- **npm**: >= 6.0.0
- **pip**: 最新版本

### 开发流程

1. **Fork 项目**
2. **创建功能分支**: `git checkout -b feature/amazing-feature`
3. **提交更改**: `git commit -m 'Add some amazing feature'`
4. **推送分支**: `git push origin feature/amazing-feature`
5. **提交 Pull Request**

### 代码规范

- **前端**: 遵循 Vue.js 官方风格指南
- **后端**: 遵循 PEP 8 Python 代码规范
- **提交信息**: 使用 Conventional Commits 规范

## 🚀 部署指南

### 开发环境

```bash
# 使用开发脚本
npm run start:dev
```

### 生产环境

**前端构建:**
```bash
cd frontend
npm run build
```

**后端生产部署:**
```bash
cd backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

**使用Docker (推荐):**
```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d
```

## 📊 系统截图

### 主要功能界面

- 🏠 **首页** - 活动列表和搜索
- 👤 **用户中心** - 个人信息和活动记录
- 📝 **活动管理** - 创建和编辑活动
- 📈 **数据统计** - 可视化图表展示

## 🤝 贡献指南

我们欢迎所有形式的贡献！请查看 [贡献指南](CONTRIBUTING.md) 了解详细信息。

### 贡献者

感谢所有为这个项目做出贡献的开发者！

## 📄 许可证

本项目基于 [MIT License](LICENSE) 开源协议。

## 🆘 获取帮助

如果你在使用过程中遇到问题，可以通过以下方式获取帮助：

- 📖 查看 [启动指南](启动指南.md)
- 🐛 提交 [Issue](../../issues)
- 💬 参与 [Discussions](../../discussions)
- 📧 发送邮件至: support@example.com

## 🔄 更新日志

### v1.0.0 (2024-01-XX)
- ✨ 初始版本发布
- 🎯 完整的用户管理系统
- 📅 志愿活动管理功能
- 📊 数据统计和可视化
- 🚀 多种启动方式支持

---

<div align="center">
  <p>如果这个项目对你有帮助，请给我们一个 ⭐️</p>
  <p>Made with ❤️ by 开发团队</p>
</div>