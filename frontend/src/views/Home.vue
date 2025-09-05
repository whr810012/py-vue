<template>
  <div class="home">
    <!-- 英雄区域 -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">社区志愿服务平台</h1>
        <p class="hero-subtitle">连接志愿者与社区需求，共建美好家园</p>
        <div class="hero-actions">
          <el-button type="primary" size="large" @click="$router.push('/activities')">
            <el-icon><Search /></el-icon>
            浏览活动
          </el-button>
          <el-button size="large" @click="$router.push('/create-activity')" v-if="isLoggedIn">
            <el-icon><Plus /></el-icon>
            发布活动
          </el-button>
        </div>
      </div>
    </section>

    <div class="page-container">
      <!-- 统计数据 -->
      <section class="stats-section">
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">
              <el-icon><User /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">1,234</div>
              <div class="stat-label">注册志愿者</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">
              <el-icon><Calendar /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">567</div>
              <div class="stat-label">志愿活动</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">
              <el-icon><Clock /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">8,901</div>
              <div class="stat-label">服务时长</div>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">
              <el-icon><Star /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-number">4.8</div>
              <div class="stat-label">平均评分</div>
            </div>
          </div>
        </div>
      </section>

      <!-- 最新活动 -->
      <section class="activities-section">
        <div class="section-header">
          <h2>最新活动</h2>
          <el-button type="primary" link @click="$router.push('/activities')">
            查看更多 <el-icon><ArrowRight /></el-icon>
          </el-button>
        </div>
        
        <div class="activities-grid" v-loading="loading">
          <div 
            v-for="activity in recentActivities" 
            :key="activity.id" 
            class="activity-card"
            @click="$router.push(`/activities/${activity.id}`)"
          >
            <div class="activity-image">
              <el-icon><Calendar /></el-icon>
            </div>
            <div class="activity-content">
              <h3 class="activity-title">{{ activity.title }}</h3>
              <div class="activity-meta">
                <div class="meta-item">
                  <el-icon><Location /></el-icon>
                  <span>{{ activity.location }}</span>
                </div>
                <div class="meta-item">
                  <el-icon><Clock /></el-icon>
                  <span>{{ formatDate(activity.start_time) }}</span>
                </div>
              </div>
              <p class="activity-description">{{ activity.description }}</p>
              <div class="activity-footer">
                <div class="participant-info">
                  {{ activity.current_participants }}/{{ activity.max_participants }} 人
                </div>
                <el-tag 
                  :type="getActivityStatusType(activity.status)"
                  size="small"
                >
                  {{ getActivityStatusText(activity.status) }}
                </el-tag>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 活动分类 -->
      <section class="categories-section">
        <div class="section-header">
          <h2>活动分类</h2>
        </div>
        
        <div class="categories-grid">
          <div 
            v-for="category in categories" 
            :key="category.name"
            class="category-card"
            @click="goToActivities(category.name)"
          >
            <div class="category-icon">
              <el-icon><component :is="category.icon" /></el-icon>
            </div>
            <div class="category-name">{{ category.label }}</div>
            <div class="category-count">{{ category.count }} 个活动</div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import dayjs from 'dayjs'

export default {
  name: 'Home',
  data() {
    return {
      recentActivities: [],
      loading: false,
      categories: [
        { name: '环保', label: '环保公益', icon: 'Sunny', count: 45 },
        { name: '助老', label: '助老服务', icon: 'User', count: 32 },
        { name: '教育', label: '教育支持', icon: 'Reading', count: 28 },
        { name: '社区', label: '社区建设', icon: 'House', count: 56 },
        { name: '文化', label: '文化活动', icon: 'Picture', count: 23 },
        { name: '其他', label: '其他服务', icon: 'More', count: 18 }
      ]
    }
  },
  computed: {
    ...mapState('auth', ['isLoggedIn'])
  },
  methods: {
    ...mapActions('activities', ['fetchActivities']),
    
    async loadRecentActivities() {
      this.loading = true
      try {
        const response = await this.fetchActivities({ per_page: 6 })
        this.recentActivities = response.data.activities
      } catch (error) {
        this.$message.error('加载活动失败')
      } finally {
        this.loading = false
      }
    },
    
    formatDate(dateString) {
      return dayjs(dateString).format('MM-DD HH:mm')
    },
    
    getActivityStatusType(status) {
      const statusMap = {
        'active': 'success',
        'completed': 'info',
        'cancelled': 'danger'
      }
      return statusMap[status] || 'info'
    },
    
    getActivityStatusText(status) {
      const statusMap = {
        'active': '进行中',
        'completed': '已完成',
        'cancelled': '已取消'
      }
      return statusMap[status] || status
    },
    
    goToActivities(category) {
      this.$router.push({
        path: '/activities',
        query: { category }
      })
    }
  },
  
  created() {
    this.loadRecentActivities()
  }
}
</script>

<style lang="scss" scoped>
.home {
  min-height: 100vh;
}

.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 80px 0;
  text-align: center;
  
  .hero-content {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 20px;
  }
  
  .hero-title {
    font-size: 48px;
    font-weight: 700;
    margin-bottom: 20px;
    line-height: 1.2;
  }
  
  .hero-subtitle {
    font-size: 20px;
    margin-bottom: 40px;
    opacity: 0.9;
    line-height: 1.6;
  }
  
  .hero-actions {
    display: flex;
    gap: 20px;
    justify-content: center;
    flex-wrap: wrap;
  }
}

.stats-section {
  padding: 60px 0;
  
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 30px;
  }
  
  .stat-card {
    background: white;
    padding: 30px;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    display: flex;
    align-items: center;
    gap: 20px;
    transition: transform 0.3s ease;
    
    &:hover {
      transform: translateY(-4px);
    }
    
    .stat-icon {
      width: 60px;
      height: 60px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 24px;
    }
    
    .stat-content {
      .stat-number {
        font-size: 32px;
        font-weight: 700;
        color: #303133;
        line-height: 1;
        margin-bottom: 4px;
      }
      
      .stat-label {
        font-size: 14px;
        color: #909399;
      }
    }
  }
}

.activities-section, .categories-section {
  padding: 40px 0;
  
  .section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 30px;
    
    h2 {
      font-size: 28px;
      font-weight: 600;
      color: #303133;
    }
  }
  
  .activities-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 24px;
  }
}

.categories-section {
  .categories-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
  }
  
  .category-card {
    background: white;
    padding: 30px 20px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    
    &:hover {
      transform: translateY(-4px);
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    .category-icon {
      width: 60px;
      height: 60px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 16px;
      color: white;
      font-size: 24px;
    }
    
    .category-name {
      font-size: 18px;
      font-weight: 600;
      color: #303133;
      margin-bottom: 8px;
    }
    
    .category-count {
      font-size: 14px;
      color: #909399;
    }
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: 60px 0;
    
    .hero-title {
      font-size: 36px;
    }
    
    .hero-subtitle {
      font-size: 18px;
    }
    
    .hero-actions {
      flex-direction: column;
      align-items: center;
    }
  }
  
  .stats-section {
    .stats-grid {
      grid-template-columns: 1fr;
    }
  }
  
  .activities-grid {
    grid-template-columns: 1fr;
  }
  
  .categories-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>