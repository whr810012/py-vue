<template>
  <div id="app">
    <el-container class="app-container">
      <!-- 顶部导航栏 -->
      <el-header class="app-header" v-if="!isLoginPage">
        <div class="header-content">
          <div class="logo">
            <el-icon><Star /></el-icon>
            <span>志愿服务系统</span>
          </div>
          <el-menu
            :default-active="activeIndex"
            class="header-menu"
            mode="horizontal"
            @select="handleMenuSelect"
          >
            <el-menu-item index="/home">首页</el-menu-item>
            <el-menu-item index="/activities">活动列表</el-menu-item>
            <el-menu-item index="/my-activities" v-if="isLoggedIn">我的活动</el-menu-item>
            <el-menu-item index="/profile" v-if="isLoggedIn">个人中心</el-menu-item>
          </el-menu>
          <div class="header-actions">
            <template v-if="isLoggedIn">
              <el-dropdown @command="handleUserAction">
                <span class="user-info">
                  <el-avatar :size="32" :src="userInfo.avatar">
                    <el-icon><User /></el-icon>
                  </el-avatar>
                  <span class="username">{{ userInfo.real_name || userInfo.username }}</span>
                  <el-icon class="el-icon--right"><arrow-down /></el-icon>
                </span>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="profile">个人资料</el-dropdown-item>
                    <el-dropdown-item command="statistics">我的统计</el-dropdown-item>
                    <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </template>
            <template v-else>
              <el-button type="primary" @click="$router.push('/login')">登录</el-button>
              <el-button @click="$router.push('/register')">注册</el-button>
            </template>
          </div>
        </div>
      </el-header>

      <!-- 主要内容区域 -->
      <el-main class="app-main" :class="{ 'login-page': isLoginPage }">
        <router-view />
      </el-main>

      <!-- 底部 -->
      <el-footer class="app-footer" v-if="!isLoginPage">
        <div class="footer-content">
          <p>&copy; 2024 社区志愿服务系统. All rights reserved.</p>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'

export default {
  name: 'App',
  computed: {
    ...mapState('auth', ['isLoggedIn', 'userInfo']),
    isLoginPage() {
      return ['/login', '/register'].includes(this.$route.path)
    },
    activeIndex() {
      return this.$route.path
    }
  },
  methods: {
    ...mapActions('auth', ['logout']),
    handleMenuSelect(index) {
      this.$router.push(index)
    },
    handleUserAction(command) {
      switch (command) {
        case 'profile':
          this.$router.push('/profile')
          break
        case 'statistics':
          this.$router.push('/statistics')
          break
        case 'logout':
          this.handleLogout()
          break
      }
    },
    async handleLogout() {
      try {
        await this.logout()
        this.$message.success('退出登录成功')
        this.$router.push('/login')
      } catch (error) {
        this.$message.error('退出登录失败')
      }
    }
  },
  created() {
    // 检查本地存储的token
    const token = localStorage.getItem('token')
    if (token && !this.isLoggedIn) {
      this.$store.dispatch('auth/checkAuth')
    }
  }
}
</script>

<style lang="scss">
.app-container {
  min-height: 100vh;
}

.app-header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 0;
  height: 60px;
  line-height: 60px;

  .header-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }

  .logo {
    display: flex;
    align-items: center;
    font-size: 20px;
    font-weight: bold;
    color: #409eff;

    .el-icon {
      margin-right: 8px;
      font-size: 24px;
    }
  }

  .header-menu {
    flex: 1;
    margin: 0 40px;
    border-bottom: none;
  }

  .header-actions {
    display: flex;
    align-items: center;
    gap: 12px;

    .user-info {
      display: flex;
      align-items: center;
      cursor: pointer;
      padding: 8px 12px;
      border-radius: 4px;
      transition: background-color 0.3s;

      &:hover {
        background-color: #f5f7fa;
      }

      .username {
        margin: 0 8px;
        font-size: 14px;
      }
    }
  }
}

.app-main {
  min-height: calc(100vh - 120px);
  padding: 20px;
  background: #f5f7fa;

  &.login-page {
    padding: 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }
}

.app-footer {
  background: #fff;
  border-top: 1px solid #e4e7ed;
  height: 60px;
  line-height: 60px;
  text-align: center;
  color: #909399;

  .footer-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }
}
</style>